from django.db import models
from authentication.models import User


class Customer(models.Model):
    """
    Model for representing a customer.

    Attributes:
        idCustomer (AutoField): Primary key for the Customer model.
        accountState (CharField): State of the customer's account.
        personalPresentation (TextField): Personal presentation of the customer.
        idUser (OneToOneField): Foreign key linking to the User model.
    """

    idCustomer = models.AutoField(primary_key=True)
    accountState = models.CharField(
        max_length=9,
        choices=[
            ("active", "Active"),
            ("inactive", "Inactive"),
            ("blocked", "Blocked"),
        ],
        null=True,
    )
    personalPresentation = models.TextField(null=True)
    idUser = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        String representation of the Customer model.

        Returns:
            str: Email of the associated user.
        """
        return self.idUser.email


class MedicalInformation(models.Model):
    """
    Model representing medical information related to a customer.

    Attributes:
        idMedicalInformation (AutoField): Primary key for the medical information.
        allergies (TextField): Text field to store information about allergies.
        medicalConditions (TextField): Text field to store information about medical conditions.
        medicationIntake (TextField): Text field to store information about medication taken by the user.
        medicationRestriction (TextField): Text field to store information about medication restrictions.
        emergencyContact (CharField): Char field to store emergency contact information (limited to 15 characters).
        idCustomer (ForeignKey): Foreign key linking to the Customer model, establishing a one-to-one relationship.
    """

    idMedicalInformation = models.AutoField(primary_key=True)
    allergies = models.TextField(null=True)
    medicalConditions = models.TextField(null=True)
    medicationIntake = models.TextField(null=True)
    medicationRestriction = models.TextField(null=True)
    emergencyContact = models.CharField(max_length=15, null=True)
    idCustomer = models.ForeignKey(Customer, on_delete=models.CASCADE, unique=True)


class Preference(models.Model):
    """
    Model representing customer preferences.

    Attributes:
        idPreference (AutoField): Primary key for the preference.
        description (CharField): Char field to store a brief description or name of the preference (limited to 100 characters).
        idCustomer (ForeignKey): Foreign key linking to the Customer model, establishing a many-to-one relationship.
    """

    idPreference = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    idCustomer = models.ForeignKey(Customer, on_delete=models.CASCADE)
