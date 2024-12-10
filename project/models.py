from django.db import models
from django.contrib.auth.models import User

# Model representing a category for courses
class Category(models.Model):
    name = models.CharField(max_length=100)  # Name of the category
    description = models.TextField(blank=True)  # Optional description of the category

    def __str__(self):
        return self.name  # String representation of the category


# Model representing a course
class Course(models.Model):
    course_name = models.CharField(max_length=200)  # Name of the course
    description = models.TextField()  # Detailed description of the course
    instructor = models.ForeignKey(
        User,  # Foreign key to the User model
        on_delete=models.CASCADE,  # Delete the course if the instructor is deleted
        limit_choices_to={'groups__name': 'instructors'}  # Limit to users in the 'instructors' group
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Category for the course

    def __str__(self):
        return self.course_name  # String representation of the course


# Model representing an enrollment of a student in a course
class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Foreign key to the course
    student = models.ForeignKey(
        User,  # Foreign key to the User model
        on_delete=models.CASCADE,  # Delete the enrollment if the student is deleted
        limit_choices_to={'groups__name': 'students'}  # Limit to users in the 'students' group
    )
    enrollment_date = models.DateField(auto_now_add=True)  # Date when the enrollment was created

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.course_name}"


# Model representing an assignment for a course
class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Foreign key to the course
    title = models.CharField(max_length=200)  # Title of the assignment
    description = models.TextField()  # Detailed description of the assignment
    due_date = models.DateField()  # Due date for the assignment

    def __str__(self):
        return self.title


# Model representing a grade for an assignment
class Grade(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)  # Foreign key to the assignment
    student = models.ForeignKey(
        User,  # Foreign key to the User model
        on_delete=models.CASCADE,  # Delete the grade if the student is deleted
        limit_choices_to={'groups__name': 'students'}  # Limit to users in the 'students' group
    )
    score = models.FloatField()  # Score achieved in the assignment
    feedback = models.TextField(blank=True)  # Optional feedback for the student

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title} - {self.score}"


# Model representing a discussion thread for a course
class DiscussionThread(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Foreign key to the course
    title = models.CharField(max_length=200)  # Title of the thread
    content = models.TextField(null=True, blank=True)  # Optional content of the thread
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Creator of the thread
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the thread was created

    def __str__(self):
        return f"{self.title} - {self.course.course_name}"


# Model representing a comment on a discussion thread
class Comment(models.Model):
    thread = models.ForeignKey(DiscussionThread, on_delete=models.CASCADE, related_name='comments')  # Foreign key to the thread
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Creator of the comment
    content = models.TextField()  # Content of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the comment was created

    def __str__(self):
        return f"Comment by {self.created_by.username} on {self.thread.title}"


# Model representing a certificate for completing a course
class Certificate(models.Model):
    student = models.ForeignKey(
        User,  # Foreign key to the User model
        on_delete=models.CASCADE,  # Delete the certificate if the student is deleted
        limit_choices_to={'groups__name': 'students'}  # Limit to users in the 'students' group
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Foreign key to the course
    issued_date = models.DateField(auto_now_add=True)  # Date when the certificate was issued
    certificate_code = models.CharField(max_length=20, unique=True)  # Unique code for the certificate

    def __str__(self):
        return f"Certificate for {self.student.username} - {self.course.course_name}"


# Model representing attendance for a course
class Attendance(models.Model):
    student = models.ForeignKey(
        User,  # Foreign key to the User model
        on_delete=models.CASCADE,  # Delete the attendance if the student is deleted
        limit_choices_to={'groups__name': 'students'}  # Limit to users in the 'students' group
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Foreign key to the course
    date = models.DateField()  # Date of attendance
    status = models.BooleanField()  # Attendance status: True for Present, False for Absent

    def __str__(self):
        return f"{self.student.username} - {self.course.course_name} - {self.date} - {'Present' if self.status else 'Absent'}"


# Model representing a notification for a user
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to the User model
    message = models.TextField()  # Message content of the notification
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the notification was created
    is_read = models.BooleanField(default=False)  # Status of the notification: Read or Unread

    def __str__(self):
        return f"Notification for {self.user.username} - {'Read' if self.is_read else 'Unread'}"


# Model representing a resource for a course
class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Foreign key to the course
    title = models.CharField(max_length=200)  # Title of the resource
    file = models.FileField(upload_to='resources/')  # File associated with the resource
    url = models.URLField(blank=True, null=True)  # Optional URL for the resource

    def __str__(self):
        return f"{self.title} - {self.course.course_name}"
