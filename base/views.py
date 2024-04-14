from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Announcement, Learner, Subject, Grade, Classroom, User, Marks,Message , Week,Department, UserProfile, Comment, Profile, Attendance
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import writeAnnouncement, MarksForm, SubjectForm, ProfilePictureForm, AttendanceForm
from django.db.models import Prefetch





def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        username =request.POST.get('username')
        password =request.POST.get('password')
        
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!')
    
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')
    
    
    context = {'page':page}
    return render(request, 'base/login_register.html', context)





def logoutUser(request):

    logout(request)
    return redirect('home')




def registerPage(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in. Congats')
            # Redirect to the login page or any other page as needed
            return redirect('login')  # Assuming you have a named URL pattern for the login page
    context = {'form': form}
    return render(request, 'base/login_register.html', context)

def inbox(request):
    # Fetch messages for the authenticated user (receiver)
    messages = Message.objects.filter(recipient=request.user)

    return render(request, 'base/inbox.html', {'messages': messages})

def teacher_attendance_list(request):
    attendances = Attendance.objects.all()
    learners = Learner.objects.all()
    user_profile = request.user.userprofile
    assigned_classroom = user_profile.assigned_classroom
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST, classroom=assigned_classroom)  # Pass assigned classroom to the form
        if form.is_valid():
            form.save()
            return redirect('teacher_attendance_list')  # Redirect to the same page after saving
    else:
        # Fetch attendance records for the teacher's assigned classroom
        if assigned_classroom:
            attendances = Attendance.objects.filter(classroom=assigned_classroom)
        else:
            attendances = []

        # Pass the assigned classroom to the form initialization
        form = AttendanceForm(classroom=assigned_classroom)

    return render(request, 'base/teacher_attendance_list.html', {'attendances': attendances, 'form': form})

def mark_attendance(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    if user_profile.assigned_classroom:
        classroom = user_profile.assigned_classroom

        form = AttendanceForm(request.POST or None, classroom=classroom)
        if request.method == 'POST':
            form = AttendanceForm(request.POST, classroom=classroom)
            if form.is_valid():
                attendance_instance = form.save(commit=False)
                attendance_instance.save()
                
                # Retrieve the learner selected in the form
                learner = form.cleaned_data['learner']
                
                # Send a message to the parent of the learner
                parent = learner.parent  # Assuming 'parent' is a ForeignKey or OneToOneField
                message_content = f"{learner.name} is at school today."
                Message.objects.create(sender=request.user, recipient=parent, content=message_content)
                
                messages.success(request, "Attendance marked successfully and message sent to parent.")
                return redirect('home')

        # Debug message before retrieving attendance instances
        print("Before retrieving attendance instances")

        # Retrieve all attendance instances for the current classroom
        attendance_instances = Attendance.objects.filter(classroom=classroom)

        # Debug message after retrieving attendance instances
        print("After retrieving attendance instances")

        return render(request, 'base/attendance_form.html', {'form': form, 'attendance_instances': attendance_instances})
    else:
        return render(request, 'base/home.html')

def get_all_users():
    all_users = User.objects.all()
    return all_users


from django.http import JsonResponse, HttpRequest
import json
import http.client
def generate_response(prompt):
    # Your code to interact with the OpenAI API and generate a response based on the prompt
    # Make sure to use the prompt parameter in your API request

    api_key = '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'
    endpoint = '/v1/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'text-davinci-003',  # Choose the appropriate model
        'prompt': prompt,
        'max_tokens': 50,  # Adjust as needed
    }

    # Establish connection
    connection = http.client.HTTPSConnection('api.openai.com')

    # Send the request
    connection.request('POST', endpoint, body=json.dumps(data), headers=headers)

    # Get the response
    response = connection.getresponse()
    

    if response.status == 200:
        response_data = json.loads(response.read().decode())
        if 'choices' in response_data:
            return response_data['choices'][0]['text']
        else:
            return None
    else:
        # If response status is not 200, there might be an error
        error_message = response.reason
        # You can also parse the error message from the response body if available
        error_body = response.read().decode()
        print(f"Error: {error_message}")
        print(f"Error Body: {error_body}")
        return None


def chat_view(request):
    if request.method == 'POST':
        # Retrieve user input from the form
        user_input = request.POST.get('user_input', '')
        
        # Generate response using OpenAI API
        response_text = generate_response(user_input)

        # Debugging: Print the response text
        print("Response from OpenAI:", response_text)

        # Return the response text as JSON
        return JsonResponse({'response': response_text})
    else:
        # If it's a GET request, render the empty chatbot template
        return render(request, 'base/chatbot_form.html', {'response_text': '', 'user_input': ''})


