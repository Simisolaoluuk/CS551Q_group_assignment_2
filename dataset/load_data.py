"""
Django data loading script for the CS551Q Institution Performance App.

Loads:
  - regions.csv             -> Region model
  - institutions.csv        -> Institution model
  - performance_records.csv -> PerformanceRecord model

USAGE
-----
Place this file inside an app management/commands folder, e.g.:
    institutions/management/commands/load_data.py

Then run:
    python manage.py load_data

Or run as a standalone script:
    python load_data.py

NOTE for the team:
  - This script clears existing rows before inserting, so it is safe to re-run.
  - Field names below assume the models defined in the project plan
    (Region, Institution/School, PerformanceRecord). Adjust the field names
    in the model imports if the backend used different names.
"""

import csv
import os
import sys

# ---------------------------------------------------------------------------
# Set up Django environment (only needed when running as a standalone script).
# When run via "python manage.py load_data", Django is already configured.
# ---------------------------------------------------------------------------
if __name__ == "__main__" and "DJANGO_SETTINGS_MODULE" not in os.environ:
    import django
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edu_dashboard.settings")
    django.setup()

# Import models AFTER Django is configured.
# IMPORTANT: change "institutions" to whatever the backend app is called,
# and adjust class names if needed.
try:
    from institutions.models import Region, Institution, PerformanceRecord
except ImportError:
    # Fallback name – older versions of the plan used "School" instead of "Institution"
    from institutions.models import Region, School as Institution, PerformanceRecord


HERE = os.path.dirname(os.path.abspath(__file__))


def load_regions():
    """Load regions from CSV. Returns a dict {region_id: Region instance}."""
    print("Loading regions...")
    Region.objects.all().delete()
    region_map = {}

    path = os.path.join(HERE, "regions.csv")
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            region = Region.objects.create(
                name=row["name"],
                country=row["country"],
            )
            region_map[int(row["region_id"])] = region
    print(f"  -> {len(region_map)} regions inserted.")
    return region_map


def load_institutions(region_map):
    """Load institutions and link them to regions."""
    print("Loading institutions...")
    Institution.objects.all().delete()
    institution_map = {}

    path = os.path.join(HERE, "institutions.csv")
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            inst = Institution.objects.create(
                name=row["name"],
                category=row["category"],
                region=region_map[int(row["region_id"])],
                city=row["city"],
                postcode=row["postcode"],
                founded_year=int(row["founded_year"]) if row["founded_year"] else None,
                website=row["website"] or "",
            )
            institution_map[int(row["institution_id"])] = inst
    print(f"  -> {len(institution_map)} institutions inserted.")
    return institution_map


def load_performance_records(institution_map):
    """Load performance records linked to institutions."""
    print("Loading performance records...")
    PerformanceRecord.objects.all().delete()
    count = 0

    path = os.path.join(HERE, "performance_records.csv")
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = []
        for row in reader:
            records.append(PerformanceRecord(
                institution=institution_map[int(row["institution_id"])],
                year=int(row["year"]),
                rating=row["rating"],
                overall_score=int(row["overall_score"]),
                student_satisfaction_pct=float(row["student_satisfaction_pct"]) if row["student_satisfaction_pct"] else None,
                graduate_outcome_pct=float(row["graduate_outcome_pct"]) if row["graduate_outcome_pct"] else None,
                attendance_rate_pct=float(row["attendance_rate_pct"]) if row["attendance_rate_pct"] else None,
            ))
        # bulk_create is much faster than create() in a loop
        PerformanceRecord.objects.bulk_create(records, batch_size=500)
        count = len(records)
    print(f"  -> {count} performance records inserted.")


def main():
    print("=" * 60)
    print("Loading UK Institution dataset into the database")
    print("=" * 60)
    region_map = load_regions()
    institution_map = load_institutions(region_map)
    load_performance_records(institution_map)
    print("=" * 60)
    print("All data loaded successfully.")
    print("=" * 60)


# ---------------------------------------------------------------------------
# Django management command wrapper – allows: python manage.py load_data
# ---------------------------------------------------------------------------
try:
    from django.core.management.base import BaseCommand

    class Command(BaseCommand):
        help = "Load UK institution dataset (regions, institutions, performance records) from CSV files."

        def handle(self, *args, **options):
            main()
except ImportError:
    # django not yet importable – that is fine when running standalone
    pass


if __name__ == "__main__":
    main()
