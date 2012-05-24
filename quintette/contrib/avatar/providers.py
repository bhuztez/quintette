from quintette.contrib.accounts.models import UserProfile
from quintette.contrib.avatar.models import AvatarMixin


if issubclass(UserProfile, AvatarMixin):
    class LocalAvatarProvider(object):
        def get_avatar_url(user, size):
            pass


