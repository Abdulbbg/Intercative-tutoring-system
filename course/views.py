from django.shortcuts import render, redirect
from .forms import CourseSelectionForm
from django.contrib import messages
from .models import UserCourse
import requests
from django.shortcuts import render, get_object_or_404
from .models import Course
from django.http import JsonResponse
from urllib.parse import urlencode
import re
import requests
from django.shortcuts import render
from .forms import CourseSelectionForm  # Import the form

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
                            {"text": f"explain fully {course} a beginner {level} level."}
                        ]
                    }
                ]
            }

            try:
                response = requests.post(
                    'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyAOo9OJ8nVMRqMbSVeS7iMhzR6-ti-r3ZQ',
                    json=payload
                )
                print("Status Code:", response.status_code)
                print("Response:", response.json())
                
                if response.status_code == 200:
                    generated_content = response.json().get('candidates')[0]['content']['parts'][0]['text']
                else:
                    generated_content = "Sorry, we couldn't generate the content at this time."
            except Exception as e:
                generated_content = f"Error contacting the Gemini API: {e}"

            # Use urlencode to pass data as query parameters
            query_params = urlencode({'course_title': course, 'generated_content': generated_content})
            return redirect(f'/course/course-content/?{query_params}')

    return render(request, 'course_selection.html', {'form': form})



def course_content_view(request):
    # Get course title and generated content from query parameters or use defaults
    course_title = request.GET.get('course_title', 'Course Content')
    generated_content = request.GET.get('generated_content', 'No content available.')

    # Remove asterisks (*) and hashtags (#) from the content
    cleaned_content = re.sub(r'[\*#]', '', generated_content)

    # Render the cleaned content in the template
    return render(request, 'course_content.html', {
        'course_title': course_title,
        'generated_content': cleaned_content  # Use the cleaned content
    })



# def course_selection_view(request):
#     if request.method == 'POST':
#         form = CourseSelectionForm(request.POST)
#         if form.is_valid():
#             course_name = form.cleaned_data['course']
#             level = form.cleaned_data['level']

#             # Get the Course instance from the course name
#             try:
#                 course = Course.objects.get(name=course_name)
#             except Course.DoesNotExist:
#                 form.add_error('course', 'Selected course does not exist.')
#                 return render(request, 'course_selection.html', {'form': form})

#             # Create the UserCourse instance with the actual Course object
#             UserCourse.objects.create(user=request.user, course=course, level=level)
#             return redirect('success_page')  # Replace with your actual success page
#     else:
#         form = CourseSelectionForm()

#     return render(request, 'course_selection.html', {'form': form})


# Replace with actual API URL and authentication details if necessary
# GEMINI_API_URL = "https://api.gemini.com/courses/content"  # Example URL
# GEMINI_API_KEY = "your_api_key_here"

# def fetch_gemini_content(course_name, level):
#     headers = {
#         'Authorization': f'Bearer {GEMINI_API_KEY}',
#     }
#     params = {
#         'course': course_name,
#         'level': level
#     }
#     response = requests.get(GEMINI_API_URL, headers=headers, params=params)
    
#     if response.status_code == 200:
#         return response.json()  # Assuming the response is in JSON format
#     return None

# def course_content_view(request, course_id):
#     # Fetch the course info based on the course_id
#     course = get_object_or_404(Course, id=course_id)
    
#     # Assume user has selected a level already, for demo let's say it's 'beginner'
#     selected_level = 'beginner'  # In reality, this will come from the user's selection
    
#     # Fetch the content from the Gemini API based on course name and level
#     content_data = fetch_gemini_content(course.name, selected_level)
    
#     context = {
#         'course': course,
#         'content_data': content_data,
#     }

#     return render(request, 'course_content.html', context)