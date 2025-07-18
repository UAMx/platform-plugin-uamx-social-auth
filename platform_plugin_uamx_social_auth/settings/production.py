# Add Filter configuration to show Terms of Service modal on every user login
# based on https://docs.openedx.org/projects/openedx-filters/en/latest/how-tos/using-filters.html

# lint-amnesty, pylint: disable=missing-function-docstring, missing-module-docstring
def plugin_settings(settings):

    # Add plugin configuration based on 
    # https://github.com/eduNEXT/openedx-filters-samples/blob/c22cf063ccc82b862310b8dae45731ecb3abdd73/openedx_filters_samples/samples/pipeline.py#L273
    settings.OPEN_EDX_FILTERS_CONFIG = {
            #"org.openedx.learning.student.registration.requested.v1": {
            #    "fail_silently": False,
            #    "pipeline": [
            #        "uamx_social_auth.pipeline.StopUAMDomainRegister"
            #    ]
            #},
            "org.openedx.learning.student.login.requested.v1": {
                "fail_silently": False,
                "pipeline": [
                    "uamx_social_auth.pipeline.StopUAMDomainLogin"
                ]
            }
        }
