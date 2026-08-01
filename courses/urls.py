from django.urls import path
from . import views

urlpatterns = [
    path(
        "",
        views.recommended_courses,
        name="recommended_courses"
    ),
]