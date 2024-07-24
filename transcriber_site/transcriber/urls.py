from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_file, name='upload'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('download/<str:filename>/', views.download_file, name='download_file'),
    path('transcription_history/', views.transcription_history, name='transcription_history'),
]
