from django.db import models
from django.utils.translation import ugettext_lazy as _

from quintette.conf import settings
from quintette.db.models import ModelMixin


class AvatarMixin(ModelMixin):
    avatar = models.ImageField(_("avatar"), upload_to='avatars/', null=True, blank=True)


if 'quintette.contrib.accounts' in settings.INSTALLED_APPS:
    from quintette.contrib.accounts.models import UserProfile

    if issubclass(UserProfile, AvatarMixin):
        from django.dispatch import receiver
        from django.db.models import signals

        from quintette.contrib.avatar.signals import avatar_changed

        @receiver(signals.post_init, sender=UserProfile)
        def profile_init_handler(sender, instance, **kwargs):
            initial = getattr(instance._state, 'initial', {})
            initial['avatar'] = instance.avatar
            instance._state.initial = initial


        @receiver(signals.post_save, sender=UserProfile)
        def profile_save_handler(sender, instance, created, raw, **kwargs):
            if raw:
                return

            old_avatar = None if created else instance._state.initial['avatar']
            new_avatar = instance.avatar

            avatar_changed.send(instance, old=old_avatar, new=new_avatar)


        @receiver(signals.post_delete, sender=UserProfile)
        def profile_delete_handler(sender, instance, **kwargs):
            old_avatar = instance._state.initial['avatar']
            avatar_changed.send(instance, old=old_avatar, new=None)


        if settings.AVATAR_AUTO_CLEAN:
            @receiver(avatar_changed)
            def avatar_clean_handler(sender, old, new, **kwargs):
                if old:
                    old.delete(save=False)


        if settings.AVATAR_RESIZE_HANDLER:
            @receiver(avatar_changed)
            def avatar_resize_handler(sender, old, new, **kwargs):
                if new:
                    pass

