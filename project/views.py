from django.views.generic import ListView, DetailView
from .models import Course

class CourseListView(ListView):
    model = Course
    template_name = 'project/course_list.html'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'project/course_detail.html'
