"""renthouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from guest import views
from django.contrib.auth import views as auth_views


admin.site.site_header="RentHouse Admin"
admin.site.site_title="RentHouse Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('search/', views.search_view, name='search'),
    path('search-filter/', views.search_filter_view, name="search_filter"),
    path('addroom/', views.addroom_view, name='addroom'),
    path('update-room/<int:pk>', views.update_room_view, name='update_room'),
    path('delete-room/<int:pk>', views.delete_room_view, name='delete_room'),
    path('room/<int:rid>', views.room_view, name='room'),
    path('contact-owner/<int:rid>', views.contact_owner_view, name='contact_owner'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account-settings/', views.account_settings_view, name='account_settings'),
    path('update-password/', views.update_password_view, name='update_password'),
    path('delete-user-account/<int:pk>', views.delete_user_account_view, name='delete_user_account'),
    path('dashboard/<int:pk>', views.dashboard_view, name='dashboard'),

    # reset password with email fucntionality
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)