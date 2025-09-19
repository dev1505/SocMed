from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .authentication import get_tokens_for_user
from .hash import check_hashed_password, hash_password
from .models import Credentials, Followers, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:  # type:ignore
        model = User
        fields = ["id", "username", "email", "profile_pic", "is_deleted", "is_active"]


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
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
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            profile_pic=validated_data.get("profile_pic", None),
            is_active=True,
            is_deleted=False,
        )
        hashed_password = hash_password(validated_data["password"])
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
