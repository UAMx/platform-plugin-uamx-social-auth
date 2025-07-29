from django.http import HttpResponse
from openedx_filters import PipelineStep
from openedx_filters.learning.filters import (
    StudentLoginRequested,
    StudentRegistrationRequested
)

# Modified from: https://github.com/eduNEXT/eox-tenant/blob/master/eox_tenant/pipeline.py

class UAMxAuthException(ValueError):
    """Auth process exception."""

    def __init__(self, backend, *args, **kwargs):
        self.backend = backend
        super().__init__(*args, **kwargs)

# pylint: disable=unused-argument,keyword-arg-before-vararg
def safer_associate_by_email(backend, details, user=None, *args, **kwargs):
    """
    Associate current auth with a user with the same email address in the DB.
    This pipeline entry is not 100% secure. It is better suited however for the
    multi-tenant case so we allow it for certain tenants.

    It replaces:
    https://github.com/python-social-auth/social-core/blob/master/social_core/pipeline/social_auth.py
    """
    if user:
        return None

    email = details.get('email')
    if email:
        # Try to associate accounts registered with the same email address,
        # only if it's a single object. AuthException is raised if multiple
        # objects are returned.
        users = list(backend.strategy.storage.user.get_users_by_email(email))
        if not users:
            return None
        elif len(users) > 1:
            raise UAMxAuthException(
                backend,
                'The given email address is associated with more than one account'
            )
        else:
            # # Ignore this error for staff or superusers
            # if users[0].is_staff or users[0].is_superuser:
            #     raise UAMxAuthException(
            #         backend,
            #         'It is not allowed to auto associate staff or admin users'
            #     )
            return {'user': users[0],
                    'is_new': False}

class StopUAMDomainRegister(PipelineStep):
    """
    Stop registration process raising PreventRegister exception.

    From https://github.com/eduNEXT/openedx-filters-samples/blob/master/openedx_filters_samples/samples/pipeline.py
    """
    def run_filter(self, form_data, *args, **kwargs):
        if form_data["email"].endswith("uam.es"):
            raise StudentRegistrationRequested.PreventRegistration(
                "You can't register. UAM users should use ID-UAM.", status_code=403, error_code="uamx__uam-domain-register-forbidden"
            )

class StopUAMDomainLogin(PipelineStep):
    """
    Stop login process raising PreventLogin exception.

    From https://github.com/eduNEXT/openedx-filters-samples/blob/master/openedx_filters_samples/samples/pipeline.py
    """

    def run_filter(self, user, *args, **kwargs):  # pylint: disable=arguments-differ
        if user and user.email.endswith("uam.es"):
            raise StudentLoginRequested.PreventLogin(
                "You can't login. UAM users should use ID-UAM.", redirect_to="", error_code="uamx__uam-domain-login-forbidden"
            )
        else:
            return {}