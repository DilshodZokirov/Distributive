from django.db import models

from apps.user.models import User


class Auditable(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_by")
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="updated_by", null=True, blank=True)

    class Meta:
        abstract = True
