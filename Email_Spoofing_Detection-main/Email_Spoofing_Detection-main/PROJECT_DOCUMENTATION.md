# Email Spoofing Detection System - Technical Documentation

## Project Overview

This project implements an email spoofing detection system using a combination of:
1. Machine Learning-based content analysis
2. Email authentication protocol verification (SPF, DMARC)
3. Gmail API integration for email access

## System Architecture

### 1. Machine Learning Component

#### Training Phase
```
Data Collection → Preprocessing → Feature Extraction → Model Training → Model Evaluation
```

**Implementation Details:**
- Uses Random Forest Classifier with TF-IDF vectorization
- Performs hyperparameter tuning using GridSearchCV
- Model and vectorizer are saved as `model.pkl` and `vectorizer.pkl`

```python
# Key components of ML pipeline
vectorizer = TfidfVectorizer(stop_words='english')
classifier = RandomForestClassifier()
pipeline = Pipeline([
    ('vectorizer', vectorizer),
    ('classifier', classifier)
])
```

### 2. Email Authentication System

#### Authentication Flow
```
Email Headers → SPF Check → DMARC Check → Authentication Score Calculation
```

**Implementation Details:**
- Verifies SPF records using DNS queries
- Validates DMARC policies
- Combines results for authentication scoring

### 3. Gmail API Integration

#### OAuth2 Authentication Flow
```
User Login → OAuth Consent → Token Generation → Gmail API Access
```

**Implementation Details:**
- Uses OAuth 2.0 for secure Gmail access
- Stores credentials securely
- Implements token refresh mechanism

## Complete System Flow

1. **Initial Setup**
   ```
   Load ML Model → Initialize Gmail API → Configure Authentication
   ```

2. **User Authentication**
   ```
   User Login → OAuth Consent → Gmail Access Grant
   ```

3. **Email Analysis Process**
   ```
   Fetch Emails → Extract Content → Perform Analysis → Generate Results
   ```

4. **Analysis Components**
   - **ML Analysis**
     ```
     Clean Text → Vectorize → Predict → Get Confidence Score
     ```
   - **Authentication Check**
     ```
     Extract Headers → Check SPF → Check DMARC → Calculate Score
     ```

5. **Result Generation**
   ```
   Combine Scores → Generate Warnings → Display Results
   ```

## Implementation Details

### 1. Machine Learning Model Training
```python
# Data preprocessing
def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    return text.lower()

# Model training pipeline
pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer(stop_words='english')),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Hyperparameter tuning
param_grid = {
    'classifier__n_estimators': [50, 100],
    'classifier__max_depth': [10, 20, None],
    'classifier__min_samples_split': [2, 5]
}
```

### 2. Email Authentication Verification
```python
def check_spf_record(domain):
    # DNS query for SPF record
    resolver = dns.resolver.Resolver()
    txt_records = resolver.resolve(domain, 'TXT')
    
    # Validate SPF record format and content
    for record in txt_records:
        if record.startswith('v=spf1'):
            return validate_spf_record(record)
```

### 3. Gmail API Integration
```python
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)
```

## Security Considerations

1. **Data Protection**
   - Credentials stored securely
   - Only read-only access to Gmail
   - No storage of email content

2. **Authentication Security**
   - OAuth 2.0 implementation
   - Secure token handling
   - Regular token refresh

3. **Email Analysis Security**
   - Server-side processing
   - Sanitized input handling
   - Secure DNS queries

## Performance Optimization

1. **ML Model**
   - Optimized hyperparameters
   - Efficient text vectorization
   - Model caching

2. **Email Processing**
   - Batch processing of emails
   - Efficient header parsing
   - DNS query optimization

## Future Enhancements

1. **Machine Learning**
   - Implement deep learning models
   - Add support for more languages
   - Real-time model updates

2. **Authentication**
   - Add DKIM verification
   - Implement ARC checking
   - Enhanced header analysis

3. **User Interface**
   - Real-time analysis
   - Detailed report generation
   - Custom rule configuration

## Troubleshooting Guide

1. **Common Issues**
   - OAuth token expiration
   - DNS resolution failures
   - Model loading errors

2. **Solutions**
   - Token refresh implementation
   - DNS fallback mechanisms
   - Model version control

## API Documentation

### 1. Email Analysis Endpoint
```python
@app.route('/analyze_emails')
def analyze_emails():
    """
    Analyzes recent emails for spoofing attempts
    Returns: JSON with analysis results
    """
```

### 2. Authentication Endpoints
```python
@app.route('/authorize')
def authorize():
    """
    Initiates OAuth flow
    Returns: Redirect to Google consent
    """

@app.route('/oauth2callback')
def oauth2callback():
    """
    Handles OAuth callback
    Returns: Redirect to main application
    """
```

## Deployment Guide

1. **Prerequisites**
   - Python 3.8+
   - Required packages
   - Google Cloud project

2. **Installation Steps**
   - Clone repository
   - Install dependencies
   - Configure credentials

3. **Configuration**
   - Set up environment
   - Configure OAuth
   - Initialize ML models 