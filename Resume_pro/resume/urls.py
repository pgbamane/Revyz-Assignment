from django.urls import path, include
from . import views

urlpatterns = [
    path('candidate/', views.CandidateListView.as_view())
]
