from django.urls import path
from . import views

urlpatterns = [
    
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('announcement/<str:pk>/', views.announcement, name="announcement"),
    path('create-announcement/', views.createAnnouncement, name="create-announcement"),
    path('update-announcement/<str:pk>/', views.updateAnnouncement, name="update-announcement"),
    path('delete-announcement/<str:pk>/', views.deleteAnnouncement, name="delete-announcement"),
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
  #
    # path('user/messages/<int:recipient_id>/', views.user_to_user_messages, name='user_to_user_messages'),
    # path('send_message/', views.send_message, name='send_message'),
    
    path('grade-name/<str:grade_name>/', views.grade, name="grade-name"),
    path('learner-detail/<str:pk>/', views.learner, name="learner-detail"),
    path('classroom-name/<str:pk>/', views.classroom, name="classroom-name"),
    path('subject-marks/', views.subjectDetail, name="subject-marks"),
    path('update-marks/<str:pk>', views.updateMarks, name="update-marks"),
    path('subject-name/<str:pk>/', views.subjectNames, name="subject-name"),
    path('department-name/<str:pk>/', views.department, name="department-name"),
    path('learners-name/', views.all_learners, name="learners-name"),
    path('classroom-mark/<str:pk>/', views.classroomMarks, name="classroom-mark"),
    path('attendance/', views.mark_attendance, name='attendance'),
    path('attendance/teacher-list/', views.teacher_attendance_list, name='teacher_attendance_list'),
    path('inbox/', views.inbox, name='inbox'),
    path('register-detail/', views.teacher_attendance_list, name='register-detail'),
    
    path('chat/', views.chat_view, name='chat_view')
    # path('chart_data/<str:subject_name>/', views.chart_data, name='chart_data'),
    # # path('charts/', views.chart1, name="charts"),





]