@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home page after successful upload
    else:
        # Check if the user is in the Django user model
        if request.user.is_authenticated and User.objects.filter(pk=request.user.pk).exists():
            # Proceed if the user exists in the Django user model
            profile_instance, created = Profile.objects.get_or_create(user=request.user)
            form = ProfilePictureForm(instance=profile_instance)
        else:
            # Redirect the user or display an error message if they are not in the Django user model
            return redirect('home')  # Redirect to home or any appropriate page
    return render(request, 'base/modal.html', {'form': form})

from django.core.serializers import serialize
@login_required(login_url='/login')
def home(request):
    all_users = User.objects.all()
    comments = Comment.objects.all().order_by('-created')
    # Get the logged-in user
    logged_in_user = request.user
    
    assigned_learners = Learner.objects.filter(parent=logged_in_user)
    
    # Check if the user has a UserProfile
    
    try:
        user_profile = UserProfile.objects.get(user=logged_in_user)
        assigned_subjects = user_profile.assigned_subjects.all()
        has_user_profile = True
    except UserProfile.DoesNotExist:
        # Handle the case where the user does not have a UserProfile
        assigned_subjects = None
        has_user_profile = False
    
    # Determine which template to render based on whether the user has a UserProfile
    if has_user_profile:
        template_name = 'base/home.html'
    else:
        template_name = 'base/default_home.html'
    
    # Initialize an empty dictionary to store marks data for each subject
    marks_data_dict = {}
    
    if assigned_subjects:
        # Iterate over each subject and fetch marks data
        for subject in assigned_subjects:
            marks_data = Marks.objects.filter(subject=subject)
            marks_data_list = []
            for mark in marks_data:
                marks_data_list.append({
                    'learner__name': mark.learner.name,
                    'average_marks': mark.calculate_average()  # Calculate average dynamically
                })
            marks_data_dict[subject.name] = marks_data_list
    
    # Convert marks_data_dict to JSON format
    marks_data_json = {subject_name: marks_data for subject_name, marks_data in marks_data_dict.items()}
    
    # Querying the Learner model for search bar and output on feed section
    query = request.GET.get('q')
    if query:
        learners = Learner.objects.filter(name__icontains=query)
    else:
        learners = None
    # Retrieving announcement, classroom, and grade for showing on the home page
    announcements = Announcement.objects.all()
    classrooms = Classroom.objects.all()
    grades = Grade.objects.all()
    
    
    context = {
        'has_user_profile': has_user_profile,
        'marks_data_json': marks_data_json,
        'assigned_subjects': assigned_subjects,
        'grades': grades,
        'classrooms': classrooms,
        'announcements': announcements,
        'learners': learners,
        'comments':comments,
        'assigned_learners': assigned_learners,
        'all_users':all_users
    }
    return render(request, template_name, context)


def grade(request, grade_name):
    #get the grade's subject and learners to show in grade.html
    grade = get_object_or_404(Grade, name=grade_name)
    subjects = Subject.objects.filter(gradeName=grade) 
    learners = Learner.objects.filter(gradeName=grade)
        
    # Filter classrooms by the grade
    classrooms = Classroom.objects.filter(grade=grade)
    context = {'classrooms':classrooms,'subjects':subjects,'grade': grade,  'learners': learners}
    return render(request, 'base/grade.html', context)


def all_learners(request):
    #get a list of all learners
    all_learners = Learner.objects.all()
    subjects = Subject.objects.all()
    context = {'subjects':subjects, 'all_learners': all_learners}
    return render(request, 'base/all_learners.html', context)




def learner(request, pk):
    
       logged_in_user = request.user

       assigned_learners = Learner.objects.filter(parent=logged_in_user) 
       learners = Learner.objects.get(id=pk)
       subjects = Subject.objects.all()
       marks = Marks.objects.all()
       context = {'assigned_learners':assigned_learners,'marks':marks, 'subjects':subjects,'learners': learners}
       return render(request, 'base/learner_detail.html', context)



from django.forms import formset_factory


