import smtplib
from celery import Task
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import get_settings

settings = get_settings()

class SendWelcomeEmailTask(Task):
    name = "send_welcome_email_task"

    def run(self, receiver_email: str):
        try:
            sender_email = settings.sender_email
            password = settings.email_password
            
            print(f"Password from settings: {password[:3]}...") # 비밀번호 첫 3자리만 출력
            print(f"Attempting to send email to: {receiver_email}")

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = "회원 가입을 환영합니다."

            body = "TIL 서비스를 이용해주셔서 감사합니다."
            message.attach(MIMEText(body, "plain"))

            print("Connecting to SMTP server...")
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                print("Connected, attempting login...")
                server.login(sender_email, password)
                print("Login successful, sending message...")
                server.send_message(message)
                print("Email sent successfully!")

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            raise