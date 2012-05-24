from django import http
from django.core.exceptions import ImproperlyConfigured
from django.template.response import TemplateResponse
from django.utils.log import getLogger

logger = getLogger('quintette.request')



class ViewBase(type):

    def __call__(cls, request, *args, **kwargs):
        if request.method.lower() in cls.http_method_names:
            handler = getattr(cls, request.method.lower(), None)
        else:
            handler = None
        
        if handler is None:
            return cls.http_method_not_allowed(request, *args, **kwargs)

        instance = type.__call__(cls, request, *args, **kwargs)
        return handler(instance)



class View(object):
    __metaclass__ = ViewBase

    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']


    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs


    @classmethod
    def http_method_not_allowed(self, request, *args, **kwargs):
        allowed_methods = [m for m in self.http_method_names if hasattr(self, m)]
        logger.warning('Method Not Allowed (%s): %s', request.method, request.path,
            extra={
                'status_code': 405,
                'request': request
            }
        )
        return http.HttpResponseNotAllowed(allowed_methods)


    def options(self, request, *args, **kwargs):
        response = http.HttpResponse()
        response['Allow'] = ', '.join(self._allowed_methods())
        response['Content-Length'] = 0
        return response


    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]



class TemplateResponseMixin(object):
    """
    A mixin that can be used to render a template.
    """
    template_name = None
    response_class = TemplateResponse
    extra_context = None


    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        return self.response_class(
            request = self.request,
            template = self.get_template_names(),
            context = context,
            **response_kwargs
        )


    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [self.template_name]


    def get_context_data(self, **kwargs):
        kwargs.update(self.get_extra_context())
        return kwargs
        
    
    def get_extra_context(self):
        return self.extra_context or {}


class TemplateView(TemplateResponseMixin, View):
    """
    A view that renders a template.
    """

    def get(self):
        context = self.get_context_data()
        return self.render_to_response(context)



