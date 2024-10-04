from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


def actual_customer_required(customer_service):
    """
    Decorator to obtain the current customer associated with the logged-in user.
    Adds the current customer as an argument to the view.

    Args:
        customer_service: Instance of the customer service to use.

    Returns:
        Decorated function that handles access to the current customer.
    """

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            actual_user_id = request.user.idUser

            # Use the service to obtain the current customer
            actual_customer = customer_service.get_customer_by_user_id(actual_user_id)

            if actual_customer is None:
                return HttpResponseForbidden(
                    "No customer associated with the user was found."
                )

            # Add the current customer to the view context
            return view_func(request, actualCustomer=actual_customer, *args, **kwargs)

        return _wrapped_view

    return decorator


def inject_service(service_instance):
    """
    Decorator to inject a service instance into the view function.

    Args:
        service_instance: The service instance to inject.

    Returns:
        Decorated function that includes the service in its arguments.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, service=service_instance, *args, **kwargs)

        return _wrapped_view

    return decorator
