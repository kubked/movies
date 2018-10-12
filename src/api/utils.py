from rest_framework.renderers import JSONRenderer


class IndentedJSONRenderer(JSONRenderer):
    """JSONRenderer with default indent"""
    default_indent = 2

    def get_indent(self, accepted_media_type, renderer_context):
        indent = super().get_indent(accepted_media_type, renderer_context)
        return indent or self.default_indent
