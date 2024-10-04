from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from authentication.views import UserRegistrationView, edit_user_profile
from authentication.models import User
from .forms import MedicalInformationForm, PreferenceForm, CustomerUpdateForm
from .decorators import actual_customer_required, inject_service
from .services_factory import ServiceFactory

services_factory = ServiceFactory()
customer_service = services_factory.get_service("CUSTOMER")
preference_service = services_factory.get_service("PREFERENCE")
medical_info_service = services_factory.get_service("MEDICAL_INFO")


def CustomerRegistrationFactory():
    class CustomerRegistrationView(UserRegistrationView):
        """
        View for customer registration, extending UserRegistrationView.

        """

        @inject_service(customer_service)
        def post(self, request, *args, service=None, **kwargs):
            """
            Handle POST request to process customer registration.

            Args:
                request: HTTP request object.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.

            Returns:
                HTTP response based on the success or failure of the registration.
            """
            response = redirect("home")

            try:
                with transaction.atomic():
                    # Ensure atomicity of the database operations
                    response = super().post(request, *args, **kwargs)
                    user = get_object_or_404(User, email=request.POST["email"])
                    service.register_customer(user)
                    messages.success(
                        request, "Customer successfully created, you can now login"
                    )
                    return redirect("home")

            except IntegrityError:
                # Handle case where a customer already exists with the provided email
                messages.error(
                    request, "Error: A Customer with this email already exists."
                )
                return redirect("home")

            except Http404 as e:
                # Handle case where user is not found
                messages.error(request, "User not found.")
                return response
            except Exception as e:
                # Handle any other unforeseen errors
                print(f"An unexpected error occurred: {str(e)}")
                messages.error(request, "An unexpected error occurred")
                return redirect("home")

    return CustomerRegistrationView


@login_required
@actual_customer_required(customer_service)
@inject_service(medical_info_service)
def editCreate_MedicalInformation(request, actualCustomer, service):
    """
    View for editing or creating medical information associated with a customer.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the "editGeneralAllCustomer" page upon successful form submission.
                      Displays error messages if the form is invalid.
    """

    try:
        instanceMedicalInformation = service.get_medical_info_by_customer(
            actualCustomer.idCustomer
        )
    except Exception as e:
        instanceMedicalInformation = None

    if request.method == "POST":
        form = MedicalInformationForm(request.POST, instance=instanceMedicalInformation)
        if form.is_valid():
            try:
                service.save_medical_info(form, actualCustomer)
                messages.success(request, "Correctly updated medical information!")
            except Exception as e:
                # Handle save errors
                messages.error(request, f"Error saving medical information")
        else:
            # Form validation failed
            messages.error(request, "Error in the form. Please correct the errors.")
        return redirect("editGeneralAllCustomer")
    else:
        form = MedicalInformationForm(instance=instanceMedicalInformation)

    return form


@login_required
@actual_customer_required(customer_service)
@inject_service(preference_service)
def create_preference(request, actualCustomer, service):
    """
    View for creating a new preference associated with the current customer.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the "editGeneralAllCustomer" page upon successful form submission.
                      Displays error messages if the form is invalid.
    """

    if request.method == "POST":
        form = PreferenceForm(request.POST)
        if form.is_valid():
            try:
                service.create_preference(form, actualCustomer)
                messages.success(request, "Preference added correctly!")
            except Exception as e:
                # Handle preference creation errors
                messages.error(request, f"Error creating preference")
        else:
            # Form validation failed
            messages.error(request, "Error in the form. Please correct the errors.")
        return redirect("editGeneralAllCustomer")
    else:
        form = PreferenceForm()

    return form


@login_required
@actual_customer_required(customer_service)
@inject_service(preference_service)
def delete_preference(request, idPreference, actualCustomer, service=None):
    """
    View for deleting a preference associated with the current customer.

    Args:
        request (HttpRequest): The HTTP request object.
        idPreference (int): The ID of the preference to delete.
        actualCustomer (Customer): The current customer object.
        service (PreferenceService): The preference service injected.

    Returns:
        HttpResponse: Redirects to the "editGeneralAllCustomer" page upon successful deletion.
                      Displays error messages if the user does not have permission.
    """

    try:
        preference_deleted_message = service.delete_preference(
            idPreference, actualCustomer
        )
        if preference_deleted_message["type"]:
            messages.success(request, preference_deleted_message["content"])
        else:
            messages.error(request, preference_deleted_message["content"])
    except Exception as e:
        # Handle any errors during preference deletion
        messages.error(request, f"Error deleting preference")

    return redirect("editGeneralAllCustomer")


@login_required
@actual_customer_required(customer_service)
def edit_customer(request, actualCustomer):
    """
    Edits customer information based on the provided request.

    Args:
        request (HttpRequest): The HTTP request object.
        actualCustomer (Customer): The current customer instance.

    Returns:
        form: The customer update form.

    Note:
        This function utilizes the Django authentication decorator `@login_required`.
        It handles both GET and POST requests for editing customer information.
    """

    if request.method == "POST":
        # Process the form submission for updating customer information.
        form = CustomerUpdateForm(request.POST, instance=actualCustomer)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Correctly updated personal presentation!")
            except Exception as e:
                # Handle save errors
                messages.error(request, f"Error updating customer")
        else:
            # Display an error message if the form is invalid.
            messages.error(request, "Error in the form. Please correct the errors.")
        # Redirect the user to the customer edit page.
        return redirect("editGeneralAllCustomer")
    else:
        # Display the customer update form for GET requests.
        form = CustomerUpdateForm(instance=actualCustomer)

    return form


@login_required
@actual_customer_required(customer_service)
@inject_service(preference_service)
def edit_general_all_customer(request, actualCustomer, service):
    """
    View for editing general information for all customers.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered HTML page with the necessary forms and data.
    """
    try:
        # Initialize form instances for different sections
        formMedicalInformation = editCreate_MedicalInformation(request)
        formCreatePreference = create_preference(request)
        listPreferenceCustomer = service.get_preferences_by_customer(
            actualCustomer.idCustomer
        )
        formEditUserProfile = edit_user_profile(request)
        formEditCustomer = edit_customer(request)
    except Exception as e:
        # Handle any errors while fetching customer data or forms
        messages.error(request, f"Error loading customer data: {str(e)}")
        return redirect("home")

    # Render the edit_user.html template with form instances and data
    return render(
        request,
        "customer/edit_user_customer.html",
        {
            "formMedicalInformation": formMedicalInformation,
            "formCreatePreference": formCreatePreference,
            "listPreferenceCustomer": listPreferenceCustomer,
            "formEditUserProfile": formEditUserProfile,
            "formEditCustomer": formEditCustomer,
        },
    )
