from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import (
    Course, Enrollment, Assignment, Category, Grade, DiscussionThread,
    Comment, Certificate, Attendance, Notification, Resource
)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'instructor', 'category')
    search_fields = ('course_name', 'instructor__username')
    list_filter = ('category',)
    ordering = ('course_name',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'instructor':
            kwargs['queryset'] = User.objects.filter(groups__name='instructors')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'enrollment_date')
    search_fields = ('course__course_name', 'student__username')
    list_filter = ('course',)
    ordering = ('course', 'student')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'student':
            kwargs['queryset'] = User.objects.filter(groups__name='students')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Assignment)
admin.site.register(Category)
admin.site.register(Grade)
admin.site.register(DiscussionThread)
admin.site.register(Comment)
admin.site.register(Certificate)
admin.site.register(Attendance)
admin.site.register(Notification)
admin.site.register(Resource)
