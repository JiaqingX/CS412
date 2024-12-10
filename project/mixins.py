from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Course

class IsInstructorMixin(UserPassesTestMixin):
    """
    Custom mixin to check if the user is the instructor of the course.
    """
    def test_func(self):
        course = get_object_or_404(Course, id=self.kwargs['course_id'])
        return self.request.user == course.instructor
