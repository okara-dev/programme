"""
E-Mail-Versand für Motivations-Bot
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class EmailSender:
    def __init__(self, config):
        self.sender = config.get("sender")
        self.password = config.get("password")
        self.receiver = config.get("receiver")
        self.smtp_server = config.get("smtp_server", "smtp.gmail.com")
        self.smtp_port = config.get("smtp_port", 587)
    
    def send_motivation_letter(self, letter_content, quote_content):
        subject = f"💌 Dein Brief für heute – {datetime.now().strftime('%d.%m.%Y')}"
        
        html_body = self._build_html(letter_content, quote_content)
        text_body = f"{letter_content}\n\n{quote_content}\n\n— Dein Daily Motivation Bot"
        
        return self.send_email_html(subject, html_body, text_body)
    
    def _build_html(self, letter, quote):
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Georgia, serif;
            max-width: 650px;
            margin: 0 auto;
            padding: 20px;
            background-color: #faf8f5;
            color: #2d3748;
            line-height: 1.8;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            border-top: 4px solid #d69e2e;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 28px;
            color: #d69e2e;
            margin: 0;
            font-style: italic;
        }}
        .header p {{
            color: #a0aec0;
            font-size: 14px;
            margin: 8px 0 0 0;
        }}
        .letter {{
            font-size: 17px;
            white-space: pre-wrap;
            color: #2d3748;
            margin: 25px 0;
        }}
        .quote-box {{
            margin-top: 35px;
            padding: 20px;
            background: #fefcbf;
            border-left: 4px solid #d69e2e;
            border-radius: 8px;
            font-style: italic;
            font-size: 16px;
            color: #744210;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
            font-size: 13px;
            color: #a0aec0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💌 Dein Brief für heute</h1>
            <p>{datetime.now().strftime('%A, %d. %B %Y')}</p>
        </div>
        
        <div class="letter">{self._escape(letter)}</div>
        
        <div class="quote-box">
            {self._escape(quote)}
        </div>
        
        <div class="footer">
            💌 Dein Daily Motivation Bot<br>
            <small>Diese E-Mail wurde mit KI-Unterstützung erstellt.</small>
        </div>
    </div>
</body>
</html>"""
    
    def _escape(self, text):
        if not text:
            return ""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    def send_email_html(self, subject, html_body, text_body):
        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = self.sender
            msg["To"] = self.receiver
            msg["Subject"] = subject
            
            msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=30)
            server.starttls()
            server.login(self.sender, self.password)
            server.send_message(msg)
            server.quit()
            
            print("✅ E-Mail erfolgreich gesendet!")
            return True
        except Exception as e:
            print(f"❌ E-Mail Fehler: {e}")
            return False