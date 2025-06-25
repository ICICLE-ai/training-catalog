---
tags:
  - Food-Access
---

# Explanation

1. **locations.csv**  
   - Contains synthetic “location” rows (depots and customers).  
   - The first row (`L001`) is a fixed depot at the specified latitude/longitude.  
   - The remaining rows are random points within a given radius; each has a 10% chance to be flagged as an additional depot.  
   - All rows include fields such as demand, product type, temperature requirements, ripeness/expiration dates, packaging, handling notes, and time windows.

2. **vehicles.csv**  
   - Contains synthetic “vehicle” rows.  
   - The number of vehicles is at least 30% of the number of location rows (rounded up).  
   - Each vehicle’s start location is randomly chosen from any location flagged as a depot.  
   - Vehicle capacity is randomly between 100 and 500 boxes.  
   - Availability windows span any two hour marks in the 24-hour day (00:00–23:00).
