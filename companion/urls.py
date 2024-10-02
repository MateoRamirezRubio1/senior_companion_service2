from django.urls import path
from . import views
from authentication.views import edit_user_profile

urlpatterns = [
    path("create/", views.CompanionRegistrationView.as_view(), name="createCompanion"),
    path("edit/", views.edit_general_all_companion, name="editGeneralAllCompanion"),
    path("edit/userProfile", edit_user_profile, name="editUserProfileCompanion"),
    path("edit/createReference", views.create_reference, name="createReference"),
    path(
        "edit/deleteReference/<int:idReference>/",
        views.delete_reference,
        name="deleteReference",
    ),
    path(
        "edit/createTimeAvailability",
        views.create_time_availability,
        name="createTimeAvailability",
    ),
    path(
        "edit/deleteTimeAvailability/<int:idTimeAvailability>/",
        views.delete_time_availability,
        name="deleteTimeAvailability",
    ),
    path(
        "edit/createCertification",
        views.create_certification,
        name="createCertification",
    ),
    path(
        "edit/deleteCertification/<int:idCertification>/",
        views.delete_certification,
        name="deleteCertification",
    ),
    path("edit/createSkill", views.create_skill, name="createSkill"),
    path("edit/deleteSkill/<int:idSkill>/", views.delete_skill, name="deleteSkill"),
    path("edit/editCompanion", views.edit_companion, name="editCompanion"),
]
