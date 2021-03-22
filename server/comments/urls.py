from django.urls import path

from comments import views

app_name = 'comments'

urlpatterns = [
    path('<uuid:author_id>/posts/<uuid:post_id>/comments', 
        views.CreateCommentView.as_view(), name='comments'),
]  
