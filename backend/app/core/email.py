"""
Email Service - SendGrid / SMTP (Track A + B)
For client notifications, onboarding, billing
"""
from typing import List, Dict, Optional
import os
from datetime import datetime

class EmailService:
    def __init__(self):
        self.provider = os.getenv("EMAIL_PROVIDER", "mock")  # mock, sendgrid, smtp
        self.from_email = os.getenv("FROM_EMAIL", "noreply@ai-agency.os")
        self.sendgrid_key = os.getenv("SENDGRID_API_KEY")
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = os.getenv("SMTP_PORT", "587")
        
        # In-memory email log for demo
        self.sent_emails = []
    
    async def send_email(self, to: str, subject: str, html: str, text: str = None) -> Dict:
        email_data = {
            "id": f"email_{datetime.utcnow().timestamp()}",
            "to": to,
            "from": self.from_email,
            "subject": subject,
            "html": html,
            "text": text or html,
            "provider": self.provider,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "sent"
        }
        
        if self.provider == "sendgrid" and self.sendgrid_key:
            try:
                # Real SendGrid implementation
                import sendgrid
                from sendgrid.helpers.mail import Mail
                sg = sendgrid.SendGridAPIClient(api_key=self.sendgrid_key)
                message = Mail(
                    from_email=self.from_email,
                    to_emails=to,
                    subject=subject,
                    html_content=html
                )
                response = sg.send(message)
                email_data["sendgrid_status"] = response.status_code
            except Exception as e:
                email_data["status"] = "failed"
                email_data["error"] = str(e)
        elif self.provider == "smtp" and self.smtp_host:
            # SMTP implementation
            try:
                import smtplib
                from email.mime.text import MIMEText
                from email.mime.multipart import MIMEMultipart
                
                msg = MIMEMultipart()
                msg['From'] = self.from_email
                msg['To'] = to
                msg['Subject'] = subject
                msg.attach(MIMEText(html, 'html'))
                
                # In production: connect to SMTP and send
                email_data["smtp"] = f"Would send via {self.smtp_host}:{self.smtp_port}"
            except Exception as e:
                email_data["status"] = "failed"
                email_data["error"] = str(e)
        else:
            # Mock - just log
            print(f"📧 Mock email to {to}: {subject}")
        
        self.sent_emails.append(email_data)
        if len(self.sent_emails) > 100:
            self.sent_emails = self.sent_emails[-100:]
        
        return email_data
    
    async def send_client_onboarding(self, client_email: str, client_name: str, project_name: str) -> Dict:
        html = f"""
        <h1>مرحبا {client_name}!</h1>
        <p>تم إنشاء مشروعك <strong>{project_name}</strong> في AI Agency OS.</p>
        <p>يمكنك متابعة التقدم عبر بوابة العملاء:</p>
        <p><a href='https://ai-agency.os/client-portal'>بوابة العملاء</a></p>
        <p>فريقنا من 68 وكيل متخصص يعمل على مشروعك الآن 🤖</p>
        <br/>
        <p>مع التحية,<br/>AI Agency OS</p>
        """
        return await self.send_email(client_email, f"تم إنشاء مشروعك: {project_name}", html)
    
    async def send_task_completed(self, client_email: str, task_title: str, project_name: str) -> Dict:
        html = f"""
        <h2>✅ مهمة مكتملة: {task_title}</h2>
        <p>المشروع: {project_name}</p>
        <p>تم إكمال المهمة بنجاح. يمكنك مراجعتها في بوابة العملاء.</p>
        <p><a href='https://ai-agency.os/client-portal'>عرض التفاصيل</a></p>
        """
        return await self.send_email(client_email, f"مهمة مكتملة: {task_title}", html)
    
    async def send_proposal(self, client_email: str, client_name: str, proposal_text: str) -> Dict:
        html = f"""
        <h1>مقترح مشروع لـ {client_name}</h1>
        <div>{proposal_text}</div>
        <br/>
        <p><a href='https://ai-agency.os/approve' style='background:#8b5cf6;color:white;padding:12px 24px;border-radius:12px;text-decoration:none;'>الموافقة على المقترح</a></p>
        """
        return await self.send_email(client_email, f"مقترح مشروع من AI Agency OS", html)
    
    async def send_billing_notification(self, user_email: str, tier: str, amount: float) -> Dict:
        html = f"""
        <h2>فاتورة اشتراكك: {tier}</h2>
        <p>المبلغ: ${amount}</p>
        <p>شكراً لاستخدامك AI Agency OS!</p>
        <p>التفاصيل: <a href='https://ai-agency.os/billing'>الفوترة</a></p>
        """
        return await self.send_email(user_email, f"فاتورة {tier} - ${amount}", html)
    
    def get_sent_emails(self, limit: int = 20):
        return self.sent_emails[-limit:]

email_service = EmailService()
