from django.db import models
from userauth.models import CustomUser

User = CustomUser

from django.db import models

class Course(models.Model):
    COURSE_CHOICES = [
        ('COM 311: OPERATING SYSTEM I', 'OPERATING SYSTEM I'),
        ('COM 312: DATABASE DESIGN I', 'DATABASE DESIGN I'),
        ('COM 313: COMPUTER PROGRAMMING USING C++', 'COMPUTER PROGRAMMING USING C++'),
        ('COM 314: COMPUTER ARCHITECTURE', 'COMPUTER ARCHITECTURE'),
        ('COM 315: PYTHON PROGRAMMING LANGUAGE', 'PYTHON PROGRAMMING LANGUAGE'),
        ('STA 311: STATISTICAL THEORY', 'STATISTICAL THEORY'),
        ('STA 314: OPERATION RESEARCH I', 'OPERATION RESEARCH I'),
        ('GNS 301: USE OF ENGLISH III', 'USE OF ENGLISH III'),
        ('COM 321: OPERATING SYSTEM II', 'OPERATING SYSTEM II'),
        ('COM 322: DATABASE DESIGN II', 'DATABASE DESIGN II'),
        ('COM 323: ASSEMBLY LANGUAGE', 'ASSEMBLY LANGUAGE'),
        ('COM 324: INTRODUCTION', 'INTRODUCTION'),
    ]

    name = models.CharField(max_length=100, choices=COURSE_CHOICES)
    description = models.TextField()
    
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.level})"




class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=Course.LEVEL_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.course.name} ({self.level})"



       