from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List, Union
from fastapi import HTTPException
from app.utils.token import create_access_token, decode_token

conf = ConnectionConfig(
    MAIL_USERNAME="mail_username@yourdomain.com",
    MAIL_PASSWORD="mail_password",
    MAIL_FROM="mail_username@yourdomain.com",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.mail.com",
    MAIL_TLS=False,
    MAIL_SSL=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_email_verification(to_email: str):
    subject = "Email Verification"
    message = f"Click the link below to verify your email:\n\nhttp://your-api-domain.com/verify?token={create_access_token({'sub': to_email})}"
    
    try:
        message = MessageSchema(
            subject=subject,
            recipients=[to_email],
            body=message,
            subtype="html"
        )
        fm = FastMail(conf)
        await fm.send_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

async def verify_email_token(token: str):
    try:
        payload = decode_token(token)
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid email verification token")

async def send_reset_password_email(email: str, token: str):
    subject = "Password Reset Request"
    message = f"Click on the link below to reset your password:\n\n" f"Reset link: /reset-password?token={token}"
    recipient = email

    message_schema = MessageSchema(
        subject=subject,
        recipients=[recipient],
        body=message,
        subtype="plain",
    )

    await mail.send_message(message=message_schema)
