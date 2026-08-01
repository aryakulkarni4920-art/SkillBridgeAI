from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('career/', views.choose_career, name='choose_career'),
   path(
    'save-career/<int:career_id>/',
    views.save_career,
    name='save_career'
),
    path(
    'download-report/',
    views.download_report,
    name='download_report'
),
path(
    'chatbot/',
    views.chatbot,
    name='chatbot'
),
path(
    "save-custom-career/",
    views.save_custom_career,
    name="save_custom_career",
),
]