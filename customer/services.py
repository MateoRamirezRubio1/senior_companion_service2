from abc import ABC, abstractmethod
from .repositories import (
    AbstractCustomerRepository,
    AbstractMedicalInformationRepository,
    AbstractPreferenceRepository,
)
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class AbstractCustomerService(ABC):
    @abstractmethod
    def register_customer(self, user):
        """Registers a new customer."""
        pass

    @abstractmethod
    def get_customer_by_user_id(self, user_id):
        """Retrieves a customer associated with the given user ID."""
        pass


class CustomerService(AbstractCustomerService):
    """
    Service to manage business logic related to Customer.
    """

    def __init__(self, customer_repository: AbstractCustomerRepository):
        self.customer_repository = customer_repository

    def register_customer(self, user):
        """
        Registers a new customer.

        Args:
            user (User): The user object to register.

        Returns:
            Customer: The created customer instance.
        """
        try:
            return self.customer_repository.create(user)
        except ValidationError as ve:
            raise ValueError(
                f"Validation error occurred while registering customer: {str(ve)}"
            )
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while registering customer: {str(e)}"
            )

    def get_customer_by_user_id(self, user_id):
        """
        Retrieves the customer associated with the user.

        Args:
            user_id (int): The user ID to look for.

        Returns:
            Customer or None: The customer instance or None if not found.
        """
        try:
            return self.customer_repository.get_by_user_id(user_id)
        except Exception as e:
            raise RuntimeError(f"An error occurred while fetching customer: {str(e)}")


class AbstractMedicalInformationService(ABC):
    @abstractmethod
    def get_medical_info_by_customer(self, customer_id):
        """Retrieves medical information associated with the customer."""
        pass

    @abstractmethod
    def save_medical_info(self, medical_info):
        """Saves medical information for a customer."""
        pass


class MedicalInformationService(AbstractMedicalInformationService):
    """
    Service to manage medical information related to customers.
    """

    def __init__(self, medical_info_repository: AbstractMedicalInformationRepository):
        self.medical_info_repository = medical_info_repository

    def get_medical_info_by_customer(self, customer_id):
        """
        Retrieves medical information by customer ID.

        Args:
            customer_id (int): The customer ID to look for.

        Returns:
            MedicalInformation or None: The medical information instance or None if not found.
        """
        try:
            return self.medical_info_repository.get_by_customer_id(customer_id)
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while fetching medical information: {str(e)}"
            )

    def save_medical_info(self, form_medical_information, actual_customer):
        """
        Saves medical information for the specified customer.

        Args:
            form_medical_information: The form containing medical information.
            actual_customer (Customer): The customer for whom to save the information.
        """
        try:
            self.medical_info_repository.save(form_medical_information, actual_customer)
        except ValidationError as ve:
            raise ValueError(
                f"Validation error occurred while saving medical information: {str(ve)}"
            )
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while saving medical information: {str(e)}"
            )


class AbstractPreferenceService(ABC):
    @abstractmethod
    def get_preferences_by_customer(self, customer_id):
        """Retrieves preferences associated with the customer."""
        pass

    @abstractmethod
    def create_preference(self, preference_form, actualCustomer):
        """Creates a new preference for a customer."""
        pass

    @abstractmethod
    def delete_preference(self, preference_id, actualCustomer):
        """Deletes a customer's preference if the actual customer is the owner."""
        pass


class PreferenceService(AbstractPreferenceService):
    """
    Service to manage customer preferences.
    """

    def __init__(self, preference_repository: AbstractPreferenceRepository):
        self.preference_repository = preference_repository

    def get_preferences_by_customer(self, customer_id):
        """
        Retrieves preferences associated with a customer.

        Args:
            customer_id (int): The customer ID to look for.

        Returns:
            QuerySet: The preferences associated with the customer.
        """
        try:
            return self.preference_repository.get_by_customer_id(customer_id)
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while fetching preferences: {str(e)}"
            )

    def create_preference(self, preference_form, actualCustomer):
        """
        Creates a new preference for the current customer.

        Args:
            preference_form: The form containing preference data.
            actualCustomer (Customer): The customer for whom to create the preference.
        """
        try:
            self.preference_repository.create(preference_form, actualCustomer)
        except ValidationError as ve:
            raise ValueError(
                f"Validation error occurred while creating preference: {str(ve)}"
            )
        except Exception as e:
            raise RuntimeError(f"An error occurred while creating preference: {str(e)}")

    def delete_preference(self, preference_id, actualCustomer):
        """
        Deletes a customer preference if the actual customer is the owner.

        Args:
            preference_id (int): ID of the preference to delete.
            actualCustomer (Customer): The customer requesting the deletion.

        Returns:
            dict: A message indicating success or failure.
        """
        # Constant messages for reuse and maintainability
        SUCCESS_MESSAGE = "The preference was successfully deleted."
        PERMISSION_DENIED_MESSAGE = (
            "You do not have permission to delete this preference."
        )
        PREFERENCE_NOT_FOUND_MESSAGE = "Preference does not exist."
        ERROR_DELETING_PREFERENCE = "Error deleting preference."

        try:
            # Fetch the preference by its ID
            preference = self.preference_repository.get_preference_by_id(preference_id)

            # Verify that the user is the preference owner
            if actualCustomer.idCustomer == preference.idCustomer.idCustomer:
                self.preference_repository.delete(preference)
                return {"type": True, "content": SUCCESS_MESSAGE}

            # If not the owner, return a permission denied message
            return {"type": False, "content": PERMISSION_DENIED_MESSAGE}

        except ObjectDoesNotExist:
            # Return a message if the preference does not exist
            return {"type": False, "content": PREFERENCE_NOT_FOUND_MESSAGE}

        except Exception as e:
            # Handle unexpected exceptions
            print(f"Error deleting preference: {str(e)}")
            return {"type": False, "content": ERROR_DELETING_PREFERENCE}
