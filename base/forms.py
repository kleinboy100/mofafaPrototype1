from django.forms import ModelForm
from .models import Announcement, Marks, Learner, Subject, Comment, Profile, Attendance, Week, UserProfile
from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError
from django.db.models import Q


class writeAnnouncement(ModelForm):
    class Meta:
        model = Announcement
        fields = ['department', 'title', 'description']
        



class MarksForm(forms.ModelForm):
    learner = forms.ModelChoiceField(queryset=Learner.objects.all())
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())

    task1 = forms.IntegerField(max_value=100, min_value=0, required=False) 
    task2 = forms.IntegerField(max_value=100, min_value=0, required=False)
    task3 = forms.IntegerField(max_value=100, min_value=0, required=False)
    term = forms.IntegerField(max_value=100, min_value=0, required=False)
    
    task4 = forms.IntegerField(max_value=100, min_value=0, required=False) 
    task5 = forms.IntegerField(max_value=100, min_value=0, required=False)
    task6 = forms.IntegerField(max_value=100, min_value=0, required=False)
    term2 = forms.IntegerField(max_value=100, min_value=0, required=False)
    
    
    task7 = forms.IntegerField(max_value=100, min_value=0, required=False) 
    task8 = forms.IntegerField(max_value=100, min_value=0, required=False)
    task9 = forms.IntegerField(max_value=100, min_value=0, required=False)
    term3 = forms.IntegerField(max_value=100, min_value=0, required=False)
    
    task10 = forms.IntegerField(max_value=100, min_value=0, required=False) 
    task11 = forms.IntegerField(max_value=100, min_value=0, required=False)
    task12 = forms.IntegerField(max_value=100, min_value=0, required=False)
    term4 = forms.IntegerField(max_value=100, min_value=0, required=False)



    class Meta:
        model = Marks
        fields = ['learner', 'subject', 'task1', 'task2', 'task3' , 'task4', 'task5', 'task6' , 'task7', 'task8', 'task9' , 'task10', 'task11', 'task12']

    def clean(self):
        cleaned_data = super().clean()
        learner = cleaned_data.get('learner')
        subject = cleaned_data.get('subject')

        # Check if a Marks instance already exists for the learner and subject
        if Marks.objects.filter(learner=learner, subject=subject).exists():
            raise forms.ValidationError("Marks already exist for this learner and subject combination.")

        return cleaned_data
    
    
class MessageForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [ 'body'] 
        
        
class AttendanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        classroom = kwargs.pop('classroom')
        super().__init__(*args, **kwargs)
        # Populate the form with learners assigned to the classroom
        self.fields['learner'].queryset = Learner.objects.filter(classroomName=classroom)

    class Meta:
        model = Attendance
        fields = ['weeks', 'classroom', 'learner', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        # Set some fields as optional
        widgets = {
            'weeks': forms.Select(attrs={'class': 'form-control'}),
            'monday': forms.Select(attrs={'class': 'form-control'}),
            'tuesday': forms.Select(attrs={'class': 'form-control'}),
            'wednesday': forms.Select(attrs={'class': 'form-control'}),
            'thursday': forms.Select(attrs={'class': 'form-control'}),
            'friday': forms.Select(attrs={'class': 'form-control'})
        }

        
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']
        
        
class SubjectForm(ModelForm):
    class Meta:
        model = Marks
        fields = ['learner','task1', 'task2', 'task3', 'term']
        

    
