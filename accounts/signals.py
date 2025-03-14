from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import OtpToken
from django.core.mail import send_mail
from django.utils import timezone
import secrets
import string
from twilio.rest import Client

# Helper function to generate OTP
def generate_otp():
    """Generate a 6-digit OTP."""
    return ''.join(secrets.choice(string.digits) for _ in range(6))

# Helper function to format the phone number to E.164 format
def format_phone_number(phone_number):
    """Formats the phone number to E.164 format."""
    if phone_number:
        # Check if phone number starts with 0 (assume Tanzanian number here)
        if phone_number.startswith('0'):
            phone_number = '+255' + phone_number[1:]  # for Tanzanian numbers
        elif not phone_number.startswith('+'):
            phone_number = '+' + phone_number  # prepend '+' for international numbers
    return phone_number

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance, created, **kwargs):
    if created:
        # Skip for superusers
        if instance.is_superuser:
            return

        # Generate OTP and create OTP Token instance
        otp_code = generate_otp()
        otp_token = OtpToken.objects.create(
            user=instance,
            otp_code=otp_code,
            otp_expires_at=timezone.now() + timezone.timedelta(minutes=5)  # OTP expires in 5 minutes
        )

        # Deactivate the user until OTP is verified
        instance.is_active = False
        instance.save()

        # Send OTP via Email
        subject = "Email Verification"
        message = f"""
            Hi {instance.username},
            Here is your OTP: {otp_token.otp_code}
            It expires in 5 minutes. Please use the URL below to verify your account:
            http://127.0.0.1:8000/verify-email/{instance.username}
            
            Cheers,
            Your Website Team
        """
        sender_email = "iyumbusda@gmail.com"
        receiver_email = [instance.email]  # Ensure this is a list of email addresses

        # Send the email with OTP
        send_mail(
            subject,
            message,
            sender_email,
            receiver_email,
            fail_silently=False
        )

        # Send OTP via SMS using Twilio
        if instance.mobile_number:
            try:
                # Format the mobile number
                formatted_phone_number = format_phone_number(instance.mobile_number)

                # Initialize Twilio client
                client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)

                # Send OTP via SMS
                sms_message = client.messages.create(
                    body=f"Hi {instance.username}, your OTP is {otp_token.otp_code}. It expires in 5 minutes.",
                    from_=settings.TWILIO_PHONE_NUMBER,  # Your Twilio phone number
                    to=formatted_phone_number  # User's formatted phone number
                )
                print(f"OTP sent to {formatted_phone_number} with SID {sms_message.sid}")

            except Exception as e:
                print(f"Error sending OTP to mobile: {e}")
