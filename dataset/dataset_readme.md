# Dataset

UK institution data for the project. Includes universities, colleges, secondary schools and primary schools across the UK.

## Files

- regions.csv - 12 UK regions
- institutions.csv - 1106 institutions
- performance_records.csv - 3318 performance records (3 years per institution, 2022-2024)
- generate_dataset.py - script that generates the csv files
- load_data.py - django command to load csv into database

## Numbers

- Universities: 83
- Colleges: 73
- Secondary Schools: 250
- Primary Schools: 700
- Total: 1106

## How to use

To regenerate the csv files:

```
python generate_dataset.py
```

To load the data into django, copy load_data.py to:

```
institutions/management/commands/load_data.py
```

Then run:

```
python manage.py load_data
```

## Fields

institutions.csv has these columns:
- institution_id
- name
- category (University / College / Secondary School / Primary School)
- region_id
- region_name
- city
- postcode
- founded_year
- website

performance_records.csv has:
- record_id
- institution_id
- year
- rating
- overall_score
- student_satisfaction_pct (universities and colleges only)
- graduate_outcome_pct (universities and colleges only)
- attendance_rate_pct (schools and colleges only)
