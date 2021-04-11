from django.urls import path

from posts import views

app_name = 'posts'

urlpatterns = [
    path('author/<uuid:author_id>/posts/', views.CreatePostView.as_view(), name='create'),
    path('author/<str:author_id>/posts/<str:pk>/', views.UpdatePostView.as_view(), name='update'),
    path('author/<str:author_id>/posts/<str:pk>/share/', views.SharePostView.as_view(), name='share'),
    path('public/', views.PublicPostView.as_view(), name='public'),
] 