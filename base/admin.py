from django.contrib import admin

# Register your models here.
from .models import Announcement, Department, Comment, Subject, Learner, Grade, Classroom, Marks, Week , UserProfile,Profile, Attendance

admin.site.register(Announcement)
admin.site.register(Department)
admin.site.register(Comment)
admin.site.register(Subject)
admin.site.register(Learner)
admin.site.register(Grade)
admin.site.register(Classroom)
admin.site.register(Marks)
admin.site.register(UserProfile)
admin.site.register(Profile)
admin.site.register(Attendance)
admin.site.register(Week)

