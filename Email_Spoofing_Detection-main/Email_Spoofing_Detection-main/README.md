# 📧 Email Spoofing Detection Web App

A secure Flask web application that detects potential email spoofing by analyzing Gmail messages using SPF, DKIM, and DMARC authentication protocols.

---

## 🚀 Features

* ✅ **Email Authentication Check**: Verifies SPF, DKIM, and DMARC records
* ⚠️ **Spoofing Alerts**: Flags suspicious messages and spoofed emails
* 📬 **Email Viewer**: Displays full email content and headers
* 🔐 **Secure OAuth Access**: Connects to Gmail API using Google OAuth 2.0
* 💡 **Simple UI**: Clean and user-friendly interface for analysis

---

## 🛠️ Getting Started

### Prerequisites

* Python 3.7 or higher
* Gmail account with API access
* Google Cloud Console access

---

### 🔧 Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/email_spoofing_web.git
cd email_spoofing_web
```

#### 2. Set Up Python Virtual Environment

```bash
python -m venv venv

# Activate the environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

pip install -r requirements.txt
```

---

### 🔐 Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project (or select an existing one)
3. Enable **Gmail API**
4. Configure the **OAuth consent screen**
5. Create **OAuth 2.0 Client ID**
6. Download the credentials file and rename it to `credentials.json`
7. Place `credentials.json` in your project root (next to `app.py`)

---

### ▶️ Run the App

```bash
python app.py
```

Visit: [http://localhost:5000](http://localhost:5000)

---

## 📁 Project Structure

```
email_spoofing_web/
├── app.py               # Flask application
├── requirements.txt     # Python dependencies
├── credentials.json     # Google OAuth credentials (DO NOT COMMIT)
└── templates/
    └── index.html       # HTML frontend
```

---

## 🔒 Security Notes

* ❗ Do not expose `credentials.json` to version control (add it to `.gitignore`)
* Gmail access is **read-only**
* All analysis happens **server-side** to protect user data

---

## 🤝 Contributing

1. Fork this repository
2. Create a new branch: `git checkout -b feature-name`
3. Commit your changes
4. Push and open a pull request

---

## 📄 License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for full details.

---

## 🙌 Acknowledgements

* [Flask](https://flask.palletsprojects.com/)
* [Google Gmail API](https://developers.google.com/gmail/api)
* [SPF, DKIM, DMARC](https://dmarc.org/)
* [dnspython](https://www.dnspython.org/)

---

## 🛡️ Example

![App Screenshot](https://via.placeholder.com/800x400.png?text=Screenshot+of+Email+Analyzer)

---

## 📌 GitHub Tips

### `.gitignore`

```
credentials.json
__pycache__/
venv/
*.pyc
```

### Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/email_spoofing_web.git
git branch -M main
git push -u origin main
```

---
