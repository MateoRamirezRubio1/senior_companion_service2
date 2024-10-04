from abc import ABC, abstractmethod
from .models import Customer, MedicalInformation, Preference
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class AbstractCustomerRepository(ABC):
    """
    Interface for the Customer repository.
    Defines the abstract methods that must be implemented by concrete repositories.
    """

    @abstractmethod
    def get_by_user_id(self, user_id):
        """Gets a customer by the user ID."""
        pass

    @abstractmethod
    def create(self, user):
        """Creates a new customer."""
        pass


class CustomerRepository(AbstractCustomerRepository):
    """Concrete repository that implements AbstractCustomerRepository using Django ORM."""

    def __init__(self, model=Customer):
        self.model = model

    def get_by_user_id(self, user_id):
        """Implements the method to retrieve a customer by user ID."""
        try:
            return self.model.objects.get(idUser=user_id)
        except self.model.DoesNotExist:
            # Return None if the customer does not exist
            return None
        except Exception as e:
            # Log or handle the unexpected exception here
            raise RuntimeError(
                f"An error occurred while fetching the customer: {str(e)}"
            )

    def create(self, user):
        """Implements the method to create a new customer."""
        try:
            return self.model.objects.create(idUser=user, accountState="active")
        except ValidationError as ve:
            # Handle validation errors raised by the model
            raise ValueError(
                f"Validation error occurred while creating a customer: {str(ve)}"
            )
        except Exception as e:
            # Log or handle the unexpected exception here
            raise RuntimeError(f"An error occurred while creating a customer: {str(e)}")


class AbstractMedicalInformationRepository(ABC):
    @abstractmethod
    def get_by_customer_id(self, customer_id):
        """Gets medical information by customer ID."""
        pass

    @abstractmethod
    def save(self, form_medical_information, actual_customer):
        """Saves medical information for a customer."""
        pass


class MedicalInformationRepository(AbstractMedicalInformationRepository):
    """Concrete repository that implements AbstractMedicalInformationRepository using Django ORM."""

    def __init__(self, model=MedicalInformation):
        self.model = model

    def get_by_customer_id(self, customer_id):
        """Retrieves medical information by customer ID."""
        try:
            return self.model.objects.get(idCustomer=customer_id)
        except ObjectDoesNotExist:
            # Return None if medical information does not exist
            return None
        except Exception as e:
            # Log or handle the unexpected exception here
            raise RuntimeError(
                f"An error occurred while fetching medical information: {str(e)}"
            )

    def save(self, form_medical_information, actual_customer):
        """Saves medical information associated with the current customer."""
        try:
            medical_info = form_medical_information.save(commit=False)
            medical_info.idCustomer = actual_customer
            medical_info.save()
        except ValidationError as ve:
            # Handle validation errors raised by the model
            raise ValueError(
                f"Validation error occurred while saving medical information: {str(ve)}"
            )
        except Exception as e:
            # Log or handle the unexpected exception here
            raise RuntimeError(
                f"An error occurred while saving medical information: {str(e)}"
            )


class AbstractPreferenceRepository(ABC):
    @abstractmethod
    def get_by_customer_id(self, customer):
        """Gets preferences by customer."""
        pass

    @abstractmethod
    def get_preference_by_id(self, preference_id):
        """Gets a preference by its ID."""
        pass

    @abstractmethod
    def create(self, preference):
        """Creates a new preference."""
        pass

    @abstractmethod
    def delete(self, preference):
        """Deletes a preference."""
        pass


class PreferenceRepository(AbstractPreferenceRepository):
    """Concrete repository that implements AbstractPreferenceRepository using Django ORM."""

    def __init__(self, model=Preference):
        self.model = model

    def get_by_customer_id(self, customer_id):
        """Retrieves preferences associated with a customer."""
        try:
            return self.model.objects.filter(idCustomer=customer_id)
        except Exception as e:
            # Log or handle the unexpected exception here
            raise RuntimeError(
                f"An error occurred while fetching preferences: {str(e)}"
            )

    def get_preference_by_id(self, preference_id):
        """Retrieves a preference by its ID."""
        try:
            return self.model.objects.get(idPreference=preference_id)
        except ObjectDoesNotExist:
            # Return None if the preference does not exist
            return None
        except Exception as e:
            # Log or handle the unexpected exception here
            raise RuntimeError(
                f"An error occurred while fetching the preference: {str(e)}"
            )

    def create(self, preference_form, actualCustomer):
        """Creates a new preference associated with the current customer."""
        try:
            preference = preference_form.save(commit=False)
            preference.idCustomer = actualCustomer
            preference.save()
        except ValidationError as ve:
            # Handle validation errors raised by the model
            raise ValueError(
                f"Validation error occurred while creating a preference: {str(ve)}"
            )
        except Exception as e:
            # Log or handle the unexpected exception here
            raise RuntimeError(
                f"An error occurred while creating a preference: {str(e)}"
            )

    def delete(self, preference):
        """Deletes a specified preference."""
        try:
            preference.delete()
        except Exception as e:
            # Log or handle the unexpected exception here
            raise RuntimeError(
                f"An error occurred while deleting the preference: {str(e)}"
            )
