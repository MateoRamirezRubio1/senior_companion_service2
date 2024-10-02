from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration, extending UserCreationForm.

    Attributes:
        user_type (ChoiceField): Field for selecting user type.

    Meta:
        model: User model.
        fields: List of fields to include in the form.
    """

    class Meta:
        model = User
        fields = ["names", "lastNames", "email", "password1", "password2"]


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile information.

    Attributes:
        Meta: Configuration class defining the model and fields for the form.
        widgets: Additional configuration for the 'birthDate' field to use a date input.

    Methods:
        __init__: Initializes the form, setting all fields as not required.

    Note:
        This form is designed for use with the User model and assumes the existence
        of fields like 'names', 'lastNames', 'phone', etc.
    """

    class Meta:
        model = User
        fields = [
            "names",
            "lastNames",
            "phone",
            "address",
            "birthDate",
            "location",
            "profilePhoto",
            "genre",
        ]
        widgets = {
            "birthDate": forms.DateInput(attrs={"type": "date"}),
        }
        profilePhoto = forms.ImageField(required=False, widget=forms.FileInput)

    def __init__(self, *args, **kwargs):
        """
        Initializes the UserProfileForm.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Note:
            Sets all fields in the form as not required to allow empty submissions.
        """
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
