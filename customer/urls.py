from django.urls import path
from . import views
from authentication.views import edit_user_profile

urlpatterns = [
    path(
        "create/",
        views.CustomerRegistrationFactory().as_view(),
        name="createCustomer",
    ),
    path("edit/", views.edit_general_all_customer, name="editGeneralAllCustomer"),
    path(
        "edit/medicalInformation",
        views.editCreate_MedicalInformation,
        name="editMedicalInformation",
    ),
    path("edit/createPreference", views.create_preference, name="createPreference"),
    path(
        "edit/deletePreference/<int:idPreference>/",
        views.delete_preference,
        name="deletePreference",
    ),
    path("edit/userProfile", edit_user_profile, name="editUserProfileCustomer"),
    path("edit/customer", views.edit_customer, name="editCustomer"),
]
