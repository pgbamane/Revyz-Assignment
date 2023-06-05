from django.db import models

# Create your models here.
# Create your models here.
from django.db import models
from multiselectfield import MultiSelectField

TECH_CHOICES = (('python', 'Python'),
                ('java', 'Java'),
                ('ruby', 'Ruby'),
                ('docker', 'Docker'),
                ('node', 'Node'),
                ('js', 'JS'))


# Create your models here.
class Candidate(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()
    city_name = models.CharField(max_length=30)
    tech_skills = MultiSelectField(choices=TECH_CHOICES, max_choices=6, max_length=50)
    # experience_in_years = models.FloatField(max_length=10)
