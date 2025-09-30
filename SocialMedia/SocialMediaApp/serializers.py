from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .authentication import get_tokens_for_user
from .hash import check_hashed_password, hash_password
from .models import Comment, Credentials, Followers, Post, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:  # type:ignore
        model = User
        fields = [
            "id",
            "username",
            "email",
            "bio",
            "profile_pic",
            "is_deleted",
            "is_active",
        ]


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    profile_pic = serializers.ImageField(required=False, allow_null=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        profile_pic = validated_data.pop("profile_pic", None)

        user = User.objects.create(
            profile_pic=profile_pic,
            is_active=True,
            is_deleted=False,
            **validated_data,
        )

        hashed_password = hash_password(password)
        Credentials.objects.create(
            user=user,
            password=hashed_password,
            auth_id="",
        )
        return user


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        if not email or not password:
            raise serializers.ValidationError(
                "Email and password required if auth_id not provided."
            )
        try:
            user = User.objects.get(email=email)
            if not user.is_active or user.is_deleted:
                raise serializers.ValidationError("User is inactive or deleted.")
            creds = Credentials.objects.get(user=user)
            if not creds.password or not check_hashed_password(
                password, creds.password
            ):
                raise serializers.ValidationError("Invalid email or password.")
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")
        except Credentials.DoesNotExist:
            raise serializers.ValidationError("User credentials not found.")

        data = get_tokens_for_user(user=user)
        data["user"] = {  # type: ignore
            "id": user.id,  # type: ignore
            "username": user.username,
            "email": user.email,
        }
        return data


class SocialLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(required=False, allow_blank=True)
    auth_id = serializers.CharField()
    auth_id_by = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username") or email.split("@")[0]
        auth_id = attrs.get("auth_id")
        auth_id_by = attrs.get("auth_id_by")

        with transaction.atomic():
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": username,
                    "is_active": True,
                    "is_deleted": False,
                },
            )

            Credentials.objects.get_or_create(
                user=user,
                auth_id=auth_id,
                auth_id_by=auth_id_by,
                defaults={"password": None},
            )

        if not user.is_active or user.is_deleted:
            raise serializers.ValidationError("User is inactive or deleted.")

        data = get_tokens_for_user(user)
        data["user"] = {  # type:ignore
            "id": user.id,  # type:ignore
            "username": user.username,
            "email": user.email,
        }

        return data


def get_current_user(user):
    return UserSerializer(user).data


class FollowSerializer(serializers.ModelSerializer):
    following = serializers.IntegerField(required=True)

    class Meta:  # type:ignore
        model = Followers
        fields = ["follower", "following"]
        read_only_fields = ["follower"]

    def validate(self, attrs):
        follower = self.context["request"].user
        following = attrs.get("following")

        if follower.id == following:
            raise serializers.ValidationError("Self following is not allowed")

        if not User.objects.filter(pk=following).exists():
            raise serializers.ValidationError("No such user found")

        if Followers.objects.filter(follower=follower.id, following=following).exists():
            raise serializers.ValidationError("You are already following this user")

        attrs["follower"] = follower
        return attrs


class UnFollowSerializer(serializers.ModelSerializer):
    following = serializers.IntegerField(required=True)

    class Meta:  # type:ignore
        model = Followers
        fields = ["follower", "following"]
        read_only_fields = ["follower"]

    def validate(self, attrs):
        follower = self.context["request"].user
        following = attrs.get("following")

        if follower.id == following:
            raise serializers.ValidationError("Self unfollowing is not allowed")

        if not User.objects.filter(pk=following).exists():
            raise serializers.ValidationError("No such user found")

        if not Followers.objects.filter(
            follower=follower.id, following=following
        ).exists():
            raise serializers.ValidationError("You are not following this user")

        attrs["follower"] = follower
        return attrs


class GetUserFollowers_FollowingSerializer(serializers.ModelSerializer):
    class Meta:  # type:ignore
        model = User
        fields = ["id", "username", "profile_pic"]


class UserAvatarSerializer(serializers.ModelSerializer):
    class Meta:  # type:ignore
        model = User
        fields = ["id", "profile_pic"]


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    liked_by = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:  # type: ignore
        model = Post
        fields = [
            "id",
            "user",
            "content",
            "image",
            "liked_by",
            "likes_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "user",
            "liked_by",
            "likes_count",
            "created_at",
            "updated_at",
        ]

    def get_likes_count(self, obj):
        return obj.liked_by.count()


class GetUserRequiredInfoSerializers(serializers.ModelSerializer):
    class Meta:  # type: ignore
        model = User
        fields = ["id", "username", "profile_pic"]


class GetPostSerializer(serializers.ModelSerializer):
    user = GetUserRequiredInfoSerializers(read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:  # type: ignore
        model = Post
        fields = [
            "id",
            "user",
            "content",
            "image",
            "liked_by",
            "created_at",
            "updated_at",
            "is_liked",
        ]

    def get_is_liked(self, obj):
        request = self.context.get("request")
        return obj.liked_by.filter(id=request.user.pk).exists()


class GetPostByIdSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(required=True, allow_null=False)


class LikePostSerializer(serializers.Serializer):
    post_id = serializers.IntegerField(required=True, allow_null=False)
    liked_by = serializers.IntegerField(required=True, allow_null=False)
    likes_count = serializers.SerializerMethodField(read_only=True)

    def get_likes_count(self, obj):
        return obj.liked_by.count()


class CommentSerializer(serializers.ModelSerializer):
    user = GetUserRequiredInfoSerializers(read_only=True)

    class Meta:  # type: ignore
        model = Comment
        fields = [
            "id",
            "user",
            "post",
            "content",
            "created_at",
            "updated_at",
        ]


class DeleteCommentSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField(required=True, allow_null=False)


class GetCommentsSerializer(serializers.ModelSerializer):
    user = GetUserRequiredInfoSerializers(read_only=True)

    class Meta:  # type: ignore
        model = Comment
        fields = [
            "id",
            "user",
            "post",
            "content",
            "created_at",
            "updated_at",
        ]

        read_only_fields = ["user", "content"]
