from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import base64, os, json, secrets, logging
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import dns.resolver

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'  
def get_credentials():
    creds = None
    if 'credentials' in session:
        try:
            creds = Credentials(**session['credentials'])
        except Exception as e:
            logging.error(f"Error creating credentials from session: {e}")
            session.pop('credentials', None)
            return None

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            session['credentials'] = {
                'token': creds.token,
                'refresh_token': creds.refresh_token,
                'token_uri': creds.token_uri,
                'client_id': creds.client_id,
                'client_secret': creds.client_secret,
                'scopes': creds.scopes
            }
        except Exception as e:
            logging.error(f"Error refreshing credentials: {e}")
            session.pop('credentials', None)
            return None

    return creds

def check_authentication(domain):
    """Check SPF and DMARC records for a domain"""
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        
        
        spf_valid, spf_record = False, None
        try:
            txt_records = resolver.resolve(domain, 'TXT')
            for record in txt_records:
                for string in record.strings:
                    decoded = string.decode('utf-8', errors='ignore')
                    if decoded.startswith('v=spf1'):
                        spf_valid, spf_record = True, decoded
                        break
        except Exception:
            pass

        dmarc_valid, dmarc_record = False, None
        try:
            dmarc_records = resolver.resolve(f'_dmarc.{domain}', 'TXT')
            for record in dmarc_records:
                for string in record.strings:
                    if string.startswith(b'v=DMARC1'):
                        dmarc_valid, dmarc_record = True, string.decode('utf-8')
                        break
        except Exception:
            pass

        return {
            'spf_valid': spf_valid,
            'spf_record': spf_record,
            'dmarc_valid': dmarc_valid,
            'dmarc_record': dmarc_record
        }
    except Exception as e:
        logging.error(f"Error checking authentication: {str(e)}")
        return {'error': str(e)}

def analyze_email(service, msg_id):
    try:
        msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        payload = msg.get('payload', {})
        headers = payload.get('headers', [])
        header_dict = {h['name'].lower(): h['value'] for h in headers}
        
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('mimeType') == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        body += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        else:
            data = payload['body'].get('data', '')
            if data:
                body += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        
        from_header = header_dict.get('from', '')
        domain = from_header.split('@')[-1].strip('>')
        auth_results = check_authentication(domain)
      
        is_spoofed = False
        warning_flags = []
        
        if not auth_results.get('spf_valid', False):
            warning_flags.append("No valid SPF record found")
            is_spoofed = True
        if not auth_results.get('dmarc_valid', False):
            warning_flags.append("No valid DMARC record found")
            is_spoofed = True
        
        return {
            'id': msg_id,
            'date': header_dict.get('date', ''),
            'subject': header_dict.get('subject', '(No Subject)'),
            'from': from_header,
            'body': body,
            'is_spoofed': bool(is_spoofed),
            'spf_valid': bool(auth_results.get('spf_valid', False)),
            'dmarc_valid': bool(auth_results.get('dmarc_valid', False)),
            'warning_flags': warning_flags
        }
    except Exception as e:
        logging.error(f"Error analyzing email: {str(e)}")
        return {'error': str(e)}

@app.route('/')
def index():
    authenticated = 'credentials' in session
    return render_template('index.html', authenticated=authenticated)

@app.route('/analyze_emails', methods=['GET'])
def analyze_emails():
    try:
        creds = get_credentials()
        if not creds:
            return jsonify({'error': 'Not authenticated. Please connect your Gmail account first.'}), 401

        service = build('gmail', 'v1', credentials=creds)
        
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        
        if not messages:
            return jsonify({'emails': [], 'message': 'No emails found'})

        analyzed_emails = []
        for message in messages:
            analysis = analyze_email(service, message['id'])
            if 'error' not in analysis:
                analyzed_emails.append(analysis)
        
        return jsonify({'emails': analyzed_emails})
    except Exception as e:
        logging.error(f"Analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/authorize')
def authorize():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', 
        SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    try:
        state = session.get('state')
        if not state:
            return redirect(url_for('authorize'))

        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json',
            SCOPES,
            redirect_uri=url_for('oauth2callback', _external=True)
        )
        
        try:
            flow.fetch_token(
                authorization_response=request.url,
                state=state
            )
        except Warning:
            pass
        except Exception as e:
            logging.error(f"Error fetching token: {str(e)}")
            return redirect(url_for('authorize'))

        session['credentials'] = {
            'token': flow.credentials.token,
            'refresh_token': flow.credentials.refresh_token,
            'token_uri': flow.credentials.token_uri,
            'client_id': flow.credentials.client_id,
            'client_secret': flow.credentials.client_secret,
            'scopes': flow.credentials.scopes
        }
        
        session.pop('state', None)
        return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"OAuth callback error: {str(e)}")
        return redirect(url_for('authorize'))

@app.route('/clear')
def clear_session():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('credentials.json'):
        print("Error: credentials.json not found!")
        print("Please obtain credentials.json from Google Cloud Console")
    app.run(debug=True)