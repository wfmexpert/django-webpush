import json

from django.contrib import admin

from .models import PushInformation
from .utils import _send_notification
try:
    from django.utils.translation import gettext as _
except:
    from django.utils.translation import gettext_lazy as _

class PushInfoAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "subscription", "group")
    actions = ("send_test_message",)

    def send_test_message(self, request, queryset):
        payload = {"head": "Hey", "body": "Hello World"}
        for device in queryset:
            notification = _send_notification(device.subscription, json.dumps(payload), 0)
            if notification:
                self.message_user(request, _("Test sent successfully"))
            else:
                self.message_user(request, _("Deprecated subscription deleted"))


admin.site.register(PushInformation, PushInfoAdmin)
