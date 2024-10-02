import bcrypt
from django.db import models
from PIL import Image
import os
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    """
    Custom User model extending AbstractBaseUser.

    Attributes:
        idUser (AutoField): Primary key for the User model.
        names (CharField): User's first name(s).
        lastNames (CharField): User's last name(s).
        password (CharField): Hashed password, using bcrypt for security.
        phone (CharField): User's phone number.
        address (CharField): User's address.
        birthDate (DateField): User's date of birth.
        genre (CharField): User's gender, limited to choices: ['male', 'female', 'other'].
        email (CharField): User's unique email address for identification.
        profilePhoto (CharField): Path to the user's profile photo.
        registrationDate (DateField): Date when the user registered.
        location (CharField): User's current location.
    """

    idUser = models.AutoField(primary_key=True)
    names = models.CharField(max_length=80)
    lastNames = models.CharField(max_length=80)
    password = models.CharField(max_length=255, editable=False)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=60, null=True)
    birthDate = models.DateField(null=True)
    genre = models.CharField(
        max_length=6,
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        null=True,
    )
    email = models.CharField(max_length=60, unique=True, null=False)
    profilePhoto = models.ImageField(upload_to="profile_photos/", null=True)
    registrationDate = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=100, null=True)

    USERNAME_FIELD = "email"

    def save(self, *args, **kwargs):
        """
        Overrides the save method to hash the password before saving.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if not self.idUser and self.password:
            self.password = bcrypt.hashpw(
                self.password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")

        # Remove the previous profile photo before saving the new one
        try:
            old_instance = User.objects.get(pk=self.pk)
            if (
                old_instance.profilePhoto
                and self.profilePhoto != old_instance.profilePhoto
            ):
                if os.path.isfile(old_instance.profilePhoto.path):
                    os.remove(old_instance.profilePhoto.path)
        except User.DoesNotExist:
            pass

        super(User, self).save(*args, **kwargs)

        # Resize and save the profile photo if it exists
        if self.profilePhoto:
            img = Image.open(self.profilePhoto.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profilePhoto.path)


class Language(models.Model):
    """
    Model for representing a language.

    Attributes:
        idLanguage (AutoField): Primary key for the Language model.
        name (CharField): Name of the language, unique.
    """

    idLanguage = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, unique=True)


class LanguageUser(models.Model):
    """
    Model for associating users with languages.

    Attributes:
        idLanguageUser (AutoField): Primary key for the LanguageUser model.
        idUser (ForeignKey): Foreign key linking to the User model.
        idLanguage (ForeignKey): Foreign key linking to the Language model.
    """

    idLanguageUser = models.AutoField(primary_key=True)
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    idLanguage = models.ForeignKey(Language, on_delete=models.CASCADE)
