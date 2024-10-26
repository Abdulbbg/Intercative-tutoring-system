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
from django.views.decorators.csrf import csrf_exempt
import json
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
                    timeout=30
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



def clean_content(content):
    """Remove '*' and '#' from the content using regex."""
    cleaned_content = re.sub(r'[*#]', '', content)
    return cleaned_content.strip()

def split_into_paragraphs(content):
    """Split the cleaned content into paragraphs using double newlines or sentence breaks."""
    paragraphs = re.split(r'\n\n+|(?<=[.!?])\s{2,}', content)  # Split by double newlines or sentence ends
    return [p.strip() for p in paragraphs if p.strip()]  # Remove empty or extra spaces

def course_content_view(request):
    course_title = request.GET.get('course_title', 'Course Content')
    generated_content = request.GET.get('generated_content', 'No content available.')


    # Clean the course title and content
    course_title = clean_content(course_title)
    cleaned_content = clean_content(generated_content)

    # Split content into paragraphs
    content_paragraphs = split_into_paragraphs(cleaned_content)

    # Payload to generate quiz questions using Gemini API
    quiz_payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Generate 5 multiple-choice questions with 4 options each and i will give you the answers to evaluate based on the course do not inlude the answers '{course_title}': {generated_content}"
                    }
                ]
            }
        ]
    }

    try:
        quiz_response = requests.post(
            'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyD-5HePBxjbQDrP7gOlxn2ZfxbuwJQ2m68',
            json=quiz_payload, timeout=10
        )
        if quiz_response.status_code == 200:
            raw_quiz_data = quiz_response.json().get('candidates', [])[0]['content']['parts'][0]['text']
            quiz_questions = parse_quiz_data(raw_quiz_data)  # Parse quiz data
            request.session['quiz_questions'] = quiz_questions
        else:
            quiz_questions = []
    except requests.exceptions.RequestException:
        quiz_questions = []

    context = {
        'course_title': course_title,
        'content_paragraphs': content_paragraphs,  # Send paragraphs to the template
        'quiz_questions': quiz_questions,
    }
    return render(request, 'course_content.html', context)

def parse_quiz_data(raw_data):
    """
    Parse Gemini-generated quiz data into questions and options.
    Expected input format:
      1. Question?
         A. Option 1
         B. Option 2
         C. Option 3
         D. Option 4
    """
    quiz = []
    cleaned_data = clean_content(raw_data)

    # Split the quiz data into individual questions using double newlines
    questions = re.split(r'\n\n+', cleaned_data)

    for question in questions:
        lines = question.strip().split('\n')
        question_text = lines[0]
        options = [line[3:].strip() for line in lines[1:]]  # Extract options after "A. ", "B. ", etc.
        quiz.append({'question': question_text, 'options': options})

    return quiz




@csrf_exempt
def submit_quiz(request):
    if request.method == 'POST':
        try:
            # Parse the user's answers from the request body
            user_answers = json.loads(request.body)

            # Retrieve original questions from session
            original_questions = request.session.get('quiz_questions', [])

            # Ensure the questions and answers are lists, not sets
            original_questions = list(original_questions)
            user_answers = {k: list(v) if isinstance(v, set) else v for k, v in user_answers.items()}

            # Construct the evaluation payload
            evaluation_payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": (
                                    f"Based on the following questions and answers, provide a percentage score only:\n\n"
                                    f"Questions: {original_questions}\n\n"
                                    f"User Answers: {user_answers}"
                                )
                            }
                        ]
                    }
                ]
            }

            # Check if the payload is serializable (debug step)
            # print(json.dumps(evaluation_payload))  # This will raise an error if the payload isn't valid

            # Send the POST request
            response = requests.post(
                'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyD-5HePBxjbQDrP7gOlxn2ZfxbuwJQ2m68',
                json=evaluation_payload,
                timeout=10
            )

            if response.status_code == 200:
                score = response.json().get('candidates', [])[0]['content']['parts'][0]['text']
            else:
                score = "Failed to evaluate the answers."

        except requests.exceptions.RequestException as e:
            score = f"Error: {str(e)}"
        except (TypeError, ValueError) as e:
            score = f"JSON Serialization Error: {str(e)}"

        return JsonResponse({'score': score})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
