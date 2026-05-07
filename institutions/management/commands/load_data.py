# load the csv data into the django database
# put this file in: institutions/management/commands/load_data.py
# then run: python manage.py load_data

import csv
import os
from django.core.management.base import BaseCommand
from institutions.models import Region, Institution, PerformanceRecord


class Command(BaseCommand):
    help = "load uk institution dataset from csv files"

    def handle(self, *args, **options):
        # find the dataset folder (one level up from this command)
        # change this path if needed
        base = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base, "..", "..", "..", "dataset")
        data_dir = os.path.abspath(data_dir)

        print("loading from:", data_dir)

        # clear old data first
        PerformanceRecord.objects.all().delete()
        Institution.objects.all().delete()
        Region.objects.all().delete()

        # load regions
        region_map = {}
        with open(os.path.join(data_dir, "regions.csv"), encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # main_city is a new field, may not exist in older models
                kwargs = {
                    "name": row["name"],
                    "country": row["country"],
                }
                if "main_city" in row:
                    kwargs["main_city"] = row["main_city"]

                r = Region.objects.create(**kwargs)
                region_map[int(row["region_id"])] = r
        print("regions done:", len(region_map))

        # load institutions
        inst_map = {}
        with open(os.path.join(data_dir, "institutions.csv"), encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                kwargs = {
                    "name": row["name"],
                    "category": row["category"],
                    "region": region_map[int(row["region_id"])],
                    "city": row["city"],
                    "postcode": row["postcode"],
                    "founded_year": int(row["founded_year"]) if row["founded_year"] else None,
                    "website": row["website"] or "",
                }
                # image_url is a new field, only add it if model has it
                if "image_url" in row:
                    kwargs["image_url"] = row["image_url"]

                inst = Institution.objects.create(**kwargs)
                inst_map[int(row["institution_id"])] = inst
        print("institutions done:", len(inst_map))

        # load performance records
        records = []
        with open(os.path.join(data_dir, "performance_records.csv"), encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(PerformanceRecord(
                    institution=inst_map[int(row["institution_id"])],
                    year=int(row["year"]),
                    rating=row["rating"],
                    overall_score=int(row["overall_score"]),
                    student_satisfaction_pct=float(row["student_satisfaction_pct"]) if row["student_satisfaction_pct"] else None,
                    graduate_outcome_pct=float(row["graduate_outcome_pct"]) if row["graduate_outcome_pct"] else None,
                    attendance_rate_pct=float(row["attendance_rate_pct"]) if row["attendance_rate_pct"] else None,
                ))

        # bulk create is faster
        PerformanceRecord.objects.bulk_create(records, batch_size=500)
        print("performance records done:", len(records))
        print("all data loaded.")