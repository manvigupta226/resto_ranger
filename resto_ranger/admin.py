from django.contrib import admin
from .models import Store, BusinessHours, TimeZone, StoreReport

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_id', 'timestamp_utc', 'status')
    list_filter = ('status',)
    search_fields = ('store_id',)

@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    list_display = ('store_id', 'get_day_of_week_display', 'start_time_local', 'end_time_local')
    list_filter = ('day_of_week',)
    search_fields = ('store_id',)

@admin.register(TimeZone)
class TimeZoneAdmin(admin.ModelAdmin):
    list_display = ('store_id', 'timezone_str')
    search_fields = ('store_id',)

@admin.register(StoreReport)
class StoreReportAdmin(admin.ModelAdmin):
    list_display = ('store', 'get_status_display', 'report_url')
    raw_id_fields = ('store',)
    list_filter = ('status',)
    search_fields = ('store_id',)  
