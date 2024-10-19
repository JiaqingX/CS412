
from django.urls import path
from .views import CreateProfileView, ShowAllProfilesView, ShowProfilePageView, CreateStatusMessageView, UpdateStatusMessageView, DeleteStatusMessageView, UpdateProfileView


urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'),
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
]
