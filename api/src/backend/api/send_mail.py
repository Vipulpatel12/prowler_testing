#!/usr/bin/env python3
import os
import smtplib
import sys
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


#
# def create_invitation_email(recipient_email, role, invitation_id, base_url="http://localhost:3000"):
#     """
#     Create an HTML email for the invitation.
#
#     Args:
#         recipient_email (str): Recipient's email address.
#         role (str): Role assigned in the invitation.
#         invitation_id (str): Unique invitation token.
#         base_url (str): Base URL of the application.
#
#     Returns:
#         MIMEMultipart: Email message object.
#     """
#     invitation_link = f"{base_url}sign-up?invitation_token={invitation_id}&email={recipient_email}&company=york.ie&user_name={recipient_email.split('@')[0]}"
#
#     message = MIMEMultipart("alternative")
#     message["Subject"] = "You've Been Invited!"
#     message["From"] = "vipulp@york.ie"
#     message["To"] = recipient_email
#
#     html_content = f"""
#     <html>
#       <body>
#         <h1>You've Been Invited!</h1>
#         <p>Hello,</p>
#         <p>You have been invited to join our platform with the role of <strong>{role}</strong>.</p>
#         <p><a href="{invitation_link}" style="background:blue; color:white; padding:10px; text-decoration:none;">Accept Invitation</a></p>
#         <p>If the button does not work, copy and paste this link in your browser:</p>
#         <p>{invitation_link}</p>
#         <p>This is an automated email. Please do not reply.</p>
#         <p>Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
#       </body>
#     </html>
#     """
#
#     text_content = f"""
#     You've Been Invited!
#
#     Hello,
#
#     You have been invited to join our platform with the role of {role}.
#
#     To accept your invitation, visit:
#     {invitation_link}
#
#     If you didn't request this invitation, please ignore this email.
#
#     Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#     """
#
#     message.attach(MIMEText(text_content, "plain"))
#     message.attach(MIMEText(html_content, "html"))
#
#     return message

from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def create_invitation_email(recipient_email, invitation_id, base_url="http://localhost:3000"):
    """
    Create an HTML email for the invitation with an expiry date.

    Args:
        recipient_email (str): Recipient's email address.
        invitation_id (str): Unique invitation token.
        base_url (str): Base URL of the application.

    Returns:
        MIMEMultipart: Email message object.
    """
    expiry_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    invitation_link = f"{base_url}/sign-up?invitation_token={invitation_id}&email={recipient_email}&company=prowler&user_name={recipient_email.split('@')[0]}"

    message = MIMEMultipart("alternative")
    message["Subject"] = "You're Invited to Join Prowler!"
    message["From"] = "vipulp@york.ie"
    message["To"] = recipient_email

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #0044cc;">You're Invited to Join Prowler!</h2>
        <p>Hello, {recipient_email.split('@')[0]}</p>
        <p>You have been invited to join Prowler.</p>
        <p>Please click the button below to accept your invitation:</p>
        <p>
          <a href="{invitation_link}" 
             style="background-color: #007BFF; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
             Accept Invitation
          </a>
        </p>
        <p><strong>Note:</strong> This invitation will expire on <strong>{expiry_date}</strong>.</p>
        <hr>
        <p style="font-size: 12px; color: #777;">This is an automated email. Please do not reply.</p>
        <p style="font-size: 12px; color: #777;">Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
      </body>
    </html>
    """

    text_content = f"""
    You're Invited to Join Prowler!

    Hello,

    You have been invited to join Prowler.

    To accept your invitation, click the link below:
    {invitation_link}

    Note: This invitation will expire on {expiry_date}.

    If you didn't request this invitation, please ignore this email.

    Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """

    message.attach(MIMEText(text_content, "plain"))
    message.attach(MIMEText(html_content, "html"))

    return message

def send_email(message):
    """
    Sends an email using SMTP.

    Args:
        message (MIMEMultipart): The email message object.

    Returns:
        bool: True if email sent successfully, False otherwise.
    """
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER", "vipulp@york.ie")
    smtp_password = os.environ.get("SMTP_PASSWORD", "shfh xiwz mctb eahi")  # Set in env variables
    smtp_use_tls = os.environ.get("SMTP_SECURE", "true").lower() == "true"

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            if smtp_use_tls:
                server.starttls()

            if smtp_user and smtp_password:
                server.login(smtp_user, smtp_password)

            server.send_message(message)

        print(f"✅ Email sent successfully to {message['To']}")
        return True
    except Exception as e:
        print(f"❌ Error sending email: {e}", file=sys.stderr)
        return False


def send_invitation_email(serializer_data, base_url="http://localhost:3000"):
    """
    Extracts data from serializer and sends an invitation email.

    Args:
        serializer_data (dict): Data containing email, token, roles, etc.
        base_url (str): Base URL for the application.

    Returns:
        bool: True if email sent successfully, False otherwise.
    """
    try:
        recipient_email = serializer_data.get("email")
        invitation_id = serializer_data.get("token")
        roles = serializer_data.get("roles", [])

        role = roles[0].get("id") if roles else "N/A"

        if not recipient_email or not invitation_id:
            print("❌ Error: Missing required invitation details.", file=sys.stderr)
            return False

        message = create_invitation_email(recipient_email, invitation_id, base_url)
        return send_email(message)

    except Exception as e:
        print(f"❌ Error processing email invitation: {e}", file=sys.stderr)
        return False


def sending_mail(serializer):
    """Main function to send an email."""
    try:
        print('serializerserializer>>>',serializer)

        success = send_invitation_email(serializer, "http://localhost:3000/")
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}", file=sys.stderr)
        return 1


