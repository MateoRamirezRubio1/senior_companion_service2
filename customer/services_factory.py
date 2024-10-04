from .services import CustomerService, PreferenceService, MedicalInformationService
from .repositories import (
    CustomerRepository,
    PreferenceRepository,
    MedicalInformationRepository,
)


class ServiceFactory:
    """
    Factory to create instances of services with their associated repositories.
    """

    def get_service(self, service_type: str):
        """
        Returns the appropriate service based on the specified type.

        Args:
            service_type (str): The type of service to create.

        Returns:
            An instance of the requested service with its associated repository.

        Raises:
            ValueError: If the service_type is not supported.
        """

        services = {
            "CUSTOMER": lambda: CustomerService(CustomerRepository()),
            "PREFERENCE": lambda: PreferenceService(PreferenceRepository()),
            "MEDICAL_INFO": lambda: MedicalInformationService(
                MedicalInformationRepository()
            ),
        }

        if service_type not in services:
            raise ValueError(f"The service type '{service_type}' is not supported.")

        return services[service_type]()
