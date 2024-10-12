from django.urls import path
from . import views
from authentication.views import edit_user_profile

urlpatterns = [
    path("create/", views.CompanionRegistrationView.as_view(), name="createCompanion"),
    path("edit/", views.edit_general_all_companion, name="editGeneralAllCompanion"),
    path(
        "edit/deleteReference/<int:idReference>/",
        views.delete_reference,
        name="deleteReference",
    ),
    path(
        "edit/deleteTimeAvailability/<int:idTimeAvailability>/",
        views.delete_time_availability,
        name="deleteTimeAvailability",
    ),
    path(
        "edit/deleteCertification/<int:idCertification>/",
        views.delete_certification,
        name="deleteCertification",
    ),
    path("edit/deleteSkill/<int:idSkill>/", views.delete_skill, name="deleteSkill"),
]