@login_required(login_url='/login')
def updateMarks(request, pk):
    subject = get_object_or_404(Subject, id=pk)
    marks_instances = Marks.objects.filter(subject=subject)

    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            learner = form.cleaned_data['learner']
            task1 = form.cleaned_data['task1']
            task2 = form.cleaned_data['task2']
            task3 = form.cleaned_data['task3']
            term = form.cleaned_data['term']
            
            task4 = form.cleaned_data['task4']
            task5 = form.cleaned_data['task5']
            task6 = form.cleaned_data['task6']
            term2 = form.cleaned_data['term2']
            
            task7 = form.cleaned_data['task7']
            task8 = form.cleaned_data['task8']
            task9 = form.cleaned_data['task9']
            term3 = form.cleaned_data['term3']
            
            task10 = form.cleaned_data['task10']
            task11= form.cleaned_data['task11']
            task12= form.cleaned_data['task12']
            term4 = form.cleaned_data['term4']

            # Update existing marks or create new marks if they don't exist
            for marks_instance in marks_instances:
                if marks_instance.learner == learner:
                    marks_instance.task1 = task1
                    marks_instance.task2 = task2
                    marks_instance.task3 = task3
                    marks_instance.term = term
                    
                    marks_instance.task4 = task4
                    marks_instance.task5 = task5
                    marks_instance.task6 = task6
                    marks_instance.term2 = term2
                    
                    marks_instance.task7 = task7
                    marks_instance.task8 = task8
                    marks_instance.task9 = task9
                    marks_instance.term3 = term3

                    marks_instance.task10 = task10
                    marks_instance.task11 = task11
                    marks_instance.task12 = task12
                    marks_instance.term4 = term4                    
                    marks_instance.save()
                    return redirect('subject-name', pk=pk)

            # If marks for the learner do not exist, create new marks
            Marks.objects.create(
                learner=learner,
                subject=subject,
                task1=task1,
                task2=task2,
                task3=task3,
                term=term,
                
                task4=task4,
                task5=task5,
                task6=task6,
                term2=term2,
                
                task7=task7,
                task8=task8,
                task9=task9,
                term3=term3,
                
                
                task10=task10,
                task11=task11,
                task12=task12,
                term4=term4
            )
            return redirect('subject-name', pk=pk)
    else:
        form = MarksForm()

    context = {'subject': subject, 'form': form}
    return render(request, 'base/edit_marks.html', context)


def subjectNames(request, pk):
    # Fetch the specific subject based on the provided pk (subject ID)
    subjects = get_object_or_404(Subject, id=pk)
    department = Department.objects.all()
    
    # Get the grade associated with the subject
    grades = subjects.gradeName

    # Retrieve learners in the specific grade for the specific subject
    learners = Learner.objects.filter(gradeName=grades, subjects=subjects)
    
    # Initialize an empty list to store marks for each learner
    marks = []

    # Iterate over each learner
    for learner in learners:
        # Fetch the marks for the current learner in the specific subject
        learner_marks = Marks.objects.filter(learner=learner, subject=subjects).first()
       
        if learner_marks:
            # Calculate the average score for the learner
            learner_marks.term, learner_marks.term2, learner_marks.term3, learner_marks.term4 = learner_marks.calculate_term()
            learner_marks.average_score = learner_marks.calculate_average()

            # Add the marks to the list
            marks.append(learner_marks)
    
    

    
    context = {'department': department, 'marks': marks, 'subjects': subjects, 'grades': grades, 'learners': learners}
    return render(request, 'base/subject_detail.html', context)




def department(request, pk):
    department = Department.objects.get(id=pk)
    context = {'department':department}
    return render(request, 'base/subject_detail.html', context)



from django.core.serializers import serialize

def chart_data(request, subject_name):
    # Retrieve marks data for a specific subject
    marks_data = Marks.objects.filter(subject__name=subject_name).values('learner__name', 'term')

    # Retrieve the subjects assigned to the current user
    assigned_subjects = Subject.objects.filter(name=subject_name)

    # Serialize the queryset of assigned subjects to JSON
    assigned_subjects_json = serialize('json', assigned_subjects)

    # Convert QuerySet to list of dictionaries
    marks_list = list(marks_data)
    print("Assigned subjects JSON:", assigned_subjects_json)

    # Pass data and assigned subjects to the template
    return render(request, 'base/graphs.html', {'subject_name': subject_name, 'marks_list': marks_list, 'assigned_subjects_json': assigned_subjects_json})



def subjectDetail(request):
    # Fetch all subjects
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the home page or any other appropriate URL after form submission
    else:
        form = MarksForm()

    context = {'form': form}
    return render(request, 'base/subject_form.html', context)




