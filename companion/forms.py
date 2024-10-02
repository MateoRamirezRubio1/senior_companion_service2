from django import forms
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from .models import Reference, TimeAvailability, Skill, Certification, Companion


class ReferenceForm(forms.ModelForm):
    """
    Form for creating and updating Reference model instances.

    Attributes:
        clean_email(): Custom validation to check uniqueness of email.
    """

    class Meta:
        model = Reference
        fields = ["names", "lastNames", "phone", "address", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (
            Reference.objects.filter(email=email)
            .exclude(idReference=self.instance.idReference)
            .exists()
        ):
            raise forms.ValidationError("A reference with this email already exists.")
        return email

    def __init__(self, *args, **kwargs):
        super(ReferenceForm, self).__init__(*args, **kwargs)
        self.fields["phone"].required = False
        self.fields["address"].required = False


class TimeAvailabilityForm(forms.ModelForm):
    """
    Form for creating and updating TimeAvailability model instances.

    Attributes:
        clean_date(): Custom validation to ensure date is not in the past.
        clean(): Custom validation to ensure start time is before end time.
    """

    class Meta:
        model = TimeAvailability
        fields = ["date", "startTime", "endTime"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "startTime": forms.TimeInput(attrs={"type": "time"}),
            "endTime": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean_date(self):
        date = self.cleaned_data.get("date")

        if date and date < timezone.now().date():
            raise forms.ValidationError("Date cannot be in the past.")

        return date

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("startTime")
        end_time = cleaned_data.get("endTime")

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("The start time must be before the end time.")

        return cleaned_data


class CertificationForm(forms.ModelForm):
    """
    Form for creating and updating Certification model instances.

    Attributes:
        clean_certificate(): Custom validation to ensure only PDF files are allowed.
    """

    class Meta:
        model = Certification
        fields = ["description", "certificate"]

    def clean_certificate(self):
        certificate = self.cleaned_data.get("certificate")

        # Verificar el tipo de archivo
        if certificate:
            extension = certificate.name.split(".")[-1].lower()
            if extension != "pdf":
                raise forms.ValidationError("Only PDF files are allowed.")

        return certificate


class SkillForm(forms.ModelForm):
    """
    Form for creating and updating Skill model instances.
    """

    class Meta:
        model = Skill
        fields = ["description"]


class CompanionUpdateForm(forms.ModelForm):
    """
    Form for updating Companion model instances.

    Attributes:
        __init__(): Set personalDescription and hourlyRate fields as not required.
    """

    class Meta:
        model = Companion
        fields = ["personalDescription", "hourlyRate"]

    def __init__(self, *args, **kwargs):
        super(CompanionUpdateForm, self).__init__(*args, **kwargs)
        self.fields["personalDescription"].required = False
        self.fields["hourlyRate"].required = False
