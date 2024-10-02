from django.db import models
from authentication.models import User
from django.core.validators import FileExtensionValidator


class Companion(models.Model):
    """
    Model for representing a companion.

    Attributes:
        idCompanion (AutoField): Primary key for the Companion model.
        stateAvailability (CharField): Availability state of the companion.
        hourlyRate (DecimalField): Hourly rate of the companion.
        personalDescription (TextField): Personal description of the companion.
        idUser (OneToOneField): Foreign key linking to the User model.
    """

    idCompanion = models.AutoField(primary_key=True)
    stateAvailability = models.CharField(
        max_length=15,
        choices=[
            ("available", "Available"),
            ("not available", "Not Available"),
            ("pause", "Pause"),
            ("blocked", "Blocked"),
        ],
        null=True,
    )
    hourlyRate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    personalDescription = models.TextField(null=True)
    idUser = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        String representation of the Companion model.

        Returns:
            str: Email of the associated user.
        """
        return self.idUser.email


class Certification(models.Model):
    """
    Model to represent certifications associated with a Companion.

    Attributes:
        idCertification (AutoField): Primary key for Certification.
        description (CharField): Description of the certification.
        certificate (FileField): File field for the certificate (PDF format).
        idCompanion (ForeignKey): Foreign key relation to the Companion model.
    """

    idCertification = models.AutoField(primary_key=True)
    description = models.CharField(max_length=45)
    certificate = models.FileField(
        upload_to="certificates/", validators=[FileExtensionValidator(["pdf"])]
    )
    idCompanion = models.ForeignKey(Companion, on_delete=models.CASCADE)


class Reference(models.Model):
    """
    Model to represent references associated with a Companion.

    Attributes:
        idReference (AutoField): Primary key for Reference.
        names (CharField): Names of the reference.
        lastNames (CharField): Last names of the reference.
        phone (CharField): Phone number of the reference.
        address (CharField): Address of the reference.
        email (CharField): Email of the reference (unique).
        idCompanion (ForeignKey): Foreign key relation to the Companion model.
    """

    idReference = models.AutoField(primary_key=True)
    names = models.CharField(max_length=80, null=True)
    lastNames = models.CharField(max_length=80, null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=60, null=True)
    email = models.CharField(max_length=60, unique=True, null=True)
    idCompanion = models.ForeignKey(Companion, on_delete=models.CASCADE)


class TimeAvailability(models.Model):
    """
    Model to represent time availability associated with a Companion.

    Attributes:
        idTimeAvailability (AutoField): Primary key for TimeAvailability.
        date (DateField): Date for availability.
        startTime (TimeField): Start time for availability.
        endTime (TimeField): End time for availability.
        idCompanion (ForeignKey): Foreign key relation to the Companion model.
    """

    idTimeAvailability = models.AutoField(primary_key=True)
    date = models.DateField(null=True)
    startTime = models.TimeField(null=True)
    endTime = models.TimeField(null=True)
    idCompanion = models.ForeignKey(Companion, on_delete=models.CASCADE)


class Skill(models.Model):
    """
    Model to represent skills associated with a Companion.

    Attributes:
        idSkill (AutoField): Primary key for Skill.
        description (CharField): Description of the skill.
        idCompanion (ForeignKey): Foreign key relation to the Companion model.
    """

    idSkill = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    idCompanion = models.ForeignKey(Companion, on_delete=models.CASCADE)
