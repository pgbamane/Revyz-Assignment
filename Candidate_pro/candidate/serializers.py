from rest_framework.serializers import ModelSerializer
from .models import Candidate
from rest_framework import fields
from .models import TECH_CHOICES


class CandidateSerializer(ModelSerializer):
    tech_skills = fields.MultipleChoiceField(choices=TECH_CHOICES)

    class Meta:
        model = Candidate
        fields = "__all__"
