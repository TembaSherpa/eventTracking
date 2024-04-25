from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout', views.handle_logout, name="logout"),
    path('homepage/', views.homepage, name="homepage"),
    path('create/', views.create_class, name='create_class'),
    path('class/<int:pk>/', views.class_detail, name='class_detail'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('send-email/', views.send_email, name='send_email'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('dashboard/delete/<int:pk>/', views.delete_class, name='delete_class'),
    path('dashboard/delete_teacher/<int:pk>/', views.delete_teacher, name='delete_teacher'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)