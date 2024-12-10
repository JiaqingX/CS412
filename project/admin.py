from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import (
    Course, Enrollment, Assignment, Category, Grade, DiscussionThread,
    Comment, Certificate, Attendance, Notification, Resource
)

# Admin configuration for the Course model
class CourseAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('course_name', 'instructor', 'category')
    # Fields to enable search functionality in the admin interface
    search_fields = ('course_name', 'instructor__username')
    # Fields to filter the results in the admin interface
    list_filter = ('category',)
    # Default ordering of records in the admin list view
    ordering = ('course_name',)

    # Customize the form field for the instructor foreign key
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'instructor':  # Check if the field is 'instructor'
            # Limit the queryset to users belonging to the 'instructors' group
            kwargs['queryset'] = User.objects.filter(groups__name='instructors')
        # Call the superclass method to handle default behavior
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Admin configuration for the Enrollment model
class EnrollmentAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('course', 'student', 'enrollment_date')
    # Fields to enable search functionality in the admin interface
    search_fields = ('course__course_name', 'student__username')
    # Fields to filter the results in the admin interface
    list_filter = ('course',)
    # Default ordering of records in the admin list view
    ordering = ('course', 'student')

    # Customize the form field for the student foreign key
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'student':  # Check if the field is 'student'
            # Limit the queryset to users belonging to the 'students' group
            kwargs['queryset'] = User.objects.filter(groups__name='students')
        # Call the superclass method to handle default behavior
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# Register the models and their corresponding admin configurations
admin.site.register(Course, CourseAdmin)  # Register Course with CourseAdmin configuration
admin.site.register(Enrollment, EnrollmentAdmin)  # Register Enrollment with EnrollmentAdmin configuration
admin.site.register(Assignment)  # Register Assignment with default configuration
admin.site.register(Category)  # Register Category with default configuration
admin.site.register(Grade)  # Register Grade with default configuration
admin.site.register(DiscussionThread)  # Register DiscussionThread with default configuration
admin.site.register(Comment)  # Register Comment with default configuration
admin.site.register(Certificate)  # Register Certificate with default configuration
admin.site.register(Attendance)  # Register Attendance with default configuration
admin.site.register(Notification)  # Register Notification with default configuration
admin.site.register(Resource)  # Register Resource with default configuration
