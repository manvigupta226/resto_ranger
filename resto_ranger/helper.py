import tempfile
import csv
import os
from django.utils import timezone
from pytz import timezone as pytz_timezone
import datetime
from .models import Store, ReportStatus, StoreReport
import logging

def trigger_report_combined(report):
    csv_data = []
    
    # triggering report
    stores = Store.objects.all()
    for store in stores:
        print(store)
        data = generate_report_data(store)
        csv_data.append(data)
    generate_csv_file(report, csv_data)
    return report

def generate_report_data(store):
    tz = store.timezone_str or 'America/Chicago'
    target_timezone = pytz_timezone(tz)
    
    # hard coding current time as max of all the logs
 
    # Get the most recent store object (assuming timestamp_utc is the latest update)
    latest_store_data = Store.objects.filter(pk=store.pk).order_by('-timestamp_utc').first()


    if not latest_store_data:  # Handle case where no store data exists
        return None  # Or handle it differently based on your needs    local_time = time.astimezone(target_timezone)
    local_time = latest_store_data.timestamp_utc.astimezone(target_timezone)
    utc_timezone = pytz_timezone('UTC')
    utc_time = local_time.astimezone(utc_timezone)
    current_day = local_time.weekday()
    current_time = local_time.time()
    
    # last one hour 
    last_one_hour_data = get_last_one_hour_data(store, utc_time, current_day, current_time)
    # last one day
    last_one_day_data = get_last_one_day_data(store, utc_time, current_day, current_time)
    # last one week
    last_one_week_data = get_last_one_week_data(store, utc_time, current_day, current_time)
    
    data = []
    data.append(store.pk)
    data.extend(list(last_one_hour_data.values()))
    data.extend(list(last_one_day_data.values()))
    data.extend(list(last_one_week_data.values()))

    return data

def generate_csv_file(report, csv_data):
    with tempfile.TemporaryDirectory() as temp_dir:
        file_name = f"{report.pk}.csv"
        temp_file_path = os.path.join(temp_dir, file_name)

        with open(temp_file_path, "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["store_id", "last_one_hour uptime", "last_one_hour downtime", "last_one_hour unit", "last_one_day uptime", "last_one_day downtime", "last_one_day unit", "last_one_week uptime", "last_one_week downtime", "last_one_week unit"])
            for data in csv_data:
                csv_writer.writerow(data)
        report.report_url.save(file_name, open(temp_file_path, "rb"))
        report.status = ReportStatus.COMPLETED
        report.save()

def get_last_one_hour_data(store, utc_time, current_day, current_time):
    last_one_hour_data = {"uptime" : 0 , "downtime" : 0 , "unit" : "minutes"}
    
    # checking if store is open in the last one hour
    is_store_open = store.businesshours.filter(day_of_week=current_day, start_time_local__lte=current_time, end_time_local__gte=current_time).exists()
    if not is_store_open:
        return last_one_hour_data
    
    last_one_hour_logs = store.status_logs.filter(timestamp__gte=utc_time - datetime.timedelta(hours=1)).order_by('timestamp')
    # checking if store is open in the last one hour and the last log status is active
    if last_one_hour_logs:
        last_one_hour_log_status = last_one_hour_logs[0].status
        if last_one_hour_log_status == 'active':
            last_one_hour_data["uptime"] = 60
        else:
            last_one_hour_data["downtime"] = 60

    return last_one_hour_data

def get_last_one_day_data(store, utc_time, current_day, current_time):
    last_one_day_data = {"uptime" : 0 , "downtime" : 0, "unit" : "hours"}
    one_day_ago = current_day - 1 if current_day > 0 else 6
    
    # checking if store is open in the last one day
    is_store_open = store.businesshours.filter(day_of_week__gte=one_day_ago, day_of_week__lte=current_day, start_time_local__lte=current_time, end_time_local__gte=current_time).exists()
    if not is_store_open:
        return last_one_day_data
    
    # getting all the logs in the last one day
    last_one_day_logs = store.status_logs.filter(timestamp__gte=utc_time - datetime.timedelta(days=1)).order_by('timestamp')
    for log in last_one_day_logs:
        # checking if log is in store business hours
        log_in_store_business_hours = store.businesshours.filter(day_of_week=log.timestamp.weekday(), start_time_local__lte=log.timestamp.time(), end_time_local__gte=log.timestamp.time()).exists()
        # checking if log is in store business hours and the status is active
        if log_in_store_business_hours:
            if log.status == 'active':
                last_one_day_data["uptime"] += 1
            else:
                last_one_day_data["downtime"] += 1
    return last_one_day_data

def get_last_one_week_data(store, utc_time, current_day, current_time):
    last_one_week_data = {"uptime" : 0 , "downtime" : 0, "unit" : "hours"}
    one_week_ago = current_day - 7 if current_day > 0 else 0
    
    # checking if store is open in the last one week
    is_store_open = store.businesshours.filter(day_of_week__gte=one_week_ago, day_of_week__lte=current_day, start_time_local__lte=current_time, end_time_local__gte=current_time).exists()
    if not is_store_open:
        return last_one_week_data
    
    # getting all the logs in the last one week
    last_one_week_logs = store.status_logs.filter(timestamp__gte=utc_time - datetime.timedelta(days=7)).order_by('timestamp')
    for log in last_one_week_logs:
        # checking if log is in store business hours
        log_in_store_business_hours = store.businesshours.filter(day_of_week=log.timestamp.weekday(), start_time_local__lte=log.timestamp.time(), end_time_local__gte=log.timestamp.time()).exists()
        # checking if log is in store business hours and the status is active
        if log_in_store_business_hours:
            if log.status == 'active':
                last_one_week_data["uptime"] += 1
            else:
                last_one_week_data["downtime"] += 1
    
    return last_one_week_data
