from django.contrib import admin
from .models import Mailing


@admin.register(Mailing)
class Mailadmin(admin.ModelAdmin):
    list_display = ('mailing', 'user_filter', 'mail_template', 'mail_schedule', 'subject')
    list_filter = ('mailing',)
    search_fields = ('mailing', 'mail_schedule',)

    fields = ('mailing', 'user_filter', 'mail_template', 'mail_schedule', 'subject'
    )


