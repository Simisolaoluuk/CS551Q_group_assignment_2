from django.db import models


class Region(models.Model):
    '''Region Model: Stores geographical areas like Aberdeen, London, Glasgow, etc. Each institution belongs to one region. '''

    # Name of the region (e.g. "Aberdeen")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Institution(models.Model):
    '''Institution Model: Represents schools, colleges, or universities. Each institution is linked to one region.'''

    # Fixed list of allowed institution types
    TYPE_CHOICES = [
        ('PRIMARY', 'Primary'),
        ('SECONDARY', 'Secondary'),
        ('COLLEGE', 'College'),
        ('UNIVERSITY', 'University'),
    ]

    # Name of the institution (e.g. "University of Aberdeen")
    name = models.CharField(max_length=200)

    # Links institution to a region (many institutions per region)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    # Type of institution (restricted to TYPE_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name


class PerformanceRecord(models.Model):
    '''Performance Record Model: Stores yearly performance data for each institution. This allows ranking and trend analysis.''' 

    # Links each record to one institution
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    # Year of the record (e.g. 2024, 2025)
    year = models.IntegerField()

    # Academic performance score (used for ranking)
    score = models.FloatField()

    # Attendance percentage
    attendance = models.FloatField()

    def __str__(self):
        return f"{self.institution.name} - {self.year}"

