import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    email = "test@user.pl"
    username = "testuser"
    password = "testpass123"
    is_mod = False

    user = User.objects.create_user(
        email=email, username=username, password=password, is_mod=is_mod
    )

    assert user.email == email
    assert user.username == username
    assert user.check_password(password)
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser
    assert user.is_mod == is_mod
