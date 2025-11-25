from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("book/create/", views.create_book, name="create_book"),
    path("book/<int:book_id>/", views.book_detail, name="book_detail"),
    path("book/<int:book_id>/create-sketch/", views.create_sketch, name="create_sketch"),
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create_sketch, name='create_sketch'),
    path('sketch/<int:sketch_id>/', views.sketch_room, name='sketch_room'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('save-sketch/', views.save_sketch, name='save_sketch'),
    path('clear-sketch/<int:sketch_id>/', views.clear_sketch, name='clear_sketch'),
    path('upload-ocr/<int:sketch_id>/', views.upload_sketch_screenshot, name='upload_sketch_screenshot'),
    
    # New audio endpoints
    path('generate-audio/<int:sketch_id>/', views.generate_sketch_audio, name='generate_sketch_audio'),
    path('get-audio/<int:sketch_id>/', views.get_sketch_audio, name='get_sketch_audio'),
    path('upload-and-audio/<int:sketch_id>/', views.upload_and_generate_audio, name='upload_and_generate_audio'),
    path('supported-languages/', views.get_supported_languages, name='get_supported_languages'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)