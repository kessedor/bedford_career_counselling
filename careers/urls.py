from django.urls import path
from . import views
from .views import career_list, AICounselorView

app_name = 'careers'  # This defines the namespace

urlpatterns = [
    path('', views.career_list, name='career_list'),
    path('ai-counselor/', AICounselorView.as_view(), name='ai_counselor'),
]