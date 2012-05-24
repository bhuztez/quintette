from quintette.db import models


class TopicCountMixin(models.Model):
    topic_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)

    class Meta:
        abstract = True

