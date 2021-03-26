from django.urls import path

from followers import views

app_name = 'followers'

urlpatterns = [
    path('<uuid:author_id>/followers/', views.FollowersView.as_view(), name='followers'),
    path('<uuid:author_id>/followers/<uuid:follower_id>',
        views.FollowersUpdateView.as_view(), name='update_followers'),
    # path('<slug:id>/followers/<slug:foreignId>/', views.FollowersModificationView.as_view(), name="followers modify"),
    # path('<slug:id>/friends/', views.FollowersFriendView.as_view(), name="friends"),
]
