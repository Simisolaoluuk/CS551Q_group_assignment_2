# Dataset

UK institution data for the project. Includes universities, colleges, secondary schools and primary schools across the UK.

## Files

- regions.csv - 12 UK regions with main city
- institutions.csv - 2062 institutions
- performance_records.csv - 6186 performance records (3 years per institution, 2022-2024)
- generate_dataset.py - script that generates the csv files
- load_data.py - django command to load csv into database

## Numbers

- Universities: 113
- Colleges: 77
- Secondary Schools: 601
- Primary Schools: 1271
- Total: 2062

Every city in the dataset has at least one university, one college, one primary school and one secondary school.

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

regions.csv:
- region_id
- name
- country
- main_city

institutions.csv:
- institution_id
- name
- category (University / College / Secondary School / Primary School)
- region_id
- region_name
- city
- postcode
- founded_year

performance_records.csv:
- record_id
- institution_id
- year
- rating
- overall_score
- student_satisfaction_pct (universities and colleges only)
- graduate_outcome_pct (universities and colleges only)
- attendance_rate_pct (schools and colleges only)
