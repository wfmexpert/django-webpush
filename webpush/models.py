from django.db import models
from django.core.exceptions import FieldError
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")


class SubscriptionInfo(models.Model):
    browser = models.CharField(max_length=100)
    user_agent = models.CharField(max_length=500)
    endpoint = models.URLField(max_length=500)
    auth = models.CharField(max_length=100)
    p256dh = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} / {self.browser}"

    class Meta:
        verbose_name = _("Subscription info")
        verbose_name_plural = _("Subscriptions info")


class PushInformation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='webpush_info', blank=True, null=True, on_delete=models.CASCADE)
    subscription = models.ForeignKey(SubscriptionInfo, related_name='webpush_info', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='webpush_info', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.user and self.group:
            return f"{self.subscription} / {self.user} / {self.group}"
        elif self.user:
            return f"{self.subscription} / {self.user}"
        elif self.group:
            return f"{self.subscription} // {self.group}"

    def save(self, *args, **kwargs):
        # Check whether user or the group field is present
        # At least one field should be present there
        # Through from the functionality its not possible, just in case! ;)
        if self.user or self.group:
            super(PushInformation, self).save(*args, **kwargs)
        else:
            raise FieldError(_('At least user or group should be present'))

    class Meta:
        verbose_name = _("Push information")
        verbose_name_plural = _("Pushes information")