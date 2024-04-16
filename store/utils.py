from resto_ranger.models import Store , StoreReport , ReportStatus
from django.utils import timezone 
from pytz import timezone as pytz_timezone
import datetime


from resto_ranger.models import Store
stores = Store.objects.all()[:50]
from resto_ranger.helper import trigger_report_combined
report = StoreReport.objects.create(status=ReportStatus.PENDING)
trigger_report_combined(report)

