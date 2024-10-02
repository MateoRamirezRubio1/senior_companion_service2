import bcrypt
from django.contrib.auth.backends import ModelBackend
from .models import User

class EmailPasswordAuthBackend(ModelBackend):
    """
    Custom authentication backend for authenticating users using email and password stored in the database.
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        """
        Authenticates the user using the provided email and password.

        Args:
            request: The current HTTP request.
            email: User's email.
            password: User's password.

        Returns:
            A user object if authentication is successful.
            None if authentication fails.
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        else:
            return None

    def get_user(self, user_id):
        """
        Gets a user object based on its ID.

        Args:
            user_id: ID of the user.

        Returns:
            A user object if it exists.
            None if the user does not exist.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
