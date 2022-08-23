"""BH_DJANGO URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views

from pages import views

urlpatterns = [
    path('viv_help/', views.viv_help_view, name='viv_help'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('viv/', views.viv_view, name='viv'),
    path('flash/', views.flash_view, name='flash'),
    path('unsub/', views.unsub_view, name='unsub'),
path('loc/', views.loc_view, name='loc'),
path('gender/', views.gender_view, name='gender'),
path('doc/', views.doc_view, name='doc'),
path('age/', views.age_view, name='age'),
path('caseload/', views.caseload_view, name='caseload'),
    path('', views.homepage_view, name='home'),
    path('admin/', admin.site.urls),
    path('logout/', views.logout_user, name="logout"),
    path('clinical/', views.clinical_dc_view, name='clinical'),
    path('cl_dc_dl/', views.cl_dc_dl_view, name='cl_dc_dl'),
    path('flash_tools/', views.flash_report_tools_view, name='flash_tools'),
    path("register", views.register_request, name="register"),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name='password_reset_complete'),
    path("password_reset", views.password_reset_request, name="password_reset")

]
