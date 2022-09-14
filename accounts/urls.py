# from django.urls import path
# from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from .views import Profile

app_name = "accounts"
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('username_change/', views.username_change, name="username_change"),
    path('password_change/', views.password_change, name="password_change"),
    path('profile/', Profile.as_view(), name="profile"),
         ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)