from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Institution(models.Model):
    TYPE_CHOICES = [
        ('PRIMARY', 'Primary'),
        ('SECONDARY', 'Secondary'),
        ('COLLEGE', 'College'),
        ('UNIVERSITY', 'University'),
    ]

    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name
    
class PerformanceRecord(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    year = models.IntegerField()
    score = models.FloatField()
    attendance = models.FloatField()

    def __str__(self):
        return f"{self.institution.name} - {self.year}"

