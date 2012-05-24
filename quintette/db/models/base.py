from django.core.exceptions import ImproperlyConfigured
from django.db.models import base
from django.utils.importlib import import_module

from quintette.conf import settings


class _ModelMixin(base.Model):
    class Meta:
        abstract = True


class ModelMixinBase(base.ModelBase):

    def __new__(cls, name, bases, attrs):

        if all([issubclass(b, _ModelMixin) for b in bases]):
            meta = attrs.get('Meta', object)
            class Meta(meta):
                abstract = True
                
            attrs['Meta'] = Meta

        return base.ModelBase.__new__(cls, name, bases, attrs)


class ModelMixin(_ModelMixin):
    __metaclass__ = ModelMixinBase


def get_available_model_mixins(mixins):
    for mixin in mixins:
        parts = mixin.split('.')
        module = parts[:-1]
        if module[-1] == 'models':
            module.pop()

        module = '.'.join(module)
        if module in settings.INSTALLED_APPS:
            models = import_module(module+'.models')
            model_mixin = getattr(models, parts[-1], None)
            if not issubclass(model_mixin, ModelMixin):
                raise ImproperlyConfigured

            yield model_mixin


class ModelBase(ModelMixinBase):

    def __new__(cls, name, bases, attrs):
        mixins = attrs.get('__mixins__', ())
        bases = tuple(get_available_model_mixins(mixins)) + bases
        return base.ModelBase.__new__(cls, name, bases, attrs)


class Model(base.Model):
    __metaclass__ = ModelBase

    class Meta:
        abstract = True



