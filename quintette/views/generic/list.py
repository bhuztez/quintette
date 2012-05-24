from django import http
from django.core.exceptions import ImproperlyConfigured

from quintette.views.generic.base import TemplateResponseMixin, TemplateView


class MultipleObjectMixin(TemplateResponseMixin):
    queryset = None
    model = None
    allow_empty = True
    context_object_name = None
    template_name_suffix = '_list'


    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(u"'%s' must define 'queryset' or 'model'"
                                       % self.__class__.__name__)
        return queryset


    def get_allow_empty(self):
        """
        Returns ``True`` if the view should display empty lists, and ``False``
        if a 404 should be raised instead.
        """
        return self.allow_empty


    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if get_template is overridden.
        """
        try:
            names = super(MultipleObjectMixin, self).get_template_names()
        except ImproperlyConfigured:
            # If template_name isn't specified, it's not a problem --
            # we just start with an empty list.
            names = []

        # If the list is a queryset, we'll invent a template name based on the
        # app and model name. This name gets put at the end of the template
        # name list so that user-supplied names override the automatically-
        # generated ones.
        if hasattr(self.object_list, 'model'):
            opts = self.object_list.model._meta
            names.append("%s/%s%s.html" % (opts.app_label, opts.object_name.lower(), self.template_name_suffix))

        return names


    def get_context_object_name(self, object_list):
        """
        Get the name of the item to be used in the context.
        """
        if self.context_object_name:
            return self.context_object_name
        elif hasattr(object_list, 'model'):
            return '%s_list' % object_list.model._meta.object_name.lower()
        else:
            return 'object_list'


    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            if len(self.object_list) == 0:
                raise http.Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                        % {'class_name': self.__class__.__name__})

        context_object_name = self.get_context_object_name(self.object_list)
        context = {}
        if context_object_name is not None:
            context[context_object_name] = self.object_list

        context.update(kwargs)
        return super(MultipleObjectMixin, self).get_context_data(**context)



class ListView(MultipleObjectMixin, TemplateView):
    """
    Render some list of objects, set by `self.model` or `self.queryset`.
    `self.queryset` can actually be any iterable of items, not just a queryset.
    """

    def __init__(self, request, *args, **kwargs):
        super(ListView, self).__init__(request, *args, **kwargs)
        self.object_list = self.get_queryset()



