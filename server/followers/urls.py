from django.urls import path

from followers import views

app_name = 'followers'

urlpatterns = [
    path('<uuid:author_id>/followers/', views.FollowersView.as_view(), name='followers'),
    path('<uuid:author_id>/followers/<uuid:follower_id>',
        views.FollowersUpdateView.as_view(), name='update_followers'),
    path('<uuid:author_id>/friends/', views.FriendView.as_view(), name="friends"),
]
