# seeds.py
import os
import django
import requests
from io import BytesIO
from django.core.files import File
from django.contrib.auth.hashers import make_password
import random

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SocialMedia.settings")
django.setup()

from SocialMediaApp.models import User, Credentials, Post  # adjust your app name


def create_users_and_posts():
    for i in range(1, 6):
        random_user = random.randint(4, 20)
        user = User.objects.create(
            username=f"user{random_user}",
            email=f"user{random_user}@example.com",
            is_active=True,
        )

        Credentials.objects.create(
            user=user,
            auth_id=f"user{random_user}_auth",
            password=make_password("password123"),
            auth_id_by="manual",
        )

        print(f"Created user: {user.username}")

        for j in range(1, 6):
            post = Post.objects.create(
                user=user,
                content=f"This is post {j} by {user.username}",
            )

            # Fetch a random image
            url = f"https://picsum.photos/seed/{user.username}{j}/600/400"
            response = requests.get(url)
            if response.status_code == 200:
                ext = "jpg"
                image_path = f"post-images/{post.pk}.{ext}"
                image_file = File(BytesIO(response.content), name=image_path)
                post.image.save(image_path, image_file, save=True)

            print(f"  → Created post {post.pk} for {user.username}")

    print("Total users:", User.objects.count())
    print("Total posts:", Post.objects.count())


if __name__ == "__main__":
    create_users_and_posts()
