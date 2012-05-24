from django.core.exceptions import ImproperlyConfigured
from django.db.models import base, get_model
from django.utils.importlib import import_module


def load_model_mixin(fullname):
    module_name, mixin_name = fullname.rsplit('.', 1)
    if module_name.count('.') == 0:
        return get_model(module_name, mixin_name)
    else:
        mixin = getattr(import_module(module_name), mixin_name, None)
        if mixin is None:
            raise ImproperlyConfigured

        return mixin



class ModelBase(base.ModelBase):

    def __new__(cls, name, bases, attrs):
        mixins = attrs.get('__mixins__', ())
        bases = tuple(load_model_mixin(name) for name in mixins) + bases
        return super(ModelBase, cls).__new__(cls, name, bases, attrs)



class Model(base.Model):
    __metaclass__ = ModelBase

    class Meta:
        abstract = True


