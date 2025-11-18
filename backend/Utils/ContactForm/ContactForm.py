import os
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel, EmailStr
import resend
from Utils.SlowApi.SlowApi import limiter
from fastapi import APIRouter

ContactFormRouter = APIRouter()



resend_api_key = os.getenv("RESEND_API_KEY")
email_to = os.getenv("EMAIL_TO")


class ContactMessage(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    subject: str
    message: str


@ContactFormRouter.post("/contact")
@limiter.limit("10 per minute")
async def send_contact_email(data: ContactMessage):

    html_content = f"""
        <h2>New Contact Form Message</h2>
        <p><strong>Name:</strong> {data.first_name} {data.last_name}</p>
        <p><strong>Email:</strong> {data.email}</p>
        <p><strong>Phone:</strong> {data.phone}</p>
        <p><strong>Subject:</strong> {data.subject}</p>
        <p><strong>Message:</strong><br>{data.message}</p>
    """

    try:
        r = resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": email_to,
            "reply_to": data.email,
            "subject": f"Contact Form: {data.subject}",
            "html": html_content,
        })

        return {"status": "ok", "id": r["id"]}

    except Exception as e:
        return {"status": "error", "error": str(e)}


re_5br8kXGQ_KNxUjgoSwdi6f9LD98UCKrS6