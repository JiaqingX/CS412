from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .models import (
    Course, Assignment, Enrollment, Grade, DiscussionThread, Comment,
    Certificate, Attendance, Notification, Resource
)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home(request):
    return render(request, 'home.html', {'user': request.user})


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'project/home.html'


# 用户登录视图
class UserLoginView(LoginView):
    template_name = 'project/login.html'


# 用户注销视图
class UserLogoutView(LogoutView):
    next_page = 'login'  # 注销后跳转到主页


from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            # 添加用户到选定的组
            group = form.cleaned_data.get('group')
            group.user_set.add(user)

            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'project/register.html', {'form': form})

# 自定义主页视图
class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('course_list')  # 登录后重定向到课程列表
        login_form = AuthenticationForm()
        register_form = UserCreationForm()
        return render(request, 'project/home.html', {
            'login_form': login_form,
            'register_form': register_form,
        })


# 课程相关视图
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'project/course_list.html'
    context_object_name = 'courses'


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'project/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        
        # Existing context data
        context['assignments'] = Assignment.objects.filter(course=course)
        context['enrollments'] = Enrollment.objects.filter(course=course)
        context['discussions'] = DiscussionThread.objects.filter(course=course)

        # Additional context data
        context['resources'] = Resource.objects.filter(course=course)  # Add resources
        context['notifications'] = Notification.objects.filter(user=self.request.user)  # Add notifications for user
        context['attendance_records'] = Attendance.objects.filter(course=course)  # Add attendance records
        context['grades'] = Grade.objects.filter(assignment__course=course)
        return context

# 作业相关视图
class AssignmentListView(LoginRequiredMixin, ListView):
    template_name = 'project/assignment_list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return Assignment.objects.filter(course=course)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 将 course 传递到模板中
        context['course'] = get_object_or_404(Course, id=self.kwargs['course_id'])
        return context



class AssignmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Assignment
    fields = ['title', 'description', 'due_date']
    template_name = 'project/assignment_form.html'

    def test_func(self):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return self.request.user == course.instructor

    def form_valid(self, form):
        form.instance.course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, id=self.kwargs['course_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('assignment_list', kwargs={'course_id': self.kwargs['course_id']})


# 注册相关视图
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from .models import Course, Enrollment

class EnrollmentListView(ListView):
    model = Enrollment
    template_name = 'project/enrollment_list.html'

    def get_queryset(self):
        return Enrollment.objects.filter(course_id=self.kwargs['course_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, id=self.kwargs['course_id'])
        return context



from django.shortcuts import get_object_or_404, reverse
from django.views.generic.edit import CreateView
from .models import Enrollment, Course
from .forms import EnrollmentForm
from .mixins import IsInstructorMixin
from django.contrib.auth.mixins import LoginRequiredMixin

class EnrollmentCreateView(LoginRequiredMixin, IsInstructorMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm  # Use form_class only
    template_name = 'project/enrollment_form.html'

    def form_valid(self, form):
        # Set the course instance from the URL
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        form.instance.course = course
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the course to the context for rendering
        context['course'] = get_object_or_404(Course, id=self.kwargs['course_id'])
        return context

    def get_success_url(self):
        # Redirect to the course enrollment list after successful form submission
        return reverse('enrollment_list', kwargs={'course_id': self.kwargs['course_id']})

# 成绩相关视图
class GradeListView(LoginRequiredMixin, ListView):
    template_name = 'project/grade_list.html'
    context_object_name = 'grades'

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return Grade.objects.filter(assignment__course=course)


# 讨论区相关视图
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from .models import Course, DiscussionThread

class DiscussionThreadListView(ListView):
    model = DiscussionThread
    template_name = 'project/discussion_list.html'

    def get_queryset(self):
        return DiscussionThread.objects.filter(course_id=self.kwargs['course_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, id=self.kwargs['course_id'])
        return context



from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from .models import DiscussionThread, Course

class DiscussionThreadCreateView(CreateView):
    model = DiscussionThread
    fields = ['title', 'content'] 
    template_name = 'project/discussion_form.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        context['course'] = course  # 将 course 传递到模板上下文
        return context

    def form_valid(self, form):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        form.instance.course = course
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('discussion_list', kwargs={'course_id': self.kwargs['course_id']})

# 通知相关视图
class NotificationListView(LoginRequiredMixin, ListView):
    template_name = 'project/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


# Certificate
class CertificateListView(LoginRequiredMixin, ListView):
    template_name = 'project/certificate_list.html'
    context_object_name = 'certificates'

    def get_queryset(self):
        return Certificate.objects.filter(student=self.request.user)


# Attendance 
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView
from .models import Attendance, Course
from .forms import AttendanceForm
from .mixins import IsInstructorMixin

class AttendanceListView(ListView):
    template_name = 'project/attendance_list.html'
    context_object_name = 'attendance_records'

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        self.course = course
        return Attendance.objects.filter(course=course)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.course
        return context


class AttendanceCreateView(LoginRequiredMixin, IsInstructorMixin, CreateView):
    model = Attendance
    fields = ['student', 'date', 'status']
    template_name = 'project/attendance_form.html'

    def form_valid(self, form):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        form.instance.course = course
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, id=self.kwargs['course_id'])
        return context

    def get_success_url(self):
        return reverse('attendance_list', kwargs={'course_id': self.kwargs['course_id']})
    
# resource
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from .models import Resource, Course

class ResourceListView(ListView):
    model = Resource
    template_name = 'project/resource_list.html'
    context_object_name = 'resources'

    def get_queryset(self):
      
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        self.course = course  
        return Resource.objects.filter(course=course)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['course'] = self.course
        return context

from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Resource, Course
from .forms import ResourceForm

class ResourceCreateView(CreateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'project/resource_form.html'

    def form_valid(self, form):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        form.instance.course = course
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(Course, id=self.kwargs['course_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('resource_list', kwargs={'course_id': self.kwargs['course_id']})

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'project/comment_form.html'

    def form_valid(self, form):
        thread = get_object_or_404(DiscussionThread, id=self.kwargs['thread_id'])
        form.instance.thread = thread
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('discussion_list', kwargs={'course_id': self.kwargs['course_id']})
