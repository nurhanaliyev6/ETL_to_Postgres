# ETL_to_Postgres

# Data Engineering Homework

This repository contains solutions for the Data Engineering homework from the DataTalksClub course, specifically Week 1, where we practiced using Docker and SQL to analyze NYC taxi trip data.

## Table of Contents
- [Overview](#overview)
- [Files and Directory Structure](#files-and-directory-structure)
- [Setup](#setup)
- [Homework Questions and Solutions](#homework-questions-and-solutions)
- [Usage](#usage)
- [Conclusion](#conclusion)
- [License](#license)

## Overview

In this homework, we prepared our environment using Docker and practiced SQL queries with NYC taxi trip data. The main focus was on understanding Docker commands, running PostgreSQL, and querying data to derive meaningful insights.

## Files and Directory Structure

The repository contains the following files and directories:


### File Descriptions
- **docker-compose.yaml**: Configuration file for Docker to run PostgreSQL and PGadmin.
- **upload_trip_data.py**: Python script to upload taxi trip data to PostgreSQL.
- **upload_zone_data.py**: Python script to upload zone data to PostgreSQL.
- **green_tripdata_2019-09.csv**: Dataset containing NYC green taxi trip data for  2019.
- **taxi_zone_lookup.csv**: Dataset containing taxi zone information.
- **questions_to_solve_with_sql.txt**: Contains the homework questions that were solved using SQL.
- **commands.txt**: A log of useful Docker commands and SQL queries.

## Setup

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) must be installed on your machine.
- Basic knowledge of Docker commands and SQL.

### Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/nurhanaliyev6/ETL_to_Postgres.git
   cd ETL_to_Postgres
   ```

2. Build and run the Docker container:
```bash
    docker-compose up -d
```

3. Run the upload scripts to load data into PostgreSQL:
```bash
    python upload_trip_data.py
    python upload_zone_data.py
```

## Homework Questions and Solutions
Knowing Docker Tags

Answer: The tag that has the text "Automatically remove the container when it exits" is --rm.
--------------------------------------------------------------
Understanding Docker First Run

Run Docker with the python:3.9 image in interactive mode and check installed Python modules using:

```bash
docker run -it --entrypoint:bash python:3.9 bash
pip list

```
--------------------------------------------------------
QUESTION-1: How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18.

Remember that lpep_pickup_datetime and lpep_dropoff_datetime columns are in the format timestamp (date and hour+min+sec) and not in date.

a-15767
b-15612
c-15859
d-89009

ANSWER: 15767

QUERY:
SELECT date_trunc('day', "lpep_pickup_datetime") gun,
count(date_trunc('day', "lpep_pickup_datetime")) say
FROM public.green_trip_data 
group by gun
having date_trunc('day', "lpep_pickup_datetime")=TO_DATE('2019-09-18', 'YYYY-MM-DD');

--------------------------------------------------------------

QUESTION-2:
Longest trip for each day
Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.

Tip: For every trip on a single day, we only care about the trip with the longest distance.

a-2019-09-18
b-2019-09-16
c-2019-09-26
d-2019-09-21

ANSWER: 2019-09-26

QUERY:
SELECT date_trunc('day', "lpep_pickup_datetime") gun, max(trip_distance) maxi
FROM public.green_trip_data 
group by gun
order by maxi desc;


-----------------------------------------------------------------------

QUESTION-3:

Three biggest pick up Boroughs
Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

a-"Brooklyn" "Manhattan" "Queens"
b-"Bronx" "Brooklyn" "Manhattan"
c-"Bronx" "Manhattan" "Queens"
d-"Brooklyn" "Queens" "Staten Island"

ANSWER: "Brooklyn" "Manhattan" "Queens"

QUERY:
select "Borough",round(sum(total_amount)) maxi
from public.green_trip_data g 
join taxi_zone_lookup t
on g."PULocationID"=t."LocationID" 
where date_trunc('day', "lpep_pickup_datetime")=TO_DATE('2019-09-18', 'YYYY-MM-DD')
and "Borough"!='Unknown'
group by "Borough"
having sum(total_amount)>50000
order by maxi desc;

-----------------------------------------------

QUESTION-4:

Largest tip
For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip? We want the name of the zone, not the id.

Note: it's not a typo, it's tip , not trip

a-Central Park
b-Jamaica
c-JFK Airport
d-Long Island City/Queens Plaza

ANSWER: JFK Airport

QUERY:

select "Zone",max(tip_amount) maxi
from public.green_trip_data g 
join taxi_zone_lookup t
on g."DOLocationID"=t."LocationID" 
where date_trunc('month', "lpep_pickup_datetime")=TO_DATE('2019-09', 'YYYY-MM')
group by "Zone"
having "Zone" in ('Central Park','Jamaica','JFK Airport','Long Island City/Queens Plaza')
order by maxi desc;

