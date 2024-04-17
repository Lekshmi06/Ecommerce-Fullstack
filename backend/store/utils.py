import secrets
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Otp

def generate_and_save_otp(user):
    otp_value = str(secrets.randbelow(1000000)).zfill(6) 
    print(otp_value)
    otp_instance = Otp.objects.create(user=user, otp=otp_value)
    return otp_instance

def send_otp_email(user_email, otp_instance):
    subject = 'OTP Verification for Registration'
    from_email = 'lekshmi.anilkumar06@gmail.com'  
    recipient_list = [user_email]
    html_content = render_to_string('otp_email_template.html', {'otp_instance': otp_instance})
    text_content = strip_tags(html_content)   
    msg = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()