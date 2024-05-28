from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_email_to_admins(subject, context, template):

  try:
    email_template_name = f'email/{template}'
    email_message = render_to_string(email_template_name, context)
    admin_emails = [admin_email for _, admin_email in settings.ADMINS]

    send_mail(
      subject,
      '',
      settings.EMAIL_HOST_USER,
      admin_emails,
      fail_silently=False,
      html_message=email_message
    )

    logger.info(f"Email sent successfully. subject: {subject}, context: {str(context)}")

  except Exception as e:
    # Log the exception
    logger.error(f"Failed to send email. error: {str(e)}, subject: {subject}, context: {str(context)}")
