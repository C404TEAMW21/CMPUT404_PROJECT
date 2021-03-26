from django.urls import path

from likes import views

app_name = 'likes'

urlpatterns = [
    path('<uuid:author_id>/posts/<uuid:post_id>/likes', 
        views.ListPostLikesView.as_view(), name='post_likes'),
    path('<uuid:author_id>/posts/<uuid:post_id>/comments/<uuid:comment_id>/likes', 
        views.ListCommentLikesView.as_view(), name='comment_likes'),
    path('<uuid:author_id>/liked', 
        views.ListLikedView.as_view(), name='liked'),
]
