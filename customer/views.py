from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from authentication.views import UserRegistrationView, edit_user_profile
from authentication.models import User
from .models import Customer, MedicalInformation, Preference
from .forms import MedicalInformationForm, PreferenceForm, CustomerUpdateForm


class CustomerRegistrationView(UserRegistrationView):
    """
    View for customer registration, extending UserRegistrationView.

    Attributes:
        None.
    """

    def post(self, request, *args, **kwargs):
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
                response = super().post(request, *args, **kwargs)
                user = get_object_or_404(User, email=request.POST["email"])
                customer = Customer.objects.create(idUser=user, accountState="activo")
                return redirect("home")

        except IntegrityError:
            messages.error(request, "Error: A Customer with this email already exists.")
            return redirect("home")

        except Http404:
            return response


@login_required
def get_actualCustomer(request):
    """
    Get the current customer associated with the logged-in user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Customer: The current customer.
    """
    actualUserId = request.user.idUser
    actualCustomer = get_object_or_404(Customer, idUser=actualUserId)
    return actualCustomer


@login_required
def editCreate_MedicalInformation(request):
    """
    View for editing or creating medical information associated with a customer.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the "editGeneralAllCustomer" page upon successful form submission.
                      Displays error messages if the form is invalid.
    """
    actualCustomer = get_actualCustomer(request)

    try:
        instanceMedicalInformation = MedicalInformation.objects.get(
            idCustomer=actualCustomer.idCustomer
        )
    except MedicalInformation.DoesNotExist:
        instanceMedicalInformation = None

    if request.method == "POST":
        form = MedicalInformationForm(request.POST, instance=instanceMedicalInformation)
        if form.is_valid():
            medicalInfo = form.save(commit=False)
            medicalInfo.idCustomer = actualCustomer
            medicalInfo.save()

            messages.success(request, "¡Correctly updated medical information!")
        else:
            messages.error(request, "Error in the form. Please correct the errors.")
        return redirect("editGeneralAllCustomer")
    else:
        form = MedicalInformationForm(instance=instanceMedicalInformation)

    return form


@login_required
def create_preference(request):
    """
    View for creating a new preference associated with the current customer.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the "editGeneralAllCustomer" page upon successful form submission.
                      Displays error messages if the form is invalid.
    """
    actualCustomer = get_actualCustomer(request)

    if request.method == "POST":
        form = PreferenceForm(request.POST)
        if form.is_valid():
            preference = form.save(commit=False)
            preference.idCustomer = actualCustomer
            preference.save()

            messages.success(request, "¡Preference added correctly!")
        else:
            messages.error(request, "Error in the form. Please correct the errors.")
        return redirect("editGeneralAllCustomer")
    else:
        form = PreferenceForm()

    return form


@login_required
def preference_customer_list(request):
    """
    Get a list of all preferences of a Customer.

    Returns:
        QuerySet: All preferences of a Customer.
    """
    actualCustomer = get_actualCustomer(request)
    preferencesCustomer = Preference.objects.filter(
        idCustomer=actualCustomer.idCustomer
    )
    return preferencesCustomer


@login_required
def delete_preference(request, idPreference):
    """
    View for deleting a preference associated with the current customer.

    Args:
        request (HttpRequest): The HTTP request object.
        id_preference (int): The ID of the preference to delete.

    Returns:
        HttpResponse: Redirects to the "editGeneralAllCustomer" page upon successful deletion.
                      Displays error messages if the user does not have permission.
    """
    actualCustomer = get_actualCustomer(request)
    preference = get_object_or_404(Preference, idPreference=idPreference)

    # Verify that the user is the preference owner
    if actualCustomer.idCustomer == preference.idCustomer.idCustomer:
        preference.delete()
        messages.success(request, "The preference was successfully deleted.")
    else:
        messages.error(request, "You do not have permission to delete this preference.")

    return redirect("editGeneralAllCustomer")


@login_required
def edit_customer(request):
    """
    Edits customer information based on the provided request.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        form: The customer update form.

    Note:
        This function utilizes the Django authentication decorator `@login_required`.
        It handles both GET and POST requests for editing customer information.
    """
    # Retrieve the current customer using a utility function.
    actualCustomer = get_actualCustomer(request)

    if request.method == "POST":
        # Process the form submission for updating customer information.
        form = CustomerUpdateForm(request.POST, instance=actualCustomer)
        if form.is_valid():
            # Save the form changes if valid and display success message.
            form.save()
            messages.success(request, "¡Correctly updated personal presentation!")
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
def edit_general_all_customer(request):
    """
    View for editing general information for all customers.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered HTML page with the necessary forms and data.
    """
    # Initialize form instances for different sections
    formMedicalInformation = editCreate_MedicalInformation(request)
    formCreatePreference = create_preference(request)
    listPreferenceCustomer = preference_customer_list(request)
    formEditUserProfile = edit_user_profile(request)
    formEditCustomer = edit_customer(request)

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
