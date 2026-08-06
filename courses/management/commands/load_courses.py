from django.core.management.base import BaseCommand
from courses.models import Course

class Command(BaseCommand):
    help = "Load default courses"

    def handle(self, *args, **kwargs):

        Course.objects.all().delete()

        courses = [

            {
                "career":"AI Engineer",
                "title":"Machine Learning Specialization",
                "platform":"Coursera",
                "level":"Intermediate",
                "link":"https://www.coursera.org/specializations/machine-learning-introduction"
            },

            {
                "career":"AI Engineer",
                "title":"Python for Everybody",
                "platform":"Coursera",
                "level":"Beginner",
                "link":"https://www.coursera.org/specializations/python"
            },

            {
                "career":"AI Engineer",
                "title":"Deep Learning",
                "platform":"Coursera",
                "level":"Advanced",
                "link":"https://www.coursera.org/specializations/deep-learning"
            },

            {
                "career":"Data Analyst",
                "title":"Google Data Analytics",
                "platform":"Coursera",
                "level":"Beginner",
                "link":"https://www.coursera.org/professional-certificates/google-data-analytics"
            },

            {
                "career":"Data Analyst",
                "title":"Excel Skills",
                "platform":"Coursera",
                "level":"Beginner",
                "link":"https://www.coursera.org/specializations/excel"
            },

            {
                "career":"Web Developer",
                "title":"Responsive Web Design",
                "platform":"freeCodeCamp",
                "level":"Beginner",
                "link":"https://www.freecodecamp.org/learn"
            },

            {
                "career":"Web Developer",
                "title":"JavaScript Algorithms",
                "platform":"freeCodeCamp",
                "level":"Intermediate",
                "link":"https://www.freecodecamp.org/learn"
            },

            {
                "career":"Python Developer",
                "title":"Python for Everybody",
                "platform":"Coursera",
                "level":"Beginner",
                "link":"https://www.coursera.org/specializations/python"
            },

            {
                "career":"Java Developer",
                "title":"Java Programming",
                "platform":"Coursera",
                "level":"Beginner",
                "link":"https://www.coursera.org/specializations/java-programming"
            },

            {
                "career":"Cloud Engineer",
                "title":"Google Cloud Fundamentals",
                "platform":"Google Cloud",
                "level":"Beginner",
                "link":"https://www.cloudskillsboost.google/"
            },

            {
                "career":"Cybersecurity",
                "title":"Google Cybersecurity",
                "platform":"Coursera",
                "level":"Beginner",
                "link":"https://www.coursera.org/professional-certificates/google-cybersecurity"
            },

            {
                "career":"Full Stack Developer",
                "title":"The Odin Project",
                "platform":"The Odin Project",
                "level":"Beginner",
                "link":"https://www.theodinproject.com/"
            }

        ]

        for course in courses:
            Course.objects.create(**course)

        self.stdout.write(self.style.SUCCESS("Courses Loaded Successfully"))