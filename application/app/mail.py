from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import cStringIO
import smtplib
import json
import os


basedir = os.path.abspath(os.path.dirname(__file__))


def send_mail(receiver, pic):

    with open(os.path.join(basedir, 'smtp-credentials.json')) as data_file:
        data = json.load(data_file)

    msg = MIMEMultipart()
    msg['Subject'] = str("Photo Mosaic With Github !")
    msg['From'] = data['user']
    msg['To'] = receiver

    msg.preamble = 'Multipart massage.\n'

    memf = cStringIO.StringIO()
    pic.save(memf, "JPEG")
    image = MIMEImage(memf.getvalue(), name=("mosaic.jpeg"))
    part = MIMEText(
                    "Hi, \nHere is your picture ! \
                    \nHope you enjoy it \nCheers :)")
    image.add_header('Content-ID', '<mosaic.jpeg>')
    msg.attach(part)
    msg.attach(image)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(data['user'], data['oops'])
        server.sendmail(msg['From'], receiver, msg.as_string())
        server.quit()
        print('Successfully sent email')
    except Exception:
        print('Error: unable to send email')
