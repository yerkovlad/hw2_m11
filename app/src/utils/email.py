from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import List, Union
from fastapi import HTTPException

conf = ConnectionConfig(
    MAIL_USERNAME="email@yourdomain.com",
    MAIL_PASSWORD="email_password",
    MAIL_FROM="email@yourdomain.com",
    MAIL_PORT=465,
    MAIL_SERVER="",
    MAIL_TLS=False,
    MAIL_SSL=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_email(to_email: Union[str, List[str]], subject: str, message: str):
    message = MessageSchema(
        subject=subject,
        recipients=[to_email] if isinstance(to_email, str) else to_email,
        body=message,
        subtype="html"
    )

    try:
        fm = FastMail(conf)
        await fm.send_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
