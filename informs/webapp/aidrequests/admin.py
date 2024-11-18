"""
AidRequests Admin
"""

from django.contrib import admin
from .models import AidRequest, FieldOp, AidLocation

# Register your models here.


class AidRequestAdmin(admin.ModelAdmin):
    """aid request admin"""
    list_display = ('pk', 'field_op', 'assistance_type',
                    'requestor_first_name', 'requestor_last_name', 'group_size')
    list_filter = ('field_op', 'assistance_type',)
    search_fields = ('requestor_first_name',
                     'requestor_last_name',
                     'street_address',
                     'city',
                     'assistance_description')


class FieldOpAdmin(admin.ModelAdmin):
    """fieldops admin"""
    list_display = ('pk', 'slug', 'name')


class AidLocationAdmin(admin.ModelAdmin):
    """AidLocation admin"""
    list_display = ('aid_request', 'status', 'source', 'latitude', 'longitude')


admin.site.register(AidRequest, AidRequestAdmin)
admin.site.register(FieldOp, FieldOpAdmin)
admin.site.register(AidLocation, AidLocationAdmin)
