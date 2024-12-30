from email import encoders
from email.mime.base import MIMEBase
import os
from datetime import datetime
from pytz import timezone
import pytz
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv

load_dotenv()
mail_api_key = os.getenv("MAIL_API_KEY")

def mail_body(generation_details):
    body = f"""
    Hello,
    These are the details of the Blogs Posted at ReXplore: Science @ Fingertips.

    Date & Time: {get_current_time()}


    {generation_details}


    Regards,
    Nayan Kasturi (Raanna),
    Developer & Maintainer,
    ReXplore.
    """
    return body

def get_current_time():
    fmt = "%d-%m-%Y %H:%M:%S %Z%z"
    now_utc = datetime.now(timezone('UTC'))
    now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
    return now_asia.strftime(fmt)

def create_attachment(content, filename):
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(content)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename="{filename}"')
    return attachment

def send_email(generation_details):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = mail_api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    data = mail_body(generation_details)
    data_attchment = create_attachment(data.encode('utf-8'), "data.txt")

    subject = "New Blog Batch Published to ReXplore at " + get_current_time()
    sender = {"name": "Project Gatekeeper", "email": "projectgatekeeper@silerudaagartha.eu.org"}
    reply_to = {"name": "Project Gatekeeper", "email": "gatekeeper@raannakasturi.eu.org"}
    text_content = data
    attachments = [
        {"content": data_attchment.get_payload(), "name": data_attchment.get_filename()},
    ]
    to = [{"email": "raannakasturi@proton.me"}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, attachment=attachments, text_content=text_content, sender=sender, subject=subject)
    try:
        api_instance.send_transac_email(send_smtp_email)
        print("Email Sent")
        return True
    except ApiException as e:
        print("Can't send email")
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        return False
