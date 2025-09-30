from .models import Followers, User


def follow_user_creation(follower, following):
    Followers.objects.create(follower_id=follower, following_id=following)


def follow_user_deletion(follower, following):
    Followers.objects.filter(follower_id=follower, following_id=following).delete()


def get_user_followers(following):
    return User.objects.filter(follower__following_id=following)


def get_user_followings(follower):
    return User.objects.filter(following__follower_id=follower)


def check_user_following(user_id):
    return User.objects.filter(follower__following_id=user_id).exists()
