from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response


class IndentedJSONRenderer(JSONRenderer):
    """JSONRenderer with default indent"""
    default_indent = 2

    def get_indent(self, accepted_media_type, renderer_context):
        indent = super().get_indent(accepted_media_type, renderer_context)
        return indent or self.default_indent

