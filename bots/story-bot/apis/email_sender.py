"""
E-Mail-Versand für Story-Bot
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
    
    def send_story(self, title, story, genre, moral):
        subject = f"📖 Deine Geschichte für heute – {title}"
        
        html_body = self._build_html(title, story, genre, moral)
        text_body = f"📖 {title}\n\n{story}\n\n💡 Moral: {moral}\n\n— Dein Daily Story Bot"
        
        return self.send_email_html(subject, html_body, text_body)
    
    def _build_html(self, title, story, genre, moral):
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Georgia, serif;
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f3ff;
            color: #2d3748;
            line-height: 1.9;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 4px 16px rgba(79, 70, 229, 0.1);
            border-top: 4px solid #7c3aed;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px dashed #e9d8fd;
        }}
        .header h1 {{
            font-size: 30px;
            color: #7c3aed;
            margin: 0;
            font-style: italic;
        }}
        .header .genre {{
            color: #a78bfa;
            font-size: 14px;
            margin-top: 8px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .header p {{
            color: #a0aec0;
            font-size: 14px;
            margin: 8px 0 0 0;
        }}
        .story {{
            font-size: 17px;
            white-space: pre-wrap;
            color: #2d3748;
            margin: 25px 0;
            text-align: justify;
        }}
        .story::first-letter {{
            font-size: 3.5em;
            float: left;
            line-height: 0.9;
            padding-right: 8px;
            color: #7c3aed;
            font-weight: bold;
        }}
        .moral-box {{
            margin-top: 35px;
            padding: 20px;
            background: #faf5ff;
            border-left: 4px solid #7c3aed;
            border-radius: 8px;
            font-style: italic;
            font-size: 16px;
            color: #553c9a;
        }}
        .moral-box strong {{
            color: #7c3aed;
            font-style: normal;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e9d8fd;
            font-size: 13px;
            color: #a0aec0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📖 {self._escape(title)}</h1>
            <div class="genre">✨ {self._escape(genre)} ✨</div>
            <p>{datetime.now().strftime('%A, %d. %B %Y')}</p>
        </div>
        
        <div class="story">{self._escape(story)}</div>
        
        <div class="moral-box">
            <strong>💡 Moral der Geschichte:</strong><br>
            {self._escape(moral)}
        </div>
        
        <div class="footer">
            📖 Dein Daily Story Bot<br>
            <small>Diese Geschichte wurde mit KI-Unterstützung erstellt.</small>
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