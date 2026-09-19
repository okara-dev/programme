"""
E-Mail-Versand für Lern-Bot
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
    
    def send_lernthema(self, thema, kategorie, erklaerung, wikipedia, fun_fact):
        subject = f"🎓 {kategorie}: {thema}"
        
        html_body = self._build_html(thema, kategorie, erklaerung, wikipedia, fun_fact)
        text_body = self._build_text(thema, kategorie, erklaerung, wikipedia, fun_fact)
        
        return self.send_email_html(subject, html_body, text_body)
    
    def _build_html(self, thema, kategorie, erklaerung, wikipedia, fun_fact):
        # Kategorie-Icon
        icons = {
            "Physik": "⚛️",
            "Biologie": "🧬",
            "Psychologie": "🧠"
        }
        icon = icons.get(kategorie, "🎓")
        
        # Wikipedia-Sektion
        wiki_html = ""
        if wikipedia:
            thumbnail = wikipedia.get("thumbnail", "")
            img_html = f'<img src="{thumbnail}" alt="{thema}" style="max-width: 100%; border-radius: 12px; margin: 15px 0;">' if thumbnail else ""
            
            wiki_html = f"""
            <div style="background: #f0f9ff; padding: 20px; border-radius: 12px; margin: 20px 0; border-left: 4px solid #0284c7;">
                <h4 style="margin: 0 0 10px 0; color: #0369a1;">📖 Aus Wikipedia:</h4>
                {img_html}
                <p style="margin: 10px 0; color: #0c4a6e; line-height: 1.7;">{wikipedia.get('extract', '')}</p>
                <a href="{wikipedia.get('url', '#')}" style="color: #0284c7; font-weight: 600; text-decoration: none;">→ Ganzen Artikel lesen</a>
            </div>
            """
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 750px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f0fdf4;
            color: #2d3748;
            line-height: 1.7;
        }}
        .container {{
            background-color: #ffffff;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 4px 16px rgba(16, 185, 129, 0.1);
            border-top: 5px solid #10b981;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px dashed #a7f3d0;
        }}
        .header h1 {{
            font-size: 28px;
            color: #10b981;
            margin: 0;
        }}
        .header p {{
            color: #a0aec0;
            margin: 8px 0 0 0;
        }}
        .kategorie-badge {{
            display: inline-block;
            padding: 6px 16px;
            background: #10b981;
            color: white;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .section-title {{
            font-size: 20px;
            color: #10b981;
            border-bottom: 3px solid #a7f3d0;
            padding-bottom: 10px;
            margin: 30px 0 15px 0;
        }}
        .erklaerung-box {{
            background: #f0fdf4;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #10b981;
            font-size: 16px;
            color: #065f46;
            white-space: pre-wrap;
        }}
        .fun-fact-box {{
            background: linear-gradient(135deg, #fef3c7, #fde68a);
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            border-left: 4px solid #f59e0b;
            font-size: 16px;
            color: #78350f;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #a7f3d0;
            font-size: 13px;
            color: #a0aec0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="kategorie-badge">{icon} {kategorie}</div>
            <h1>🎓 Lernthema des Tages</h1>
            <p>{datetime.now().strftime('%A, %d. %B %Y')}</p>
        </div>

        <div class="section-title">📚 {thema}</div>
        <div class="erklaerung-box">
            {erklaerung}
        </div>

        {wiki_html}

        <div class="section-title">💡 Fun Fact</div>
        <div class="fun-fact-box">
            {fun_fact}
        </div>

        <div class="footer">
            🎓 Dein Lern-Bot<br>
            <small>Bleib neugierig – Wissen ist Macht!</small>
        </div>
    </div>
</body>
</html>"""
    
    def _build_text(self, thema, kategorie, erklaerung, wikipedia, fun_fact):
        lines = [
            f"🎓 LERNTHEMA DES TAGES – {kategorie}",
            "=" * 60,
            f"{datetime.now().strftime('%d.%m.%Y')}",
            "",
            f"📚 THEMA: {thema}",
            "-" * 60,
            erklaerung,
            "",
        ]
        
        if wikipedia:
            lines.append("📖 AUS WIKIPEDIA:")
            lines.append("-" * 60)
            lines.append(wikipedia.get('extract', '')[:600] + "...")
            lines.append(f"🔗 {wikipedia.get('url', '')}")
            lines.append("")
        
        lines.append("💡 FUN FACT:")
        lines.append("-" * 60)
        lines.append(fun_fact)
        lines.append("")
        lines.append("=" * 60)
        lines.append("🎓 Bleib neugierig!")
        
        return "\n".join(lines)
    
    def send_email_html(self, subject, html_body, text_body):
        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = self.sender
            msg["To"] = self.receiver
            msg["Subject"] = subject
            
            msg.attach(MIMEText(text_body, "plain", "utf-8"))
            msg.attach(MIMEText(html_body, "html", "utf-8"))
            
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