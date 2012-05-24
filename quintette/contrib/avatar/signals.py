from django.dispatch import Signal


avatar_changed = Signal(providing_args=["old", "new"])


