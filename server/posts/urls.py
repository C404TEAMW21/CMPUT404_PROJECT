from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [
    path('author/<uuid:author_id>/posts/', views.CreatePostView.as_view(), name='create'),
    path('author/<uuid:author_id>/posts/<uuid:pk>/', views.UpdatePostView.as_view(), name='update'),
    path('public/', views.PublicPostView.as_view(), name='public'),
] 