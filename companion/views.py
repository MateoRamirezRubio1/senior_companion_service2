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
from abc import ABC, abstractmethod
from .services import ReferenceService, TimeAvailabilityService, CertificationService


class EditCompanionProfileStrategy(ABC):
    @abstractmethod
    def process(self, request, actualCompanion):
        pass


class CompanionUpdateStrategy(EditCompanionProfileStrategy):
    def process(self, request, actualCompanion):
        if request.method == "POST" and "edit_companion_form" in request.POST:
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


class ReferenceStrategy(EditCompanionProfileStrategy):
    def process(self, request, actualCompanion):
        if request.method == "POST" and "create_reference_form" in request.POST:
            service = ReferenceService()
            # Process POST request to save a new reference
            form = ReferenceForm(request.POST)

            if form.is_valid():
                # Valid form submission
                service.create_reference(actualCompanion, form)

                messages.success(request, "¡Reference added correctly!")

            else:
                # Invalid form submission
                email_error_message = service.validate_email_reference_form(form)

                if email_error_message:
                    messages.error(request, email_error_message)
                else:
                    messages.error(
                        request, "Error in the form. Please correct the errors."
                    )

            return redirect("editGeneralAllCompanion")
        else:
            # Render the form for a GET request
            form = ReferenceForm()

        return form


class TimeAvailabilityStrategy(EditCompanionProfileStrategy):
    def process(self, request, actualCompanion):
        if request.method == "POST" and "create_time_availability_form" in request.POST:
            form = TimeAvailabilityForm(request.POST)
            if form.is_valid():
                service = TimeAvailabilityService()
                # Validate if a TimeAvailability already exists with the same date and times
                existing_availability_message = (
                    service.validate_time_availability_exists(form)
                )

                if existing_availability_message:
                    messages.error(
                        request,
                        existing_availability_message,
                    )
                else:
                    service.create_time_availability(actualCompanion, form)
                    messages.success(request, "Time availability added successfully!")
            else:
                # Invalid form submission
                if form.errors:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"{error}")
                else:
                    messages.error(
                        request, "Error in the form. Please correct the errors."
                    )

            return redirect("editGeneralAllCompanion")
        else:
            # Render the form for a GET request
            form = TimeAvailabilityForm()

        return form


class CertificationStrategy(EditCompanionProfileStrategy):
    def process(self, request, actualCompanion):
        if request.method == "POST" and "create_certification_form" in request.POST:
            # Process POST request to save a new certification entry
            form = CertificationForm(request.POST, request.FILES)

            if form.is_valid():
                service = CertificationService()
                service.create_certification(actualCompanion, form)

                messages.success(request, "¡Certification added correctly!")
            else:
                # Invalid form submission
                if form.errors:
                    for field, errors in form.errors.items():
                        for error in errors:
                            messages.error(request, f"{field.capitalize()}: {error}")
                else:
                    messages.error(
                        request, "Error in the form. Please correct the errors."
                    )

            return redirect("editGeneralAllCompanion")
        else:
            # Render the form for a GET request
            form = CertificationForm()

        return form


class SkillStrategy(EditCompanionProfileStrategy):
    def process(self, request, actualCompanion):
        if request.method == "POST" and "create_skill_form" in request.POST:
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


class CompanionProfileStrategyFactory:
    def get_strategy(self, section):
        sections = {
            "companion": CompanionUpdateStrategy,
            "skill": SkillStrategy,
            "certification": CertificationStrategy,
            "time_availability": TimeAvailabilityStrategy,
            "reference": ReferenceStrategy,
        }

        if section not in sections:
            raise ValueError(f"The section type '{section}' is not supported.")

        return sections[section]()


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
    service = ReferenceService()
    reference = service.get_reference_by_id(idReference)

    deleted_reference = service.delete_reference(actualCompanion, reference)

    # Verify that the user is the preference owner
    if deleted_reference["type"]:
        messages.success(request, deleted_reference["content"])
    else:
        messages.error(request, deleted_reference["content"])

    return redirect("editGeneralAllCompanion")


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
    service = TimeAvailabilityService()
    timeAvailability = service.get_time_availability_by_id(idTimeAvailability)

    deleted_time_availability = service.delete_time_availability(
        actualCompanion, timeAvailability
    )

    # Verify that the user is the preference owner
    if deleted_time_availability["type"]:
        messages.success(request, deleted_time_availability["content"])
    else:
        messages.error(request, deleted_time_availability["content"])

    return redirect("editGeneralAllCompanion")


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
    service = CertificationService()

    # Retrieve the certification object or raise a 404 error if not found
    certification = service.get_certification_by_id(idCertification)
    deleted_certification = service.delete_certification(actualCompanion, certification)

    # Verify that the user is the owner of the associated companion
    if deleted_certification["type"]:
        messages.success(request, deleted_certification["content"])
    else:
        # Display an error message if the user does not have permission
        messages.error(request, deleted_certification["content"])

    # Redirect to the "editGeneralAllCompanion" view
    return redirect("editGeneralAllCompanion")


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
def edit_general_all_companion(request):
    """
    View function to render the companion's general edit page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Renders the "companion/edit_user_companion.html" template with necessary forms and lists.
    """
    factory = CompanionProfileStrategyFactory()
    actualCompanion = get_actualCompanion(request)
    reference_service = ReferenceService()
    time_availability_service = TimeAvailabilityService()
    certification_service = CertificationService()

    # Retrieve forms and lists from respective views
    formEditUserProfile = edit_user_profile(request)
    formReferenceCompanion = factory.get_strategy("reference").process(
        request, actualCompanion
    )
    listReferencesCompanion = reference_service.get_reference_list_by_companion(
        actualCompanion
    )
    formCreateTimeAvailability = factory.get_strategy("time_availability").process(
        request, actualCompanion
    )
    listTimeAvailabilityCompanion = (
        time_availability_service.get_time_availability_list_by_companion(
            actualCompanion
        )
    )
    formCertificationCompanion = factory.get_strategy("certification").process(
        request, actualCompanion
    )
    listCertificationCompanion = (
        certification_service.get_certification_list_by_companion(actualCompanion)
    )
    formCreateSkill = factory.get_strategy("skill").process(request, actualCompanion)
    listSkillsCompanion = skill_companion_list(request)
    formEditCompanion = factory.get_strategy("companion").process(
        request, actualCompanion
    )

    if request.method == "POST":
        return redirect("editGeneralAllCompanion")

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
