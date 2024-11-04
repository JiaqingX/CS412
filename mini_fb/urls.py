from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    CreateProfileView, ShowAllProfilesView, ShowProfilePageView,
    CreateStatusMessageView, UpdateStatusMessageView, DeleteStatusMessageView,
    UpdateProfileView, CreateFriendView, ShowFriendSuggestionsView, ShowNewsFeedView
)

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    
    # Adding patterns as requested without requiring pk
    path('profile/update/', UpdateProfileView.as_view(), name='profile_update'),
    path('profile/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='profile_friend_suggestions'),
    path('profile/news_feed/', ShowNewsFeedView.as_view(), name='profile_news_feed'),
    path('profile/add_friend/<int:other_pk>/', CreateFriendView.as_view(), name='profile_add_friend'),

    # Patterns that use pk
    path('status/create_status/<int:pk>/', CreateStatusMessageView.as_view(), name='create_status'),
    path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status'),
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile_with_pk'),
    path('profile/<int:pk>/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions_with_pk'),
    path('profile/<int:pk>/news_feed/', ShowNewsFeedView.as_view(), name='news_feed_with_pk'),
    path('profile/<int:pk>/add_friend/<int:other_pk>/', CreateFriendView.as_view(), name='add_friend_with_pk'),

    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'),
]
