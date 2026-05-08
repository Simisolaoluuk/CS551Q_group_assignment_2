from io import StringIO
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse
from .models import (FavouriteInstitution, Institution, PerformanceRecord, Region,)


class InstitutionDashboardTests(TestCase):
    """Tests for models, views, authentication, favourites, comparison and filters."""

    def setUp(self):
        """Create reusable test data before each test."""

        self.client = Client()

        # Create test user
        self.user = User.objects.create_user(
            username="testuser",
            password="user1234"
        )

        # Create test region
        self.region = Region.objects.create(
            name="Scotland",
            country="Scotland"
        )

        # Create first university
        self.uni1 = Institution.objects.create(
            name="University of Aberdeen",
            category="University",
            region=self.region,
            city="Aberdeen",
            postcode="AB24 3FX",
            founded_year=1495
        )

        # Create second university for comparison tests
        self.uni2 = Institution.objects.create(
            name="Robert Gordon University",
            category="University",
            region=self.region,
            city="Aberdeen",
            postcode="AB10 7QB",
            founded_year=1992
        )

        # Create primary school for category validation tests
        self.primary_school = Institution.objects.create(
            name="Aberdeen Primary School",
            category="Primary School",
            region=self.region,
            city="Aberdeen",
            postcode="AB11 1AA",
            founded_year=1980
        )

        # Create performance record for first university
        PerformanceRecord.objects.create(
            institution=self.uni1,
            year=2024,
            rating="Gold",
            overall_score=92,
            student_satisfaction_pct=88,
            graduate_outcome_pct=90,
            attendance_rate_pct=None
        )

        # Create performance record for second university
        PerformanceRecord.objects.create(
            institution=self.uni2,
            year=2024,
            rating="Silver",
            overall_score=84,
            student_satisfaction_pct=82,
            graduate_outcome_pct=80,
            attendance_rate_pct=None
        )

        # Create performance record for primary school
        PerformanceRecord.objects.create(
            institution=self.primary_school,
            year=2024,
            rating="Good",
            overall_score=76,
            student_satisfaction_pct=None,
            graduate_outcome_pct=None,
            attendance_rate_pct=95
        )


    # Basic page/view tests

    def test_home_page_loads(self):
        """Home page should load successfully."""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Institution Dashboard")

    def test_institution_list_page_loads(self):
        """Institution list page should load successfully."""
        response = self.client.get(reverse("institution_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Browse Institutions")

    def test_top_institutions_page_loads(self):
        """Top institutions page should load successfully."""
        response = self.client.get(reverse("top_institutions"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Top Institutions")

    def test_register_page_loads(self):
        """Registration page should load successfully."""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")

    def test_login_page_loads(self):
        """Login page should load successfully."""
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    
    # Institution detail tests
    def test_institution_detail_page_displays_correct_institution(self):
        """Detail page should display selected institution and metrics."""
        response = self.client.get(
            reverse("institution_detail", args=[self.uni1.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "University of Aberdeen")
        self.assertContains(response, "Performance Trend")
        self.assertContains(response, "92")

    def test_invalid_institution_detail_returns_404(self):
        """Invalid institution ID should return 404."""
        response = self.client.get(
            reverse("institution_detail", args=[99999])
        )

        self.assertEqual(response.status_code, 404)

    def test_institution_detail_shows_performance_summary(self):
        """Detail page should show analytical performance summary."""
        response = self.client.get(
            reverse("institution_detail", args=[self.uni1.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Performance Summary")
        self.assertContains(response, "Performance level")
        self.assertContains(response, "Strong")

    def test_institution_detail_shows_regional_average(self):
        """Detail page should compare institution score with regional average."""
        response = self.client.get(
            reverse("institution_detail", args=[self.uni1.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Regional average score")
        self.assertContains(response, "regional average")

    def test_institution_detail_without_performance_data(self):
        """Detail page should handle institutions with no performance data."""
        institution_without_data = Institution.objects.create(
            name="No Data Institution",
            category="University",
            region=self.region,
            city="Aberdeen"
        )

        response = self.client.get(
            reverse("institution_detail", args=[institution_without_data.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No performance data available")
        self.assertContains(response, "No chart data available")


    # Search and filter tests
    def test_search_institution_name(self):
        """Search should return matching institution names."""
        response = self.client.get(
            reverse("institution_list"),
            {
                "category": "University",
                "q": "Aberdeen"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "University of Aberdeen")
        self.assertNotContains(response, "Robert Gordon University")

    def test_filter_by_category(self):
        """Category filter should show only matching category."""
        response = self.client.get(
            reverse("institution_list"),
            {
                "category": "Primary School"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aberdeen Primary School")
        self.assertNotContains(response, "University of Aberdeen")

    def test_filter_by_region(self):
        """Region filter should show institutions from selected region."""
        response = self.client.get(
            reverse("institution_list"),
            {
                "category": "University",
                "region": "Scotland"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "University of Aberdeen")
        self.assertContains(response, "Robert Gordon University")

    def test_empty_search_does_not_crash(self):
        """Search with no matching results should still return page."""
        response = self.client.get(
            reverse("institution_list"),
            {
                "category": "University",
                "q": "NoMatchingInstitutionName"
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_invalid_region_filter_does_not_crash(self):
        """Invalid region filter should not crash the page."""
        response = self.client.get(
            reverse("institution_list"),
            {
                "category": "University",
                "region": "InvalidRegion"
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_invalid_sort_option_does_not_crash(self):
        """Invalid sort option should fall back safely."""
        response = self.client.get(
            reverse("institution_list"),
            {
                "category": "University",
                "sort": "invalid-sort"
            }
        )

        self.assertEqual(response.status_code, 200)

  
    # Top institution tests
    def test_top_institutions_filter(self):
        """Top institutions page should support category and region filters."""
        response = self.client.get(
            reverse("top_institutions"),
            {
                "category": "University",
                "region": "Scotland"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "University of Aberdeen")
        self.assertContains(response, "Robert Gordon University")

    def test_top_institutions_ranking_order(self):
        """Top institutions should be ordered by highest score first."""
        response = self.client.get(
            reverse("top_institutions"),
            {
                "category": "University",
                "region": "Scotland"
            }
        )

        self.assertEqual(response.status_code, 200)

        content = response.content.decode()

        self.assertTrue(
            content.index("University of Aberdeen")
            < content.index("Robert Gordon University")
        )


    # Comparison tests
    def test_compare_same_category_institutions(self):
        """Comparison should work for institutions in the same category."""
        response = self.client.get(
            reverse("compare_institutions"),
            {
                "institution_ids": [self.uni1.id, self.uni2.id]
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Best Overall")
        self.assertContains(response, "University of Aberdeen")

    def test_compare_different_categories_redirects(self):
        """Comparison should reject institutions from different categories."""
        response = self.client.get(
            reverse("compare_institutions"),
            {
                "institution_ids": [self.uni1.id, self.primary_school.id]
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_compare_requires_two_institutions(self):
        """Comparison should require at least two institutions."""
        response = self.client.get(
            reverse("compare_institutions"),
            {
                "institution_ids": [self.uni1.id]
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_compare_rejects_more_than_three_institutions(self):
        """Comparison should reject more than three selected institutions."""
        uni3 = Institution.objects.create(
            name="Third University",
            category="University",
            region=self.region,
            city="Glasgow"
        )

        uni4 = Institution.objects.create(
            name="Fourth University",
            category="University",
            region=self.region,
            city="Edinburgh"
        )

        response = self.client.get(
            reverse("compare_institutions"),
            {
                "institution_ids": [
                    self.uni1.id,
                    self.uni2.id,
                    uni3.id,
                    uni4.id
                ]
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_compare_redirects_when_institution_missing(self):
        """Comparison should redirect if selected institution does not exist."""
        response = self.client.get(
            reverse("compare_institutions"),
            {
                "institution_ids": [self.uni1.id, 99999]
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_compare_shows_best_and_lowest_performers(self):
        """Comparison page should show highest, lowest and score gap."""
        response = self.client.get(
            reverse("compare_institutions"),
            {
                "institution_ids": [self.uni1.id, self.uni2.id]
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Highest performing")
        self.assertContains(response, "Lowest performing")
        self.assertContains(response, "Score gap")


    # Authentication tests
    def test_user_registration(self):
        """Valid user registration should create account and redirect home."""
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "ComplexPass123",
                "password2": "ComplexPass123"
            }
        )

        self.assertEqual(
            User.objects.filter(username="newuser").count(),
            1
        )
        self.assertRedirects(response, reverse("home"))

    def test_registration_password_mismatch(self):
        """Registration should fail when passwords do not match."""
        response = self.client.post(
            reverse("register"),
            {
                "username": "user2",
                "email": "user2@example.com",
                "password1": "ComplexPass123",
                "password2": "DifferentPass123"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            User.objects.filter(username="user2").count(),
            0
        )

    def test_user_login(self):
        """Existing user should be able to log in."""
        logged_in = self.client.login(
            username="testuser",
            password="user1234"
        )

        self.assertTrue(logged_in)

    def test_logout_rejects_get_request(self):
        """Logout view should reject GET because it requires POST."""
        self.client.login(username="testuser", password="user1234")

        response = self.client.get(reverse("logout"))

        self.assertEqual(response.status_code, 405)

    def test_logout_works_with_post_request(self):
        """Logout should work with POST and redirect home."""
        self.client.login(username="testuser", password="user1234")

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("home"))


    # Favourite tests
    def test_favourites_redirect_without_login(self):
        """Favourite list should redirect anonymous users to login."""
        response = self.client.get(reverse("favourite_list"))

        self.assertRedirects(
            response,
            f'/login/?next={reverse("favourite_list")}'
        )

    def test_add_favourite_get_redirects_safely(self):
        response = self.client.get(
            reverse("add_favourite", args=[self.uni1.id])
        )

        self.assertEqual(response.status_code, 302)

    def test_remove_favourite_get_redirects_safely(self):
        response = self.client.get(
            reverse("remove_favourite", args=[self.uni1.id])
        )

        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_add_favourite(self):
        """Logged-in user should be able to add favourite using POST."""
        self.client.login(username="testuser", password="user1234")

        response = self.client.post(
            reverse("add_favourite", args=[self.uni1.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            FavouriteInstitution.objects.filter(
                user=self.user,
                institution=self.uni1
            ).count(),
            1
        )

    def test_duplicate_favourites_prevented(self):
        """Adding the same favourite twice should not create duplicates."""
        self.client.login(username="testuser", password="user1234")

        self.client.post(reverse("add_favourite", args=[self.uni1.id]))
        self.client.post(reverse("add_favourite", args=[self.uni1.id]))

        self.assertEqual(
            FavouriteInstitution.objects.filter(
                user=self.user,
                institution=self.uni1
            ).count(),
            1
        )

    def test_logged_in_user_can_view_favourites(self):
        """Logged-in user should see their saved favourites."""
        self.client.login(username="testuser", password="user1234")

        FavouriteInstitution.objects.create(
            user=self.user,
            institution=self.uni1
        )

        response = self.client.get(reverse("favourite_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "University of Aberdeen")

    def test_logged_in_user_can_remove_favourite(self):
        """Logged-in user should be able to remove favourite using POST."""
        self.client.login(username="testuser", password="user1234")

        FavouriteInstitution.objects.create(
            user=self.user,
            institution=self.uni1
        )

        response = self.client.post(
            reverse("remove_favourite", args=[self.uni1.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            FavouriteInstitution.objects.filter(
                user=self.user,
                institution=self.uni1
            ).count(),
            0
        )

    def test_add_favourite_rejects_get_request(self):
        """Add favourite view should reject GET requests."""
        self.client.login(username="testuser", password="user1234")

        response = self.client.get(
            reverse("add_favourite", args=[self.uni1.id])
        )

        self.assertEqual(response.status_code, 405)

    def test_remove_favourite_rejects_get_request(self):
        """Remove favourite view should reject GET requests."""
        self.client.login(username="testuser", password="user1234")

        response = self.client.get(
            reverse("remove_favourite", args=[self.uni1.id])
        )

        self.assertEqual(response.status_code, 405)

    
    # Model relationship tests
    def test_model_relationships_connect_region_institution_and_performance(self):
        """Institution should connect correctly to region and performance data."""
        self.assertEqual(self.uni1.region.name, "Scotland")
        self.assertEqual(
            PerformanceRecord.objects.filter(institution=self.uni1).count(),
            1
        )

    def test_favourite_model_relationship(self):
        """Favourite should correctly link a user and institution."""
        favourite = FavouriteInstitution.objects.create(
            user=self.user,
            institution=self.uni1
        )

        self.assertEqual(favourite.user.username, "testuser")
        self.assertEqual(
            favourite.institution.name,
            "University of Aberdeen"
        )


    # Management command tests
    def test_load_data_command_exists(self):
        """load_data management command should exist and run without crashing."""
        output = StringIO()

        try:
            call_command("load_data", stdout=output)
            command_ran = True
        except Exception:
            command_ran = False

        self.assertTrue(command_ran)