from django import forms
from .models import MedicalInformation, Preference, Customer


class MedicalInformationForm(forms.ModelForm):
    """
    Form class for collecting and validating medical information related to a customer.

    Meta:
        model (MedicalInformation): Specifies the model associated with the form.
        fields (list): A special value "__all__" indicates that all fields in the model should be included in the form.
        exclude (list): Specifies the fields to be excluded from the form ("idMedicalInformation", "idCustomer").

    """

    class Meta:
        model = MedicalInformation
        fields = "__all__"
        exclude = ["idMedicalInformation", "idCustomer"]

    def __init__(self, *args, **kwargs):
        """
        Initializes the MedicalInformationForm.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Note:
            Sets all fields in the form as not required to allow empty submissions.
        """
        super(MedicalInformationForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class PreferenceForm(forms.ModelForm):
    """
    Form class for collecting and validating customer preferences.

    Meta:
        model (Preference): Specifies the model associated with the form.
        fields (list): Specifies the fields to be included in the form ("description").

    """

    class Meta:
        model = Preference
        fields = ["description"]


class CustomerUpdateForm(forms.ModelForm):
    """
    Meta class for CustomerUpdateForm, specifying the model and fields to include.
    """

    class Meta:
        model = Customer
        fields = ["personalPresentation"]
