from django import forms
from .models import Course

# Define choices for courses statically or dynamically from the model
class CourseSelectionForm(forms.Form):
    course = forms.ChoiceField(
        choices=Course.COURSE_CHOICES,
        label="Select Course"
    )
    level = forms.ChoiceField(
        choices=Course.LEVEL_CHOICES,
        label="Select Learning Level"
    )

# class CourseSelectionForm(forms.Form):
#     course = forms.ChoiceField(choices=Course.COURSE_CHOICES, label="Select Course")
#     level = forms.ChoiceField(choices=Course.LEVEL_CHOICES, label="Select Learning Level")