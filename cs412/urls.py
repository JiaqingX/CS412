"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('quotes.urls')),
    path('restaurant/', include('restaurant.urls')),
]


from django.contrib import admin
from django.urls import path, include
from restaurant import views as restaurant_views

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('', restaurant_views.main, name='main'),  # Set restaurant as the default homepage
    path('restaurant/', include('restaurant.urls')),  # Restaurant application URL patterns
    path('quotes/', include('quotes.urls')),  # Quotes application URL patterns
]
