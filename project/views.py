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

# 用户登录视图
class UserLoginView(LoginView):
    template_name = 'project/login.html'


# 用户注销视图
class UserLogoutView(LogoutView):
    next_page = 'home'  # 注销后跳转到主页


# 用户注册视图
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group, created = Group.objects.get_or_create(name='students')
            user.groups.add(group)
            login(request, user)  # 自动登录
            return redirect('home')  # 注册后跳转到主页
    else:
        form = UserCreationForm()
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


# 作业相关视图
class AssignmentListView(LoginRequiredMixin, ListView):
    template_name = 'project/assignment_list.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return Assignment.objects.filter(course=course)


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

    def get_success_url(self):
        return reverse_lazy('assignment_list', kwargs={'course_id': self.kwargs['course_id']})


# 注册相关视图
class EnrollmentListView(LoginRequiredMixin, ListView):
    template_name = 'project/enrollment_list.html'
    context_object_name = 'enrollments'

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return Enrollment.objects.filter(course=course)


class EnrollmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Enrollment
    fields = ['student']
    template_name = 'project/enrollment_form.html'

    def test_func(self):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return self.request.user == course.instructor

    def form_valid(self, form):
        form.instance.course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('enrollment_list', kwargs={'course_id': self.kwargs['course_id']})


# 成绩相关视图
class GradeListView(LoginRequiredMixin, ListView):
    template_name = 'project/grade_list.html'
    context_object_name = 'grades'

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return Grade.objects.filter(assignment__course=course)


# 讨论区相关视图
class DiscussionThreadListView(LoginRequiredMixin, ListView):
    template_name = 'project/discussion_list.html'
    context_object_name = 'threads'

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return DiscussionThread.objects.filter(course=course)


class DiscussionThreadCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = DiscussionThread
    fields = ['title']
    template_name = 'project/discussion_form.html'

    def test_func(self):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return self.request.user == course.instructor

    def form_valid(self, form):
        form.instance.course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('discussion_list', kwargs={'course_id': self.kwargs['course_id']})


# 通知相关视图
class NotificationListView(LoginRequiredMixin, ListView):
    template_name = 'project/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


# 证书相关视图
class CertificateListView(LoginRequiredMixin, ListView):
    template_name = 'project/certificate_list.html'
    context_object_name = 'certificates'

    def get_queryset(self):
        return Certificate.objects.filter(student=self.request.user)


# 出勤相关视图
class AttendanceListView(LoginRequiredMixin, ListView):
    template_name = 'project/attendance_list.html'
    context_object_name = 'attendance_records'

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return Attendance.objects.filter(course=course)


# 资源相关视图
class ResourceListView(LoginRequiredMixin, ListView):
    template_name = 'project/resource_list.html'
    context_object_name = 'resources'

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return Resource.objects.filter(course=course)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    template_name = 'project/comment_form.html'

    def form_valid(self, form):
        # 获取当前讨论线程
        thread = get_object_or_404(DiscussionThread, id=self.kwargs['thread_id'])
        form.instance.thread = thread
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('discussion_list', kwargs={'course_id': self.kwargs['course_id']})
