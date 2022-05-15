from django.contrib import admin
from .models import Mailing, SMS, Push
from django.shortcuts import redirect


@admin.register(Mailing)
class MailAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'user_filter', 'mail_template', 'mail_schedule', 'subject',)
    list_filter = ('mailing',)
    search_fields = ('mailing', 'mail_schedule',)

    fields = ('mailing', 'user_filter', 'mail_template', 'mail_schedule', 'subject'
              )

    def response_change(self, request, obj):
        if "send" in request.POST:
            try:
                obj.Send()
                obj.save()
            except (ValueError, TypeError):
                pass
        return redirect(".")


@admin.register(SMS)
class SMSAdmin(admin.ModelAdmin):
    list_display = ('Name', 'user_filter', 'text', 'sms_schedule')
    list_filter = ('Name',)
    search_fields = ('Name', 'sms_schedule',)

    fields = ('Name', 'user_filter', 'text', 'sms_schedule')


@admin.register(Push)
class PushAdmin(admin.ModelAdmin):
    list_display = ('Name', 'user_filter', 'text', 'push_schedule')
    list_filter = ('Name',)
    search_fields = ('Name', 'push_schedule',)

    fields = ('Name', 'user_filter', 'text', 'push_schedule')
