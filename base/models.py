from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    assigned_subjects = models.ManyToManyField('Subject')  # Many-to-many relationship with Subject
    assigned_classroom = models.ForeignKey('Classroom', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f'{self.user.username} Profile'
    
    

class Attendance(models.Model):
    ATTENDANCE_TRACKING = (
        ('P', 'Present'),
        ('A', 'Absent'),
    )
    weeks = models.ForeignKey('Week', on_delete=models.SET_NULL, null=True)
    learner = models.ForeignKey('Learner', on_delete=models.SET_NULL, null=True)
    classroom = models.ForeignKey('Classroom', on_delete=models.SET_NULL, null=True)
    monday = models.CharField(max_length=1, choices=ATTENDANCE_TRACKING, null=True, blank=True)
    tuesday = models.CharField(max_length=1, choices=ATTENDANCE_TRACKING, null=True, blank=True)
    wednesday = models.CharField(max_length=1, choices=ATTENDANCE_TRACKING, null=True, blank=True)
    thursday = models.CharField(max_length=1, choices=ATTENDANCE_TRACKING, null=True, blank=True)
    friday = models.CharField(max_length=1, choices=ATTENDANCE_TRACKING, null=True, blank=True)

    def __str__(self):
        return f"{self.monday} {self.tuesday} {self.wednesday} {self.thursday} {self.friday}"

    
    
class Week(models.Model):
    name = models.CharField(max_length=50, null=True, default='')
    
    def __str__(self):
        return self.name
    
    
    

class Learner(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    gradeName = models.ForeignKey('Grade', on_delete=models.SET_NULL, null=True)
    classroomName = models.ForeignKey('Classroom', on_delete=models.SET_NULL, null=True)
    subjects = models.ManyToManyField('Subject')  # Many-to-many relationship with Subject
    parent = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    

    def __str__(self):
        return f"{self.name} {self.surname}"

    


class Subject(models.Model):
    name = models.CharField(max_length=100)
    gradeName = models.ForeignKey('Grade', on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
 
        return self.name
  

 

    
    
class Classroom(models.Model):
    name = models.CharField(max_length=100, null=True)
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    subjects = models.ManyToManyField(Subject)
    
    def __str__(self):
        return self.name
    

class Grade(models.Model):
    name = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

    


class Marks(models.Model):
    name = models.CharField(max_length=50, default='Unknown')  # Example default value
    
    task1 = models.CharField(max_length=50, null=True, default='')
    task2 = models.CharField(max_length=50, null=True, default='')
    task3 = models.CharField(max_length=50, null=True, default='')
    term = models.FloatField(null=True, default=None)
    
    task4 = models.CharField(max_length=50, null=True, default='')
    task5 = models.CharField(max_length=50, null=True, default='')
    task6 = models.CharField(max_length=50, null=True, default='')
    term2 = models.FloatField(null=True, default=None)
    
    task7 = models.CharField(max_length=50, null=True, default='')
    task8 = models.CharField(max_length=50, null=True, default='')
    task9 = models.CharField(max_length=50, null=True, default='')
    term3 = models.FloatField(null=True, default=None)
    
    task10 = models.CharField(max_length=50, null=True, default='')
    task11 = models.CharField(max_length=50, null=True, default='')
    task12 = models.CharField(max_length=50, null=True, default='')
    term4 = models.FloatField(null=True, default=None) 
    # Change to FloatField for calculated sum
    
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='marks', null=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)

    def __str__(self):
         return f"{self.learner.name} {self.learner.surname} {self.subject}"
    
    

    def calculate_average(self):
        tasks = [self.task1, self.task2, self.task3, self.task4, self.task5, self.task6, self.task7, self.task8, self.task9, self.task10, self.task11, self.task12]
        # Filter out empty strings and convert to integers
        scores = [int(task) for task in tasks if task]
        if scores:
            return sum(scores) / len(scores)
        else:
            return None

    def calculate_term(self):
        task1 = int(self.task1) if self.task1 else 0
        task2 = int(self.task2) if self.task2 else 0
        task3 = int(self.task3) if self.task3 else 0

        task4 = int(self.task4) if self.task4 else 0
        task5 = int(self.task5) if self.task5 else 0
        task6 = int(self.task6) if self.task6 else 0
        
        task7 = int(self.task7) if self.task7 else 0
        task8 = int(self.task8) if self.task8 else 0
        task9 = int(self.task9) if self.task9 else 0
        
        task10 = int(self.task10) if self.task10 else 0
        task11 = int(self.task11) if self.task11 else 0
        task12 = int(self.task12) if self.task12 else 0


        task1_percentage = (task1*float(0.25)) 
        task2_percentage = (task2*float(0.25))
        task3_percentage = (task3*float(0.5))

        task4_percentage = (task4*float(0.25)) 
        task5_percentage = (task5*float(0.25))
        task6_percentage = (task6*float(0.5))

        task7_percentage = (task7*float(0.25)) 
        task8_percentage = (task8*float(0.25))
        task9_percentage = (task9*float(0.5))

        task10_percentage = (task10*float(0.25)) 
        task11_percentage = (task11*float(0.25))
        task12_percentage = (task12*float(0.5))
        
        term = task1_percentage + task2_percentage + task3_percentage 
        term2 = task4_percentage+task5_percentage+task6_percentage
        term3 = task7_percentage+task8_percentage+task9_percentage
        term4 = task10_percentage+task11_percentage+task12_percentage 
        
        return term, term2, term3, term4
    
    def save(self, *args, **kwargs):
       # Calculate term
        self.term, self.term2, self.term3, self.term4 = self.calculate_term()
    
        self.average_score = self.calculate_average()  # Calculate average
        super().save(*args, **kwargs)




class Announcement(models.Model):
    host =  models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    department =  models.ForeignKey(Department,on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=20, null=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User,related_name='participants', blank= True)
    updated = models.DateTimeField(auto_now=True)
    created= models.DateTimeField(auto_now=True)
    
       
    class Meta:
        ordering = ['-updated', '-created']  
    
    def __str__(self):
        return self.title
    
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='images/avatar.svg')

    # Add any additional profile fields you need, such as bio, location, etc.
    
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

    # Create a profile for each new user
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    
    
   
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)
    def __str__(self):
       return f"{self.user.username} liked comment: {self.comment.id}"
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    announcement = models.ForeignKey(Announcement,on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.body[0:50]