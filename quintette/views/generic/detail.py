from django import http
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _

from quintette.views.generic.base import TemplateResponseMixin, TemplateView



class SingleObjectMixin(TemplateResponseMixin):
    model = None
    queryset = None
    slug_field = 'slug'
    context_object_name = None
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    template_name_field = None
    template_name_suffix = '_detail'


    def get_model(self):
        return self.model


    def get_queryset(self):
        """
        Get the queryset to look an object up against. May not be called if
        `get_object` is overridden.
        """
        if self.queryset is None:
            model = self.get_model()
            if model:
                return model._default_manager.all()
            else:
                raise ImproperlyConfigured(u"%(cls)s is missing a queryset. Define "
                                           u"%(cls)s.model, %(cls)s.queryset, or override "
                                           u"%(cls)s.get_object()." % {
                                                'cls': self.__class__.__name__
                                        })
        return self.queryset._clone()


    def get_slug_field(self):
        """
        Get the name of a slug field to be used to look up by slug.
        """
        return self.slug_field


    def get_object(self, queryset):
        """
        Returns the object the view is displaying.

        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        elif slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        else:
            raise AttributeError(u"Generic detail view %s must be called with "
                                 u"either an object pk or a slug."
                                 % self.__class__.__name__)

        try:
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise http.Http404(_(u"No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj


    def get_context_object_name(self, obj):
        """
        Get the name to use for the object.
        """
        if self.context_object_name:
            return self.context_object_name
        elif hasattr(obj, '_meta'):
            return obj._meta.object_name.lower()
        else:
            return None


    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        return super(SingleObjectMixin, self).get_context_data(**context)


    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        try:
            names = super(SingleObjectMixin, self).get_template_names()
        except ImproperlyConfigured:
            # If template_name isn't specified, it's not a problem --
            # we just start with an empty list.
            names = []

        # If self.template_name_field is set, grab the value of the field
        # of that name from the object; this is the most specific template
        # name, if given.
        if self.object and self.template_name_field:
            name = getattr(self.object, self.template_name_field, None)
            if name:
                names.insert(0, name)

        # The least-specific option is the default <app>/<model>_detail.html;
        # only use this if the object in question is a model.
        if hasattr(self.object, '_meta'):
            names.append("%s/%s%s.html" % (
                self.object._meta.app_label,
                self.object._meta.object_name.lower(),
                self.template_name_suffix
            ))
        elif hasattr(self, 'get_model'):
            model = self.get_model()
            if hasattr(model, '_meta'):
                names.append("%s/%s%s.html" % (
                    model._meta.app_label,
                    model._meta.object_name.lower(),
                    self.template_name_suffix
                ))
        return names




class DetailView(SingleObjectMixin, TemplateView):
    """
    Render a "detail" view of an object.

    By default this is a model instance looked up from `self.queryset`, but the
    view will support display of *any* object by overriding `self.get_object()`.
    """

    def __init__(self, request, *args, **kwargs):
        super(DetailView, self).__init__(request, *args, **kwargs)
        self.object = self.get_object(self.get_queryset())



