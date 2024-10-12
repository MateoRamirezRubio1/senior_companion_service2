from abc import ABC, abstractmethod
from .models import Reference, TimeAvailability, Certification, Skill


class AbstractReferenceService(ABC):
    @abstractmethod
    def create_reference(self, actualCompanion, form):
        pass

    @abstractmethod
    def get_reference_by_id(self, idReference):
        pass

    @abstractmethod
    def delete_reference(self, actualCompanion, idReference):
        pass

    @abstractmethod
    def validate_email_reference_form(self, form):
        pass

    @abstractmethod
    def get_reference_list_by_companion(self, actualCompanion):
        pass


class ReferenceService(AbstractReferenceService):
    def create_reference(self, actualCompanion, form):
        reference = form.save(commit=False)
        reference.idCompanion = actualCompanion
        reference.save()

    def get_reference_by_id(self, idReference):
        return Reference.objects.get(idReference=idReference)

    def delete_reference(self, actualCompanion, reference):
        if actualCompanion.idCompanion == reference.idCompanion.idCompanion:
            reference.delete()
            return {"type": True, "content": "The reference was successfully deleted."}
        return {
            "type": False,
            "content": "You do not have permission to delete this reference.",
        }

    def validate_email_reference_form(self, form):
        return (
            "A reference with this email already exists."
            if form.errors.get("email")
            else None
        )

    def get_reference_list_by_companion(self, actualCompanion):
        return Reference.objects.filter(idCompanion=actualCompanion.idCompanion)


class AbstractTimeAvailabilityService(ABC):
    @abstractmethod
    def create_time_availability(self, actualCompanion, form):
        pass

    @abstractmethod
    def get_time_availability_by_params(self, date, end_time, start_time):
        pass

    @abstractmethod
    def get_time_availability_by_id(self, idTimeAvailability):
        pass

    @abstractmethod
    def delete_time_availability(self, actualCompanion, idTimeAvailability):
        pass

    @abstractmethod
    def validate_time_availability_exists(self, form):
        pass

    @abstractmethod
    def get_time_availability_list_by_companion(self, actualCompanion):
        pass


class TimeAvailabilityService(ABC):
    def create_time_availability(self, actualCompanion, form):
        timeAv = form.save(commit=False)
        timeAv.idCompanion = actualCompanion
        timeAv.save()

    def get_time_availability_by_params(self, date, end_time, start_time):
        return TimeAvailability.objects.filter(
            date=date, startTime__lte=end_time, endTime__gte=start_time
        )

    def get_time_availability_by_id(self, idTimeAvailability):
        return TimeAvailability.objects.get(idTimeAvailability=idTimeAvailability)

    def delete_time_availability(self, actualCompanion, timeAvailability):
        if actualCompanion.idCompanion == timeAvailability.idCompanion.idCompanion:
            timeAvailability.delete()
            return {
                "type": True,
                "content": "The time availability was successfully deleted.",
            }
        return {
            "type": False,
            "content": "You do not have permission to delete this time availability.",
        }

    def validate_time_availability_exists(self, form):
        date = form.cleaned_data["date"]
        start_time = form.cleaned_data["startTime"]
        end_time = form.cleaned_data["endTime"]

        existing_availability = self.get_time_availability_by_params(
            date, end_time, start_time
        )

        if existing_availability.exists():
            return "Time availability already exists for the specified period."
        else:
            return None

    def get_time_availability_list_by_companion(self, actualCompanion):
        return TimeAvailability.objects.filter(
            idCompanion=actualCompanion.idCompanion
        ).order_by("date", "startTime")


class AbstractSkillService(ABC):
    @abstractmethod
    def create_skill(self, actualCompanion, form):
        pass

    @abstractmethod
    def get_skill_by_id(self, idReference):
        pass

    @abstractmethod
    def delete_skill(self, actualCompanion, idReference):
        pass

    @abstractmethod
    def validate_email_reference_form(self, form):
        pass

    @abstractmethod
    def get_skill_list_by_companion(self, actualCompanion):
        pass


class AbstractCertificationService(ABC):
    @abstractmethod
    def create_certification(self, actualCompanion, form):
        pass

    @abstractmethod
    def get_certification_by_id(self, idCertification):
        pass

    @abstractmethod
    def delete_certification(self, actualCompanion, idReference):
        pass

    @abstractmethod
    def get_certification_list_by_companion(self, actualCompanion):
        pass


class CertificationService(ABC):
    def create_certification(self, actualCompanion, form):
        certification = form.save(commit=False)
        certification.idCompanion = actualCompanion
        certification.save()

    def get_certification_by_id(self, idCertification):
        return Certification.objects.get(idCertification=idCertification)

    def delete_certification(self, actualCompanion, certification):
        # Verify that the user is the owner of the associated companion
        if actualCompanion.idCompanion == certification.idCompanion.idCompanion:
            # Delete the certification
            certification.delete()
            return {
                "type": True,
                "content": "The certification was successfully deleted.",
            }
        return {
            "type": False,
            "content": "You do not have permission to delete this certification.",
        }

    def get_certification_list_by_companion(self, actualCompanion):
        return Certification.objects.filter(idCompanion=actualCompanion.idCompanion)
