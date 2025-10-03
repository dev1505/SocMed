from ChatApp.ChatViews import Get_User_Messages, Home
from django.urls import path

from SocialMediaApp.user_credentials import AuthChecking

from .comments import AddCommentView, DeleteCommentView, GetCommentsView
from .followers import (
    check_followings,
    follow_user,
    get_followers,
    get_followings,
    unfollow_user,
)
from .google_github_auth import (
    GithubCallback,
    GithubLoginURL,
    GoogleCallback,
    GoogleLoginURL,
    logout,
)
from .image_upload import ProfileUploadView
from .posts import Get_Other_Users_Post, Get_Post, Get_User_Post
from .user_credentials import CustomTokenRefreshView, Login, SignupView
from .user_post import (
    CheckLikePost,
    DeletePostView,
    Get_Users,
    LikeUnlikePost,
    PostUploadAPIView,
)

urlpatterns = [
    path("chat/", Home, name="Home"),
    path("auth", AuthChecking.as_view(), name="auth_me"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("user/logout/", logout, name="user_logout"),
    path("api/token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("auth/google/login/", GoogleLoginURL.as_view(), name="google_login_url"),
    path("auth/google/callback/", GoogleCallback.as_view(), name="google_callback_url"),
    path("auth/github/login/", GithubLoginURL.as_view()),
    path("auth/github/callback/", GithubCallback.as_view()),
    path("get/users/", Get_Users.as_view(), name="get_users"),
    path("get/posts/", Get_Post.as_view(), name="get_posts"),
    path("get/user/posts/", Get_User_Post.as_view(), name="get_user_posts"),
    path(
        "get/other/user/posts/",
        Get_Other_Users_Post.as_view(),
        name="get_other_user_posts",
    ),
    path("user/follow/", follow_user, name="user_follower"),
    path("user/unfollow/", unfollow_user, name="user_unfollow"),
    path("user/getfollowers/", get_followers, name="user_get_followers"),
    path("user/getfollowings/", get_followings, name="user_get_followers"),
    path("user/checkfollowing/", check_followings, name="user_check_followers"),
    path(
        "user/profile/upload/", ProfileUploadView.as_view(), name="user_profile_upload"
    ),
    path("user/post/upload/", PostUploadAPIView.as_view(), name="user_post_upload"),
    path("user/post/delete/", DeletePostView.as_view(), name="user_post-delete"),
    path("user/post/like/", LikeUnlikePost.as_view(), name="user_post_like"),
    path(
        "user/post/check/like/<int:post_id>/",
        CheckLikePost.as_view(),
        name="check-like-post",
    ),
    path("user/comment/post/", AddCommentView.as_view(), name="user_post_comment"),
    path("user/comments/get/", GetCommentsView.as_view(), name="user_comments_get"),
    path(
        "user/comment/delete/", DeleteCommentView.as_view(), name="user_delete_comment"
    ),
    path(
        "user/messages/<int:user_id>/",
        Get_User_Messages.as_view(),
        name="get_user_messages",
    ),  # type:ignore
]
