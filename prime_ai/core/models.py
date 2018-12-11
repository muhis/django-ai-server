import uuid
from django.db import models


class Trial(models.Model):
    """Each one of the trials represent different trial

    """
    uuid = models.UUIDField(default=uuid.uuid4)
    js_payload = models.TextField()
    result_accuracy_percentage = models.FloatField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
