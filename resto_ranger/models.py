from django.db import models

class Store(models.Model):
    store_id = models.CharField(max_length=50)
    timestamp_utc = models.DateTimeField()
    status = models.CharField(max_length=10)  # Assuming 'active' or 'inactive'
    
    def __str__(self):
        return self.store_id

class BusinessHours(models.Model):
    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    store_id = models.CharField(max_length=50)
    day_of_week = models.IntegerField(choices=DAY_CHOICES, null=True )
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    def __str__(self):
        return f"{self.store_id} - {self.get_day_of_week_display()}"


class TimeZone(models.Model):
    store_id = models.CharField(max_length=50)
    timezone_str = models.CharField(max_length=100)


    def __str__(self):
        return self.store_id

class ReportStatus(models.IntegerChoices):
    PENDING = 0
    COMPLETED = 1   

class StoreReport(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="reports", null=True, blank=True)
    status = models.IntegerField(choices=ReportStatus.choices)
    report_url = models.FileField(upload_to="reports", null=True, blank=True)
