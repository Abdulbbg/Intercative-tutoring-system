from django.shortcuts import render, redirect
from .forms import CourseSelectionForm
from django.contrib import messages
from .models import UserCourse, QuizQuestion, CourseContent
import requests
from django.shortcuts import render, get_object_or_404
from .models import Course
from django.http import JsonResponse
from urllib.parse import urlencode
import re
from django.http import HttpResponseNotFound
import requests
from django.shortcuts import render
from .forms import CourseSelectionForm  # Import the form

from django.shortcuts import render, redirect
from django.http import HttpResponse
from urllib.parse import urlencode
import requests
import re

def course_selection_view(request):
    form = CourseSelectionForm()
    if request.method == 'POST':
        form = CourseSelectionForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            level = form.cleaned_data['level']

            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": (
                                    f"Generate a detailed, well-structured explanation for the course '{course}' at the "
                                    f"{level} level in 8 pages and provide full explanation of each page not outline full explanation"
                                )
                            }
                        ]
                    }
                ]
            }

            try:
                response = requests.post(
                    'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyD-5HePBxjbQDrP7gOlxn2ZfxbuwJQ2m68',
                    json=payload,
                    timeout=10
                )
                if response.status_code == 200:
                    content = response.json().get('candidates', [])[0]['content']['parts'][0]['text']
                else:
                    content = "Sorry, we couldn't generate the content at this time."
            except requests.exceptions.RequestException as e:
                content = f"Error contacting the Gemini API: {str(e)}"

            query_params = urlencode({'course_title': course, 'generated_content': content})
            return redirect(f'/course/course-content/?{query_params}')

    return render(request, 'course_selection.html', {'form': form})




def course_content_view(request):
    course_title = request.GET.get('course_title', 'Course Content')
    generated_content = request.GET.get('generated_content', 'No content available.')
    course_id = request.GET.get('course_id')

    cleaned_content = re.sub(r'[\*#]', '', generated_content)
    formatted_content = cleaned_content.replace('\n', '<br>')

    context = {
        'course_title': course_title,
        'generated_content': formatted_content,
        'course_id': course_id  # Pass course_id to the template
    }
    return render(request, 'course_content.html', context)



# def quiz_view(request, course_id):
#     questions = Question.objects.filter(course_id=course_id)

#     if request.method == 'POST':
#         score = 0
#         total = questions.count()

#         for question in questions:
#             selected_answer = request.POST.get(str(question.id))
#             if selected_answer == question.correct_answer:
#                 score += 1

#         percentage = (score / total) * 100
#         return HttpResponse(f"Your score is {score}/{total} ({percentage:.2f}%)")

#     return render(request, 'quiz.html', {'questions': questions})

