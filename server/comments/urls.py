from django.urls import path

from comments import views

app_name = 'comments'

urlpatterns = [
    path('<uuid:author_id>/posts/<uuid:post_id>/comments/', 
        views.CreateCommentView.as_view(), name='comments'),
    path('<str:author_id>/posts/<str:post_id>/create_remote_comments/', 
        views.CreateRemoteCommentView.as_view(), name='create_remote_comments'),
    path('<str:author_id>/posts/<str:post_id>/get_remote_comments/', 
        views.GetRemoteCommentView.as_view(), name='get_remote_comments'),
]  
