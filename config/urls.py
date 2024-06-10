"""
URL configuration for customJira project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)
from rest_framework.routers import DefaultRouter

from src.tasks.views import TaskViewSet, TakeTaskView, CompleteTaskView, TaskUpdateView
from src.users.views import LogoutAPIView, LoginAPIView, RegisterAPIView, CurrentUserView, EmployeeListView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth API
    path('api/v1/logout/', LogoutAPIView.as_view(), name='logging_out'),
    path('api/v1/login/', LoginAPIView.as_view(), name='logging_in'),
    path('api/v1/register/', RegisterAPIView.as_view(), name="sign_up"),

    # Users API
    path('api/v1/current-user/', CurrentUserView.as_view(), name='get_current_user'),
    path('api/v1/employers/', EmployeeListView.as_view(), name='get_employers'),

    # Tasks API
    path('api/v1/', include(router.urls)),
    path('api/v1/tasks/<uuid:uuid>/complete/', CompleteTaskView.as_view()),
    path('api/v1/tasks/<uuid:uuid>/take/', TakeTaskView.as_view()),
    path('api/v1/tasks/<uuid:uuid>/edit/', TaskUpdateView.as_view()),

    # Swagger API
    path('api/v1/docs/download/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/v1/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'api/v1/docs/specific/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
]
