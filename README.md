# resto_ranger
Efficiently manage your restaurant's activity status with just a tap - our polling app makes it effortless

This repository contains the backend system for monitoring the status of restaurants. The system tracks these restaurants' online/offline status during their business hours and provides detailed reports on store uptime and downtime.

The system uses the Python Django framework and utilizes a PostgreSQL database.
This system aims to give restaurant owners valuable insights into their stores' operational status, helping them make informed decisions to improve uptime and customer experience.


**APIs**

 1. Trigger report-

  --url http://localhost:8000/store/{store_id}/trigger_report/ 

2. Generate Report-

   --url http://localhost:8000/store/get_report/ 
