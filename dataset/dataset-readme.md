# UK Institution Dataset – CS551Q Group Assignment 2

**Owner:** Database Manager (Jia)
**Issue:** [#32 – Find UK Institution dataset (1000+ records)](../../issues/32)
**Related sub-issues:** #33, #34, #35, #36, #37, #38, #40

---

## 1. Overview

This dataset contains **1106 real and realistic UK educational institutions**
spread across all 12 UK regions (England's 9 regions, Scotland, Wales, and
Northern Ireland), together with **3318 performance records** (3 years per
institution, 2022–2024).

The data is structured to map directly onto the three Django models defined in
the project plan: `Region`, `Institution`, and `PerformanceRecord`.

## 2. Files

| File | Records | Description |
|------|---------|-------------|
| `regions.csv` | 12 | UK regions and their parent country |
| `institutions.csv` | **1106** | All educational institutions |
| `performance_records.csv` | 3318 | Yearly performance data per institution |
| `generate_dataset.py` | – | Script used to generate the dataset (reproducible with `seed=42`) |
| `load_data.py` | – | Django script that loads the CSVs into the database |

## 3. Institution breakdown

| Category | Count | Notes |
|----------|-------|-------|
| University | 83 | All real UK universities (Oxford, Cambridge, Russell Group, post-92, all four nations) |
| College | 73 | Real UK Further Education / Sixth Form colleges |
| Secondary School | 250 | Realistic UK secondary school names |
| Primary School | 700 | Realistic UK primary school names |
| **Total** | **1106** | |

## 4. Regional distribution

Institutions are distributed across regions roughly proportional to UK
population, so London and the South East have the most, and Northern Ireland
the fewest:

| Region | Institutions |
|--------|--------------|
| Greater London | 173 |
| South East England | 160 |
| North West England | 112 |
| West Midlands | 100 |
| Scotland | 96 |
| South West England | 93 |
| East Midlands | 84 |
| Yorkshire and the Humber | 83 |
| East of England | 76 |
| Wales | 58 |
| North East England | 40 |
| Northern Ireland | 31 |

## 5. Schema

### `regions.csv`
| Column | Type | Description |
|--------|------|-------------|
| region_id | int | Primary key |
| name | string | Region name (e.g. "Greater London") |
| country | string | Parent country (England / Scotland / Wales / Northern Ireland) |

### `institutions.csv`
| Column | Type | Description |
|--------|------|-------------|
| institution_id | int | Primary key |
| name | string | Institution name |
| category | string | One of: `University`, `College`, `Secondary School`, `Primary School` |
| region_id | int | FK -> regions.region_id |
| region_name | string | Denormalised region name (for convenience) |
| city | string | City the institution is in |
| postcode | string | UK postcode (real prefix for the city) |
| founded_year | int | Year the institution was founded |
| website | string | Website URL (universities/colleges only) |

### `performance_records.csv`
| Column | Type | Description |
|--------|------|-------------|
| record_id | int | Primary key |
| institution_id | int | FK -> institutions.institution_id |
| year | int | One of 2022, 2023, 2024 |
| rating | string | `Outstanding`/`Good`/`Requires Improvement`/`Inadequate` for schools/colleges; `Gold`/`Silver`/`Bronze` for universities |
| overall_score | int | Numeric score 0–100 (used for sorting & ranking) |
| student_satisfaction_pct | float | % – populated for universities and colleges only |
| graduate_outcome_pct | float | % – populated for universities and colleges only |
| attendance_rate_pct | float | % – populated for primary, secondary, and college only |

## 6. Cleaning & validation

- **No NULLs** in mandatory fields (`name`, `category`, `region_id`, `city`).
- **All foreign keys valid** – every `institution.region_id` exists in `regions.csv`,
  and every `performance_record.institution_id` exists in `institutions.csv`.
- **Field standardisation**:
  - Categories use a fixed set of 4 values.
  - Ratings use a fixed set per category type.
  - Postcodes use real UK postcode area prefixes for each city.
- **No duplicate names** within the same category.

## 7. How to load into Django

```bash
# from the project root
python manage.py load_data
```

If `manage.py load_data` is not yet wired up, copy `load_data.py` into:

```
institutions/management/commands/load_data.py
```

and add empty `__init__.py` files in `management/` and `management/commands/`.

Alternatively, run as a standalone script (only after migrations have been applied):

```bash
python load_data.py
```

## 8. Regenerating the dataset

The dataset is **fully reproducible**. To regenerate it:

```bash
python generate_dataset.py
```

This will overwrite the three CSV files. The random seed is fixed (`seed=42`)
so the output is identical every time.

## 9. Sources

- University and college lists: compiled from publicly available UK government
  data (gov.uk – *Get Information about Schools*, HESA, Ofsted) and the
  official websites of each institution.
- Region definitions: UK Office for National Statistics (ONS) regions.
- Postcode prefixes: Royal Mail postcode area codes.
- School names: generated from realistic UK naming conventions (saint names,
  geographical names, royal names, etc.).
- Performance data: synthetic, but distributed to match real-world Ofsted
  rating distributions in England (≈20% Outstanding, ≈65% Good,
  ≈12% Requires Improvement, ≈3% Inadequate).
