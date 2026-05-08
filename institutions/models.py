from django.db import models
from django.contrib.auth.models import User


# Stores UK regions/countries
class Region(models.Model):

    # Region name (example: Greater London)
    name = models.CharField(max_length=100)

    # Country name (England, Scotland, Wales, etc.)
    country = models.CharField(max_length=100, blank=True)

    # Default ordering when querying regions
    class Meta:
        ordering = ["name"]

    # String representation
    def __str__(self):
        return self.name


# Stores institution information
class Institution(models.Model):

    # Dropdown choices for institution category
    CATEGORY_CHOICES = [
        ("Primary School", "Primary School"),
        ("Secondary School", "Secondary School"),
        ("College", "College"),
        ("University", "University"),
    ]

    # Institution name
    name = models.CharField(max_length=200)

    # Institution type/category
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    # Relationship to Region model
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE
    )

    # City where institution is located
    city = models.CharField(
        max_length=100,
        blank=True
    )

    # UK postcode
    postcode = models.CharField(
        max_length=20,
        blank=True
    )

    # Year institution was founded
    founded_year = models.IntegerField(
        null=True,
        blank=True
    )

    # Default ordering
    class Meta:
        ordering = ["name"]

    # String representation
    def __str__(self):
        return self.name


# Stores yearly performance data for institutions
class PerformanceRecord(models.Model):

    # Linked institution
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE
    )

    # Performance year
    year = models.IntegerField()

    # Rating (Outstanding, Good, Gold, Silver, etc.)
    rating = models.CharField(
        max_length=50,
        blank=True
    )

    # Overall performance score
    overall_score = models.FloatField()

    # Student satisfaction percentage
    student_satisfaction_pct = models.FloatField(
        null=True,
        blank=True
    )

    # Graduate employment/outcome percentage
    graduate_outcome_pct = models.FloatField(
        null=True,
        blank=True
    )

    # Attendance rate percentage
    attendance_rate_pct = models.FloatField(
        null=True,
        blank=True
    )

    # Show newest records first
    class Meta:
        ordering = ["-year"]

    # String display
    def __str__(self):
        return f"{self.institution.name} - {self.year}"


# Stores user's favourite institutions
class FavouriteInstitution(models.Model):

    # User who favourited the institution
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # Institution added to favourites
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE
    )

    # Automatically stores when favourite was created
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        # Prevent duplicate favourites
        unique_together = ("user", "institution")

        # Show latest favourites first
        ordering = ["-created_at"]

    # String representation
    def __str__(self):
        return f"{self.user.username} - {self.institution.name}"