from django.urls import path

from author import views

app_name = 'author'

urlpatterns = [
    path('author/create/', views.CreateAuthorView.as_view(), name='create'),
    path('author/auth/', views.AuthAuthorView.as_view(), name='auth'),
    path('author/me/', views.MyProfileView.as_view(), name = 'me'),
    path('authors/', views.AllLocalAuthorsView.as_view(), name = 'all_local'),
    path('all-authors/', views.AllAuthorsView.as_view(), name = 'all'),
    path('author/<slug:pk>/', views.AuthorProfileView.as_view(), name = 'authors'),
]