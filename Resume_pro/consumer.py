import json
import pika
import django
from sys import path
from os import environ
from fpdf import FPDF

# path.append('/home/john/Dev/SECTION/Likes/Likes/settings.py')  # Your path to settings.py file
path.append('D:/Interview Preparation/Revyz/Resume_pro/Resume_pro/settings.py')

environ.setdefault('DJANGO_SETTINGS_MODULE', 'Resume_pro.settings')
django.setup()

from resume.models import Candidate

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost', heartbeat=600, blocked_connection_timeout=300))
channel = connection.channel()
channel.queue_declare(queue='resume')


def create_resume(data):
    file_name = "D:/Resumes/Resume_{}_{}.pdf".format(data["name"], data["id"])
    pdf = FPDF()
    # Add a page
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", style="B", size=17)

    # create a cell
    pdf.cell(200, 10, txt=data["name"] + " Resume", ln=1, align='C')

    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Address: " + data["address"], ln=1, align='C')
    pdf.cell(200, 10, txt="Phone number: " + data["phone_number"], ln=1, align='C')
    pdf.cell(200, 10, txt="Email: " + data["email"], ln=1, align='C')
    pdf.cell(200, 10, txt="City name: " + data["city_name"], ln=1, align='C')
    pdf.cell(200, 10, txt="Tech skills: " + ", ".join(data["tech_skills"]), ln=1, align='C')

    pdf.output("Resume_{}_{}.pdf".format(data["name"], data["id"]))


def callback(ch, method, properties, body):
    print("Received in resume...")
    print(body)
    data = json.loads(body)
    print(data)

    if properties.content_type == 'candidate_created':
        candidate = Candidate.objects.create(
            # id=data['id'],
            name=data['name'],
            address=data['address'],
            phone_number=data['phone_number'],
            email=data['email'],
            city_name=data['city_name'],
            tech_skills=data['tech_skills'])
        candidate.save()

        create_resume(data)
        print("candidate created")


channel.basic_consume(queue='resume', on_message_callback=callback, auto_ack=True)
print("Started Consuming...")
channel.start_consuming()
