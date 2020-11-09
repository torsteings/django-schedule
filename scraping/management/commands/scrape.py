from django.core.management.base import BaseCommand

from jobs.settings import EMAIL_HOST_PASSWORD
from jobs.settings import EMAIL_HOST_USER

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class Command(BaseCommand):
    # define logic of command
    def handle(self, *args, **options):

        # Set email header information.
        sender = "CTbirds AS"
        username = EMAIL_HOST_USER
        password = EMAIL_HOST_PASSWORD
        host = "smtp.gmail.com"
        port = 587 #transport level security

        recipient = "torstein.skarsgard@gmail.com"

        body = "var3"

        # Assemble the message.
        msg = MIMEMultipart()
        msg.add_header("From", sender)
        msg.add_header("To", recipient)
        msg.add_header("Subject", "Dagens aksje")
        msg.attach(MIMEText(body, "plain"))

        # Send the message.
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(username, password)
        server.send_message(msg)
        server.quit()

        self.stdout.write( 'job complete' )
