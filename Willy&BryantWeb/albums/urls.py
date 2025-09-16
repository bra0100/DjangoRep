from django.urls import path
from django.contrib.auth import views as auth_views
from .views import HomeView, AlbumListView, AlbumUpdateView, AlbumDeleteView, register, upload_album,  custom_login, custom_logout

urlpatterns = [
    # Página de inicio REAL
    path('', HomeView.as_view(), name='home'),

    # Lista completa de álbumes
    path('albums/', AlbumListView.as_view(), name='album_list'),

    # Other CRUD operations
    path('upload/', upload_album, name='upload_album'),
    path('album/<int:pk>/edit/', AlbumUpdateView.as_view(), name='edit_album'),
    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name='delete_album'),

    # Authentication
    path('login/', custom_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', custom_logout, name='logout'),
]
