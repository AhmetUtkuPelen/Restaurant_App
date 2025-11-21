import os
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel, EmailStr, Field, field_validator
import resend
from Utils.SlowApi.SlowApi import limiter
from fastapi import APIRouter, Request, HTTPException, status
from typing import Optional

ContactFormRouter = APIRouter(prefix="/api", tags=["Contact"])

### Initialize Resend for email provider ####
resend_api_key = os.getenv("RESEND_API_KEY")
email_to = os.getenv("EMAIL_TO")

if resend_api_key:
    resend.api_key = resend_api_key


class ContactMessage(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone: Optional[str] = Field(default=None, max_length=20)
    subject: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=10, max_length=1000)
    
    @field_validator('phone', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if v == "" or v is None:
            return None
        return v

    @field_validator('first_name')
    @classmethod
    def validate_first_name(cls, v):
        if not v or v.strip() == "":
            raise ValueError("First name is required")
        
        if not all(c.isalpha() or c in " -'" for c in v):
            raise ValueError("First name must contain only letters, spaces, hyphens, or apostrophes")
        
        return v.strip()

    @field_validator('last_name')
    @classmethod
    def validate_last_name(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Last name is required")
        
        if not all(c.isalpha() or c in " -'" for c in v):
            raise ValueError("Last name must contain only letters, spaces, hyphens, or apostrophes")
        
        return v.strip()
    
    @field_validator('subject')
    @classmethod
    def validate_subject(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Subject is required !")
        return v.strip()

    @field_validator('message')
    @classmethod
    def validate_message(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Message is required !")
        
        if len(v.strip()) < 10:
            raise ValueError("Message must be at least 10 characters long !")
        
        return v.strip()


@ContactFormRouter.post("/contact")
@limiter.limit("5/minute")
async def send_contact_email(request: Request, data: ContactMessage):
    """
    Send contact form message via email using Resend as an email provider.
    Rate limited to 5 requests / minute per IP.
    """
    
    print(f"Received contact form data: {data.model_dump()}")
    
    # check if environment variables exists or not #
    if not resend_api_key or not email_to:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email service not configured"
        )
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #3b82f6; color: white; padding: 20px; border-radius: 5px; }}
            .content {{ background-color: #f9fafb; padding: 20px; margin-top: 20px; border-radius: 5px; }}
            .field {{ margin-bottom: 15px; }}
            .label {{ font-weight: bold; color: #374151; }}
            .value {{ margin-top: 5px; color: #1f2937; }}
            .message-box {{ background-color: white; padding: 15px; border-left: 4px solid #3b82f6; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2 style="margin: 0;">New Contact Form Message</h2>
                <p style="margin: 5px 0 0 0;">From Delicious Bites Website</p>
            </div>
            
            <div class="content">
                <div class="field">
                    <div class="label">Name:</div>
                    <div class="value">{data.first_name} {data.last_name}</div>
                </div>
                
                <div class="field">
                    <div class="label">Email:</div>
                    <div class="value">{data.email}</div>
                </div>
                
                <div class="field">
                    <div class="label">Phone:</div>
                    <div class="value">{data.phone or 'Not provided'}</div>
                </div>
                
                <div class="field">
                    <div class="label">Subject:</div>
                    <div class="value">{data.subject}</div>
                </div>
                
                <div class="field">
                    <div class="label">Message:</div>
                    <div class="message-box">{data.message}</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    try:
        response = resend.Emails.send({
            "from": "Delicious Bites <onboarding@resend.dev>",
            "to": [email_to],
            "reply_to": data.email,
            "subject": f"Contact Form: {data.subject}",
            "html": html_content,
        })

        return {
            "status": "success",
            "message": "Your message has been sent successfully!",
            "id": response.get("id")
        }

    except Exception as e:
        print(f"Email error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send email. Please try again later."
        )