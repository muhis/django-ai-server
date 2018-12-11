from django.contrib import admin
from core.models import Trial


class TrialAdmin(admin.ModelAdmin):
    pass


admin.site.register(Trial, TrialAdmin)
# Register your models here.
