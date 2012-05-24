from django import http
from django.forms import models as model_forms
from django.core.exceptions import ImproperlyConfigured
from quintette.views.generic.base import TemplateResponseMixin, TemplateView
from quintette.views.generic.detail import SingleObjectMixin



class FormMixin(TemplateResponseMixin):
    """
    A mixin that provides a way to show and handle a form in a request.
    """

    initial = {}
    form_class = None
    success_url = None

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        return self.initial.copy()

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        return self.form_class

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {'initial': self.get_initial()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_success_url(self):
        if self.success_url:
            url = self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

    def form_valid(self, form):
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    


class ProcessFormView(FormMixin, TemplateView):
    """
    A mixin that processes a form on POST.
    """
    def get(self):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))


    def post(self):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



class ModelFormMixin(FormMixin, SingleObjectMixin):
    """
    A mixin that provides a way to show and handle a modelform in a request.
    """


    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        if self.form_class:
            return self.form_class
        else:
            model = self.get_model()
            return model_forms.modelform_factory(model)


    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        kwargs.update({'instance': self.object})
        return kwargs


    def get_success_url(self):
        if self.success_url:
            url = self.success_url % self.object.__dict__
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url


    def form_valid(self, form):
        self.object = form.save()
        return super(ModelFormMixin, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        return super(SingleObjectMixin, self).get_context_data(**context)


    def get_model(self):
        if self.model:
            return self.model
        elif self.form_class and issubclass(self.form_class, model_forms.ModelForm):
            return self.form_class._meta.model
        elif hasattr(self, 'object') and self.object is not None:
            return self.object.__class__
        else:
            return self.get_queryset().model



class CreateView(ModelFormMixin, ProcessFormView):
    """
    View for creating an new object instance,
    with a response rendered by template.
    """
    template_name_suffix = '_form'

    def __init__(self, request, *args, **kwargs):
        super(CreateView, self).__init__(request, *args, **kwargs)
        self.object = None



