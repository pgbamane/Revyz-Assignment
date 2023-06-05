from .views import CandidateListView
from django.urls import path

urlpatterns = [
    path('candidate/', CandidateListView.as_view()),
    path('candidate/<bulk>/', CandidateListView.as_view()),
]
