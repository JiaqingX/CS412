from django.urls import path
from .views import (
    # Home and user management
    UserLoginView,
    UserLogoutView,
    register_view,
    HomeView,  # 修改后的主页视图
    CourseListView, 
    CourseDetailView, 
    AssignmentListView, 
    AssignmentCreateView, 
    EnrollmentListView, 
    EnrollmentCreateView,
    GradeListView,
    DiscussionThreadListView,
    DiscussionThreadCreateView,
    CommentCreateView,
    CertificateListView,
    AttendanceListView,
    NotificationListView,
    ResourceListView,
)

urlpatterns = [
    # Home
    path('', HomeView.as_view(), name='home'),  # 修改为登录和注册页面

    # User management
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(next_page='home'), name='logout'),
    path('register/', register_view, name='register'),
    
    # Courses
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    
    # Assignments
    path('courses/<int:course_id>/assignments/', AssignmentListView.as_view(), name='assignment_list'),
    path('courses/<int:course_id>/assignments/create/', AssignmentCreateView.as_view(), name='assignment_create'),
    
    # Enrollments
    path('courses/<int:course_id>/enrollments/', EnrollmentListView.as_view(), name='enrollment_list'),
    path('courses/<int:course_id>/enrollments/create/', EnrollmentCreateView.as_view(), name='enrollment_create'),
    
    # Grades
    path('courses/<int:course_id>/grades/', GradeListView.as_view(), name='grade_list'),

    # Discussions
    path('courses/<int:course_id>/discussions/', DiscussionThreadListView.as_view(), name='discussion_list'),
    path('courses/<int:course_id>/discussions/create/', DiscussionThreadCreateView.as_view(), name='discussion_create'),
    path('discussions/<int:thread_id>/comments/create/', CommentCreateView.as_view(), name='comment_create'),
    
    # Certificates
    path('certificates/', CertificateListView.as_view(), name='certificate_list'),

    # Attendance
    path('courses/<int:course_id>/attendance/', AttendanceListView.as_view(), name='attendance_list'),
    
    # Notifications
    path('notifications/', NotificationListView.as_view(), name='notification_list'),

    # Resources
    path('courses/<int:course_id>/resources/', ResourceListView.as_view(), name='resource_list'),
]
