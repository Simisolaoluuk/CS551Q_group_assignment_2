from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Institution(models.Model):
    CATEGORY_CHOICES = [
        ("Primary School", "Primary School"),
        ("Secondary School", "Secondary School"),
        ("College", "College"),
        ("University", "University"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    city = models.CharField(max_length=100, blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    founded_year = models.IntegerField(null=True, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class PerformanceRecord(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    year = models.IntegerField()

    rating = models.CharField(max_length=50, blank=True)
    overall_score = models.FloatField()
    student_satisfaction_pct = models.FloatField(null=True, blank=True)
    graduate_outcome_pct = models.FloatField(null=True, blank=True)
    attendance_rate_pct = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.institution.name} - {self.year}"