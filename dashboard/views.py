from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from ai.gemini import analyze_resume
from .models import Career, CareerCatalog
from resumes.models import Resume
from courses.models import Course

import json
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
from courses.models import Course



@login_required
def dashboard(request):

    career = Career.objects.filter(
        user=request.user
    ).first()

    recommended_courses = []

    if career:
        recommended_courses = Course.objects.filter(
            career__iexact=career.career_name
        )

    resume = Resume.objects.filter(
        user=request.user
    ).order_by("-uploaded_at").first()

    analysis = None

    if resume and resume.ai_analysis:

        try:
            analysis = json.loads(resume.ai_analysis)

        except json.JSONDecodeError:
            analysis = None

    # Calculate Learning Progress
    progress = 0

    if analysis:

        total_skills = (
            len(analysis["existing_skills"])
            + len(analysis["missing_skills"])
        )

        if total_skills > 0:

            progress = int(
                (len(analysis["existing_skills"]) / total_skills) * 100
            )

    context = {

        "career": career,

        "resume": resume,

        "analysis": analysis,

        "recommended_courses": recommended_courses,

        "progress": progress,

    }

    return render(
        request,
        "dashboard.html",
        context,
    )

@login_required
def choose_career(request):

    careers = CareerCatalog.objects.all().order_by("career_name")

    return render(
        request,
        "choose_career.html",
        {
            "careers": careers,
        }
    )

@login_required
def save_career(request, career_id):

    selected = CareerCatalog.objects.get(id=career_id)

    Career.objects.update_or_create(
        user=request.user,
        defaults={
            "career_name": selected.career_name
        }
    )

    resume = Resume.objects.filter(
        user=request.user
    ).order_by("-uploaded_at").first()

    if resume and resume.extracted_text:

        try:

            ai_result = analyze_resume(
                selected.career_name,
                resume.extracted_text
            )
            print("================================")
            print("Career Changed To:", selected.career_name)
            print("Re-analyzing Resume...")
            print("================================")
            print("Selected Career:", selected.career_name)
            print("AI Result:")
            print(ai_result)
            try:

                ai_json = json.loads(ai_result)

                resume.ai_analysis = json.dumps(
                    ai_json,
                    indent=4
                )

            except json.JSONDecodeError:

                resume.ai_analysis = ai_result

            resume.save()
            print("AI Analysis Saved Successfully")
        except Exception as e:

            print(e)

    return redirect("dashboard")
@login_required
def download_report(request):

    resume = Resume.objects.filter(
        user=request.user
    ).order_by("-uploaded_at").first()

    if not resume:
        return HttpResponse("No resume found.")

    analysis = json.loads(resume.ai_analysis)

    response = HttpResponse(
        content_type="application/pdf"
    )

    response["Content-Disposition"] = 'attachment; filename="SkillBridge_Report.pdf"'

    p = canvas.Canvas(response)

    y = 800

    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, y, "SkillBridge AI Report")

    y -= 40

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"User: {request.user.username}")

    y -= 25
    p.drawString(50, y, f"Match Score: {analysis['match_score']}%")

    y -= 40
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Existing Skills")

    y -= 25
    p.setFont("Helvetica", 12)

    for skill in analysis["existing_skills"]:
        p.drawString(70, y, "• " + skill)
        y -= 20

    y -= 20

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Missing Skills")

    y -= 25
    p.setFont("Helvetica", 12)

    for skill in analysis["missing_skills"]:
        p.drawString(70, y, "• " + skill)
        y -= 20

    y -= 20

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Learning Roadmap")

    y -= 25
    p.setFont("Helvetica", 12)

    for item in analysis["roadmap"]:
        p.drawString(70, y, "• " + item)
        y -= 20

    y -= 20

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Recommended Courses")

    y -= 25
    p.setFont("Helvetica", 12)

    for course in analysis["courses"]:
        p.drawString(70, y, "• " + course)
        y -= 20

    p.save()

    return response


@login_required
def chatbot(request):

    answer = ""

    if request.method == "POST":

        question = request.POST.get("question")

        prompt = f"""
You are SkillBridge AI Career Assistant.

Answer the user's career-related question clearly and professionally.

Question:
{question}
"""

        try:

            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt,
            )

            answer = response.text

        except Exception as e:

            answer = str(e)

    return render(
        request,
        "chatbot.html",
        {
            "answer": answer
        }
    )
from django.contrib import messages

@login_required
def save_custom_career(request):

    if request.method == "POST":

        career_name = request.POST.get("career_name", "").strip()

        career = CareerCatalog.objects.filter(
            career_name__iexact=career_name
        ).first()

        if career:

            Career.objects.update_or_create(
                user=request.user,
                defaults={
                    "career_name": career.career_name
                }
            )

            messages.success(
                request,
                "Career selected successfully!"
            )

            return redirect("dashboard")

        else:

            messages.error(
                request,
                "Please select a valid career from the suggestions."
            )

            return redirect("choose_career")

    return redirect("choose_career")