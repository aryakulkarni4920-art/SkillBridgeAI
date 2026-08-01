import json
import fitz

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Resume
from dashboard.models import Career
from ai.gemini import analyze_resume


@login_required
def upload_resume(request):

    if request.method == "POST":

        resume_file = request.FILES.get("resume")

        if not resume_file:
            messages.error(request, "Please select a resume.")
            return redirect("upload_resume")

        # Save resume
        resume = Resume.objects.create(
            user=request.user,
            resume=resume_file
        )

        # Extract text from PDF
        try:
            pdf = fitz.open(resume.resume.path)

            extracted_text = ""

            for page in pdf:
                extracted_text += page.get_text()

            pdf.close()

            resume.extracted_text = extracted_text
            resume.save()

        except Exception as e:
            print(e)
            messages.error(request, "Please upload a valid PDF file.")
            return redirect("upload_resume")

        # Get selected career
        career = Career.objects.filter(user=request.user).first()

        if not career:
            messages.warning(
                request,
                "Please select a career before uploading your resume."
            )
            return redirect("choose_career")

        # AI Analysis
        try:

            ai_result = analyze_resume(
                career.career_name,
                extracted_text
            )

            # Convert JSON string to Python object
            try:
                ai_json = json.loads(ai_result)

                # Save formatted JSON
                resume.ai_analysis = json.dumps(
                    ai_json,
                    indent=4
                )

            except json.JSONDecodeError:
                # Save raw response if it isn't valid JSON
                resume.ai_analysis = ai_result

            resume.save()

            print("\n========== GEMINI RESPONSE ==========\n")
            print(resume.ai_analysis)
            print("\n=====================================\n")

            messages.success(
                request,
                "Resume analysed successfully!"
            )

        except Exception as e:

            print("\n========== GEMINI ERROR ==========\n")
            print(e)
            print("\n==================================\n")

            messages.warning(
                request,
                "Resume uploaded successfully, but AI analysis is temporarily unavailable. Please try again later."
            )

        return redirect("dashboard")

    return render(request, "upload_resume.html")
from django.contrib.auth.decorators import login_required


@login_required
def resume_history(request):

    resumes = Resume.objects.filter(
        user=request.user
    ).order_by("-uploaded_at")

    return render(
        request,
        "resume_history.html",
        {
            "resumes": resumes
        }
    )
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def delete_resume(request, resume_id):

    resume = get_object_or_404(
        Resume,
        id=resume_id,
        user=request.user
    )

    resume.resume.delete(save=False)

    resume.delete()

    return redirect("resume_history")