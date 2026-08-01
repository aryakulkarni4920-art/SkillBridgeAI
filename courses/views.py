from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dashboard.models import Career
from .models import Course


@login_required
def recommended_courses(request):

    career = Career.objects.filter(
        user=request.user
    ).first()

    courses = []

    if career:

        courses = Course.objects.filter(
            career__iexact=career.career_name
        )

    return render(
        request,
        "courses/recommended_courses.html",
        {
            "career": career,
            "courses": courses,
        }
    )