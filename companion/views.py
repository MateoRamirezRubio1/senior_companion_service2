from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from authentication.views import UserRegistrationView, edit_user_profile
from authentication.models import User
from .models import Companion, Certification, Reference, TimeAvailability, Skill
from .forms import (
    ReferenceForm,
    TimeAvailabilityForm,
    CertificationForm,
    SkillForm,
    CompanionUpdateForm,
)


class CompanionRegistrationView(UserRegistrationView):
    """
    View for companion registration, extending UserRegistrationView.

    Attributes:
        None.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to process companion registration.

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
                companion = Companion.objects.create(
                    idUser=user, stateAvailability="available"
                )
                return redirect("home")

        except IntegrityError:
            messages.error(
                request, "Error: A Companion with this email already exists."
            )
            return redirect("home")

        except Http404:
            return response


@login_required
def get_actualCompanion(request):
    """
    Get the current companion associated with the logged-in user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Companion: The current companion.
    """
    actualUserId = request.user.idUser
    actualCompanion = get_object_or_404(Companion, idUser=actualUserId)
    return actualCompanion


@login_required
def reference_companion_list(request):
    """
    Get a list of all references of a Companion.

    Returns:
        QuerySet: All references of a Companion.
    """
    actualCompanion = get_actualCompanion(request)
    referencesCompanion = Reference.objects.filter(
        idCompanion=actualCompanion.idCompanion
    )
    return referencesCompanion


@login_required
def delete_reference(request, idReference):
    """
    View for deleting a reference associated with the current companion.

    Args:
        request (HttpRequest): The HTTP request object.
        idReference (int): The ID of the reference to delete.

    Returns:
        HttpResponse: Redirects to the "editGeneralAllCompanion" page upon successful deletion.
                      Displays error messages if the user does not have permission.
    """
    actualCompanion = get_actualCompanion(request)
    reference = get_object_or_404(Reference, idReference=idReference)

    # Verify that the user is the preference owner
    if actualCompanion.idCompanion == reference.idCompanion.idCompanion:
        reference.delete()
        messages.success(request, "The reference was successfully deleted.")
    else:
        messages.error(request, "You do not have permission to delete this reference.")

    return redirect("editGeneralAllCompanion")


@login_required
def create_reference(request):
    """
    View function for creating a new reference associated with the current companion.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the 'editGeneralAllCompanion' page with appropriate messages.

    """
    actualCompanion = get_actualCompanion(request)

    if request.method == "POST":
        # Process POST request to save a new reference
        form = ReferenceForm(request.POST)

        if form.is_valid():
            # Valid form submission
            reference = form.save(commit=False)
            reference.idCompanion = actualCompanion
            reference.save()

            messages.success(request, "¡Reference added correctly!")
        else:
            # Invalid form submission
            email_errors = form.errors.get("email")

            if email_errors:
                messages.error(request, "A reference with this email already exists.")
            else:
                messages.error(request, "Error in the form. Please correct the errors.")

        return redirect("editGeneralAllCompanion")
    else:
        # Render the form for a GET request
        form = ReferenceForm()

    return form


@login_required
def time_availability_list(request):
    """
    View function for retrieving a list of time availabilities associated with the current companion.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        QuerySet: A queryset of TimeAvailability objects filtered by the current companion's ID, ordered by date and start time.

    """
    actualCompanion = get_actualCompanion(request)
    time_availabilities = TimeAvailability.objects.filter(
        idCompanion=actualCompanion.idCompanion
    ).order_by("date", "startTime")

    return time_availabilities


@login_required
def create_time_availability(request):
    """
    View function for creating a new time availability entry associated with the current companion.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse or TimeAvailabilityForm: If the request method is POST, redirects to the 'editGeneralAllCompanion' page with appropriate messages.
        If the request method is GET, returns the TimeAvailabilityForm for rendering.

    """
    actualCompanion = get_actualCompanion(request)

    if request.method == "POST":
        form = TimeAvailabilityForm(request.POST)
        if form.is_valid():
            # Validate if a TimeAvailability already exists with the same date and times
            date = form.cleaned_data["date"]
            start_time = form.cleaned_data["startTime"]
            end_time = form.cleaned_data["endTime"]

            existing_availability = TimeAvailability.objects.filter(
                date=date, startTime__lte=end_time, endTime__gte=start_time
            )

            if existing_availability.exists():
                messages.error(
                    request,
                    "Time availability already exists for the specified period.",
                )
            else:
                timeAv = form.save(commit=False)
                timeAv.idCompanion = actualCompanion
                timeAv.save()

                messages.success(request, "Time availability added successfully!")
        else:
            # Invalid form submission
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")
            else:
                messages.error(request, "Error in the form. Please correct the errors.")

        return redirect("editGeneralAllCompanion")
    else:
        # Render the form for a GET request
        form = TimeAvailabilityForm()

    return form


@login_required
def delete_time_availability(request, idTimeAvailability):
    """
    View function for deleting a time availability entry associated with the current companion.

    Args:
        request (HttpRequest): The HTTP request object.
        id_time_availability (int): The ID of the time availability entry to be deleted.

    Returns:
        HttpResponse: Redirects to the 'editGeneralAllCompanion' page with appropriate messages.

    """
    actualCompanion = get_actualCompanion(request)
    timeAvailability = get_object_or_404(
        TimeAvailability, idTimeAvailability=idTimeAvailability
    )

    # Verify that the user is the preference owner
    if actualCompanion.idCompanion == timeAvailability.idCompanion.idCompanion:
        timeAvailability.delete()
        messages.success(request, "The time availability was successfully deleted.")
    else:
        messages.error(
            request, "You do not have permission to delete this time availability."
        )

    return redirect("editGeneralAllCompanion")


@login_required
def create_certification(request):
    """
    View function for creating a new certification entry associated with the current companion.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse or CertificationForm: If the request method is POST, redirects to the 'editGeneralAllCompanion' page with appropriate messages.
        If the request method is GET, returns the CertificationForm for rendering.

    """
    actualCompanion = get_actualCompanion(request)

    if request.method == "POST":
        # Process POST request to save a new certification entry
        form = CertificationForm(request.POST, request.FILES)

        if form.is_valid():
            certification = form.save(commit=False)
            certification.idCompanion = actualCompanion
            certification.save()

            messages.success(request, "¡Certification added correctly!")
        else:
            # Invalid form submission
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field.capitalize()}: {error}")
            else:
                messages.error(request, "Error in the form. Please correct the errors.")

        return redirect("editGeneralAllCompanion")
    else:
        # Render the form for a GET request
        form = CertificationForm()

    return form


@login_required
def certifications_companion_list(request):
    """
    View function for retrieving a list of certifications associated with the current companion.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        QuerySet: A queryset of Certification objects filtered by the current companion's ID.

    """
    actualCompanion = get_actualCompanion(request)
    certifications = Certification.objects.filter(
        idCompanion=actualCompanion.idCompanion
    )
    return certifications


@login_required
def delete_certification(request, idCertification):
    """
    View function to handle the deletion of a certification associated with a companion.

    Args:
        request (HttpRequest): The request object.
        idCertification (int): The ID of the certification to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the "editGeneralAllCompanion" view.

    Raises:
        Http404: If the specified certification is not found.
    """
    # Retrieve the current companion from the request
    actualCompanion = get_actualCompanion(request)

    # Retrieve the certification object or raise a 404 error if not found
    certification = get_object_or_404(Certification, idCertification=idCertification)

    # Verify that the user is the owner of the associated companion
    if actualCompanion.idCompanion == certification.idCompanion.idCompanion:
        # Delete the certification
        certification.delete()
        messages.success(request, "The certification was successfully deleted.")
    else:
        # Display an error message if the user does not have permission
        messages.error(
            request, "You do not have permission to delete this certification."
        )

    # Redirect to the "editGeneralAllCompanion" view
    return redirect("editGeneralAllCompanion")


@login_required
def create_skill(request):
    """
    View function to handle the creation of a new skill associated with a companion.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Redirects to the "editGeneralAllCompanion" view after processing the form.
    """
    # Retrieve the current companion from the request
    actualCompanion = get_actualCompanion(request)

    if request.method == "POST":
        # Process the form data if the request method is POST
        form = SkillForm(request.POST)
        if form.is_valid():
            # Save the skill associated with the current companion
            skill = form.save(commit=False)
            skill.idCompanion = actualCompanion
            skill.save()

            messages.success(request, "¡Skill added correctly!")
        else:
            # Display an error message if the form is not valid
            messages.error(request, "Error in the form. Please correct the errors.")
        return redirect("editGeneralAllCompanion")
    else:
        # Render an empty form for GET requests
        form = SkillForm()

    return form


@login_required
def skill_companion_list(request):
    """
    View function to retrieve a list of skills associated with the current companion.

    Args:
        request (HttpRequest): The request object.

    Returns:
        QuerySet: A queryset containing the skills associated with the current companion.
    """
    # Retrieve the current companion from the request
    actualCompanion = get_actualCompanion(request)

    # Retrieve the skills associated with the current companion
    skillsCompanion = Skill.objects.filter(idCompanion=actualCompanion.idCompanion)

    return skillsCompanion


@login_required
def delete_skill(request, idSkill):
    """
    View function to handle the deletion of a skill associated with a companion.

    Args:
        request (HttpRequest): The request object.
        idSkill (int): The ID of the skill to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the "editGeneralAllCompanion" view.

    Raises:
        Http404: If the specified skill is not found.
    """
    # Retrieve the current companion from the request
    actualCompanion = get_actualCompanion(request)

    # Retrieve the skill object or raise a 404 error if not found
    skill = get_object_or_404(Skill, idSkill=idSkill)

    # Verify that the user is the owner of the associated skill
    if actualCompanion.idCompanion == skill.idCompanion.idCompanion:
        # Delete the skill
        skill.delete()
        messages.success(request, "The skill was successfully deleted.")
    else:
        # Display an error message if the user does not have permission
        messages.error(request, "You do not have permission to delete this skill.")

    # Redirect to the "editGeneralAllCompanion" view
    return redirect("editGeneralAllCompanion")


@login_required
def edit_companion(request):
    """
    View function to handle the editing of companion information.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Redirects to the "editGeneralAllCompanion" view after processing the form.
    """
    # Retrieve the current companion from the request
    actualCompanion = get_actualCompanion(request)

    if request.method == "POST":
        # Process the form submission for updating companion information.
        form = CompanionUpdateForm(request.POST, instance=actualCompanion)
        if form.is_valid():
            # Save the form changes if valid and display success message.
            form.save()
            messages.success(request, "¡Correctly updated your about me!")
        else:
            # Display an error message if the form is invalid.
            messages.error(request, "Error in the form. Please correct the errors.")
        # Redirect the user to the companion edit page.
        return redirect("editGeneralAllCompanion")
    else:
        # Display the companion update form for GET requests.
        form = CompanionUpdateForm(instance=actualCompanion)

    return form


@login_required
def edit_general_all_companion(request):
    """
    View function to render the companion's general edit page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders the "companion/edit_user_companion.html" template with necessary forms and lists.
    """
    # Retrieve forms and lists from respective views
    formEditUserProfile = edit_user_profile(request)
    formReferenceCompanion = create_reference(request)
    listReferencesCompanion = reference_companion_list(request)
    formCreateTimeAvailability = create_time_availability(request)
    listTimeAvailabilityCompanion = time_availability_list(request)
    formCertificationCompanion = create_certification(request)
    listCertificationCompanion = certifications_companion_list(request)
    formCreateSkill = create_skill(request)
    listSkillsCompanion = skill_companion_list(request)
    formEditCompanion = edit_companion(request)

    # Render the template with forms and lists
    return render(
        request,
        "companion/edit_user_companion.html",
        {
            "formEditUserProfile": formEditUserProfile,
            "formReferenceCompanion": formReferenceCompanion,
            "listReferencesCompanion": listReferencesCompanion,
            "formCreateTimeAvailability": formCreateTimeAvailability,
            "listTimeAvailabilityCompanion": listTimeAvailabilityCompanion,
            "formCertificationCompanion": formCertificationCompanion,
            "listCertificationCompanion": listCertificationCompanion,
            "formCreateSkill": formCreateSkill,
            "listSkillsCompanion": listSkillsCompanion,
            "formEditCompanion": formEditCompanion,
        },
    )
