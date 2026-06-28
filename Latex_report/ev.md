Dataset Overview

A comprehensive synthetic dataset containing 1,317,750 time-series records tracking EV charging station availability across 150 stations from 8 major charging networks in 15 US metropolitan areas over 6 months (July - December 2025). This dataset combines station specifications, real-time availability, dynamic pricing, weather conditions, and external factors into a single unified format perfect for machine learning and data analysis.

Use Cases
This dataset is ideal for:

Time Series Forecasting: Predict station availability and peak demand hours
Classification: Determine if a charger will be available at a given time
Regression: Predict utilization rates and wait times
Clustering: Segment stations by usage patterns and location type
Anomaly Detection: Identify maintenance issues or unusual demand spikes
Correlation Analysis: Explore relationships between weather, gas prices, traffic, and EV charging demand
Infrastructure Planning: Identify underserved areas and optimal locations for new stations
Dynamic Pricing Optimization: Model pricing strategies based on demand patterns
Visualization: Create compelling EV infrastructure dashboards and maps
File Structure
Single File: ev_charging_station_data.csv

Rows: 1,317,750 time-series records
Columns: 33 features
Size: ~323 MB
Format: CSV with headers
Time Range: July 1 - December 31, 2025
Sampling Interval: Every 30 minutes
Column Descriptions

Station Info (11 columns)

station_id: Unique identifier for each charging station (e.g., EV00001)
station_name: Human-readable name combining network and location (e.g., "Tesla Supercharger - San Francisco #3")
network: Charging network operator (Tesla Supercharger, ChargePoint, EVgo, Electrify America, Blink, Shell Recharge, Volta, EVCS)
city: City where the station is located (15 major US metros including Los Angeles, San Francisco, New York, Seattle, Austin, etc.)
state: US state abbreviation (CA, TX, NY, WA, FL, etc.)
latitude: Geographic latitude coordinate for mapping and distance calculations
longitude: Geographic longitude coordinate for mapping and distance calculations
location_type: Type of venue (Highway Corridor, Urban Center, Suburban, Shopping Center, Hotel/Hospitality, Workplace, Residential, Airport)
charger_type: Charging technology (Level 2, DC Fast Charge, Tesla DC Fast, Hyper-Fast)
power_output_kw: Maximum power delivery in kilowatts (7.2 kW for Level 2 up to 350 kW for ultra-fast)
amenities_nearby: Comma-separated list of nearby facilities (Restaurant, Shopping Mall, Coffee Shop, Restroom, WiFi, etc.)
Availability Metrics (8 columns)

ports_total: Total number of charging ports at the station (ranges 2-24)
ports_available: Number of ports currently free and ready for use
ports_occupied: Number of ports currently in use by vehicles
ports_out_of_service: Number of ports temporarily unavailable due to maintenance or faults
utilization_rate: Percentage of operational ports currently occupied (0.0 to 1.0)
0.0-0.3: Low usage (plenty of availability)
0.3-0.6: Moderate usage
0.6-0.8: High usage (may need to wait)
0.8-1.0: Near capacity (expect wait times)
station_status: Current operational state (operational, partial_outage, under_maintenance, offline)
estimated_wait_time_mins: Predicted wait time in minutes if all ports are occupied (0 if ports available)
avg_session_duration_mins: Average charging session length (~35 min for DC Fast, ~180 min for Level 2)
Pricing (2 columns)

current_price: Real-time price at this timestamp (reflects dynamic pricing adjustments)
Increases ~15% during peak hours (5-8 PM)
Decreases ~15% during off-peak (2-5 AM)
Surge pricing when utilization > 80%
pricing_type: Billing model (per_kwh, per_minute, or free)
Weather Conditions (3 columns)

temperature_f: Ambient temperature in Fahrenheit at the station location
precipitation_mm: Rainfall/precipitation amount in millimeters (0.0 = dry conditions)
weather_condition: Categorical weather status (clear, partly_cloudy, cloudy, light_rain, heavy_rain, extreme_heat, freezing)
External Factors (3 columns)

gas_price_per_gallon: Local gasoline price in USD (useful for studying EV adoption correlation)
traffic_congestion_index: Traffic intensity score from 1-10 (1-3 light, 4-6 moderate, 7-10 heavy congestion)
local_event: Nearby events that may impact demand (concert, sports_game, conference, festival, none)
Time Features (6 columns)

timestamp: Date and time of the observation (YYYY-MM-DD HH:MM:SS format)
hour_of_day: Hour extracted from timestamp (0-23)
day_of_week: Day of week as integer (0=Monday, 6=Sunday)
month: Month as integer (7=July through 12=December)
is_weekend: Boolean flag (True for Saturday/Sunday)
is_peak_hour: Boolean flag (True during high-traffic hours: 7-9 AM and 5-8 PM)
Key Insights
Usage Patterns by Location Type:

Highway Corridor: Peaks during travel hours (7-9 AM, 4-7 PM), higher on weekends
Workplace: High weekday usage (8 AM - 5 PM), minimal weekends
Shopping Center: Evening and weekend peaks
Residential: Overnight charging peaks (6 PM - 6 AM)
Network Coverage:

8 major networks with realistic pricing structures
Tesla Supercharger, ChargePoint, EVgo, Electrify America, Blink, Shell Recharge, Volta, EVCS
Weather Impact:

Extreme temperatures increase charging demand (battery drain)
Heavy rain reduces overall travel and charging demand