from django.contrib.auth.decorators import user_passes_test


def staff_or_superuser_required(function=None, redirect_field_name=None,
                                unauthorized_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_staff or u.is_superuser,
        login_url=None,
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
