from django.urls import path

from likes import views

app_name = 'likes'

urlpatterns = [
    path('<str:author_id>/posts/<str:post_id>/likes/', 
        views.ListPostLikesView.as_view(), name='post_likes'),
    path('<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/likes/', 
        views.ListCommentLikesView.as_view(), name='comment_likes'),
    path('<str:author_id>/liked/', 
        views.ListLikedView.as_view(), name='liked'),
]
