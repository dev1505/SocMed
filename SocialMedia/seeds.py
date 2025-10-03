# # seeds.py
# import os
# import random
# from io import BytesIO

# import django
# import requests
# from django.contrib.auth.hashers import make_password
# from django.core.files import File

# # Setup Django environment
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SocialMedia.settings")
# django.setup()

# from SocialMediaApp.models import User, Credentials, Post  # Replace with your app name


# def create_users_and_posts():
#     usernames = [
#         "oliviajohnson",
#         "liamsmith",
#         "emmajones",
#         "noahbrown",
#         "avawilliams",
#         "elijahdavis",
#         "sophiamiller",
#         "lucaswilson",
#         "isabellamartin",
#         "masonthomas",
#     ]

#     post_contents = [
#         "Exploring the beauty of nature 🌿✨",
#         "Coffee first, then the world ☕🌍",
#         "Life is short, make every selfie count 📸",
#         "Chasing sunsets and dreams 🌅💭",
#         "Adventures are the best way to learn 🚀🌄",
#         "Good vibes only ✌️💛",
#         "Books, coffee, and a cozy corner 📚☕",
#         "Creativity takes courage 🎨🖌️",
#         "Smile, it confuses people 😄🤷‍♂️",
#         "Sometimes the best therapy is a long walk 🌳👣",
#         "Sunshine mixed with a little bit of sass ☀️😉",
#         "Travel far enough to meet yourself ✈️🌍",
#         "Happiness is homemade 🏡💖",
#         "Let the adventure begin 🚣‍♂️🏞️",
#         "Keep going, keep growing 🌱🌸",
#         "Music is the soundtrack of life 🎶💫",
#         "A picture is worth a thousand words 📷🖋️",
#         "Collect moments, not things 🌅🗺️",
#         "Dream big, hustle harder 💪🌟",
#         "Nature does not hurry, yet everything is accomplished 🌿🌳",
#         "Good friends, good times, good vibes 🤗🥳",
#         "Life is better when you’re laughing 😄🌈",
#         "Be fearless in the pursuit of what sets your soul on fire 🔥💖",
#         "Escape the ordinary, embrace the extraordinary 🌌✨",
#         "Every sunset brings the promise of a new dawn 🌄🌞",
#     ]

#     for username in usernames:
#         # Create User
#         user = User.objects.create(
#             username=username, email=f"{username}@example.com", is_active=True
#         )

#         # Create Credentials
#         Credentials.objects.create(user=user, password=make_password("Password@123"))

#         print(f"Created user: {user.username}")

#         # Create 10 posts per user
#         for i in range(10):
#             post = Post.objects.create(user=user, content=random.choice(post_contents))

#             # Fetch high-res image
#             url = f"https://picsum.photos/2000/2600?random={random.randint(1, 10000)}"
#             response = requests.get(url)
#             if response.status_code == 200:
#                 ext = "jpg"
#                 image_path = f"post-images/{post.pk}.{ext}"
#                 image_file = File(BytesIO(response.content), name=image_path)
#                 post.image.save(image_path, image_file, save=True)

#             print(f"  → Created post {post.pk} for {user.username}")

#     print("✅ Seeding complete!")
#     print("Total users:", User.objects.count())
#     print("Total posts:", Post.objects.count())


# if __name__ == "__main__":
#     create_users_and_posts()


# seeds.py
import os
import random
from io import BytesIO

import django
import requests
from django.contrib.auth.hashers import make_password
from django.core.files import File

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SocialMedia.settings")
django.setup()

from SocialMediaApp.models import User, Credentials, Post  # Replace with your app name


def create_users_and_posts():
    users = User.objects.all()

    for i in range(len(users)):
        url = f"https://picsum.photos/2000/2600?random={random.randint(1, 10000)}"
        response = requests.get(url)
        if response.status_code == 200:
            ext = "jpg"
            image_path = f"profile-pic/{users[i].pk}.{ext}"
            image_file = File(BytesIO(response.content), name=image_path)
            users[i].profile_pic = url
            users[i].profile_pic.save(image_path, image_file, save=True)

    print("✅ Seeding complete!")
    print("Total users:", User.objects.count())
    print("Total posts:", Post.objects.count())


if __name__ == "__main__":
    create_users_and_posts()
