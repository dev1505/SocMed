from django.contrib.auth.hashers import check_password, make_password


def hash_password(password):
    hashed_password = make_password(password=password)
    return hashed_password


def check_hashed_password(input_password, hashed_password):
    return check_password(input_password, hashed_password)