def announcement(request, pk):
    all_users = User.objects.all()
    announcement = Announcement.objects.get(id=pk)
    comments = Comment.objects.filter(announcement=announcement).order_by('-created')

    if request.method == 'POST':
        comment_body = request.POST.get('body')
        if comment_body:
            Comment.objects.create(
                user=request.user,
                announcement=announcement,
                body=comment_body
            )
        return redirect('announcement', pk=pk)

    context = {'all_users': all_users, 'announcement': announcement, 'comments': comments}
    return render(request, 'base/announcement.html', context)


def view_all_messages(request):
    # Retrieve all comments/messages
    all_messages = Comment.objects.all()
    
    # Pass all_messages to the template
    context = {'all_messages': all_messages}
    return render(request, 'base/default_home.html', context)


def classroomMarks(request, pk):
    # Get classroom by ID
    classroom = get_object_or_404(Classroom, id=pk)
    
    # Get subjects in the specific classroom
    subjects = Subject.objects.filter(gradeName=classroom.grade)
    
    # Specify the subject you are interested in (change 'YourSubjectName' to the desired subject)
    subject_name = 'YourSubjectName'
    subject = get_object_or_404(Subject, name=subject_name)

    # Retrieve learners in the specific classroom for the specified subject
    learners = Learner.objects.filter(classroomName=classroom, marks__subject=subject).distinct()

    # Initialize an empty list to store marks
    marks = []

    # Iterate over each learner
    for learner in learners:
        # Fetch the marks for the current learner in the specific subject
        learner_marks = Marks.objects.filter(learner=learner, subject=subject).first()
       
        if learner_marks:
            # Calculate the average score for the learner
            learner_marks.term, learner_marks.term2, learner_marks.term3, learner_marks.term4 = learner_marks.calculate_term()
            learner_marks.average_score = learner_marks.calculate_average()

            # Add the marks to the list
            marks.append(learner_marks)

    context = {
        'subjects': subjects,
        'learners': learners,
        'classroom': classroom,
        'marks': marks,
    }
    return render(request, 'base/classroom.html', context)



def classroom(request, pk):
    # Get classroom by ID
    classroom = get_object_or_404(Classroom, id=pk)
    
    # Get subjects in the specific classroom
    subjects = Subject.objects.filter(gradeName=classroom.grade)

    # Retrieve learners in the specific classroom for specific subjects
    learners = Learner.objects.filter(classroomName=classroom)
    # Retrieve marks for the learners in the specified classroom and subjects
    marks = Marks.objects.filter(learner__in=learners, subject__in=subjects)

    context = {'subjects': subjects, 'learners': learners, 'classroom': classroom,'marks':marks}
    return render(request, 'base/classroom.html', context)


def markAttendance(request):
    attendanceRegister = Attendance()
    if request.method == 'POST':
        form = writeAnnouncement(request.POST)
        if form.is_valid:
            attendanceRegister = form.save(commit=False)
            announcement.host = request.user
            announcement.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request, 'base/announcement_form.html', context)
    


def createAnnouncement(request):
    
    form = writeAnnouncement()
    if request.method == 'POST':
        form = writeAnnouncement(request.POST)
        if form.is_valid:
            announcement = form.save(commit=False)
            announcement.host = request.user
            announcement.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request, 'base/announcement_form.html', context)


@login_required(login_url='/login')
def updateAnnouncement(request, pk):
    announcement = Announcement.objects.get(id=pk)
    form = writeAnnouncement(instance = announcement) 
    if request.user != announcement.host:
        return HttpResponse('Access Denied')
    
    
    
    if request.method == 'POST':
        form = writeAnnouncement(request.POST, instance = announcement)
        if form.is_valid:
            form.save()
            return redirect('home')
    
    context = {'form': form, 'announcement':announcement}
    return render(request, 'base/announcement_form.html', context)

@login_required(login_url='/login')
def deleteAnnouncement(request, pk):
    announcement = Announcement.objects.get(id=pk)
    
    if request.user != announcement.host:
        return HttpResponse('Access Denied')
    if request.method == 'POST':
            announcement.delete()
            return redirect('home')
    
    return render(request, 'base/delete.html', {'obj':announcement})






@login_required(login_url='/login')
def deleteMessage(request, pk):
    comment = Comment.objects.get(id=pk)
    
    if request.user != comment.user:
        return HttpResponse('Access Denied')
    if request.method == 'POST':
            comment.delete()
            return redirect('home')
    
    return render(request, 'base/delete.html', {'obj':comment})

