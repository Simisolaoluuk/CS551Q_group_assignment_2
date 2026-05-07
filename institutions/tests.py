from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Region, Institution, PerformanceRecord, FavouriteInstitution


class InstitutionDashboardTests(TestCase):

    def setUp(self):
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

        # Create university institution
        self.uni1 = Institution.objects.create(
            name="University of Aberdeen",
            category="University",
            region=self.region,
            city="Aberdeen",
            postcode="AB24 3FX",
            founded_year=1495
        )

        # Create second university institution
        self.uni2 = Institution.objects.create(
            name="Robert Gordon University",
            category="University",
            region=self.region,
            city="Aberdeen",
            postcode="AB10 7QB",
            founded_year=1992
        )

        # Create primary school institution
        self.primary_school = Institution.objects.create(
            name="Aberdeen Primary School",
            category="Primary School",
            region=self.region,
            city="Aberdeen",
            postcode="AB11 1AA",
            founded_year=1980
        )

        # Create performance records
        PerformanceRecord.objects.create(
            institution=self.uni1,
            year=2024,
            rating="Gold",
            overall_score=92,
            student_satisfaction_pct=88,
            graduate_outcome_pct=90,
            attendance_rate_pct=None
        )

        PerformanceRecord.objects.create(
            institution=self.uni2,
            year=2024,
            rating="Silver",
            overall_score=84,
            student_satisfaction_pct=82,
            graduate_outcome_pct=80,
            attendance_rate_pct=None
        )

        PerformanceRecord.objects.create(
            institution=self.primary_school,
            year=2024,
            rating="Good",
            overall_score=76,
            student_satisfaction_pct=None,
            graduate_outcome_pct=None,
            attendance_rate_pct=95
        )

    # 1. Home page loads
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Institution Dashboard")

    # 2. Institution list page loads
    def test_institution_list_page_loads(self):
        response = self.client.get(reverse("institution_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Browse Institutions")

    # 3. Institution detail page displays correct institution
    def test_institution_detail_page(self):
        response = self.client.get(
            reverse("institution_detail", args=[self.uni1.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "University of Aberdeen")
        self.assertContains(response, "Performance Trend")
        self.assertContains(response, "92")

    # 4. Invalid institution detail returns 404
    def test_institution_detail_invalid_id(self):
        response = self.client.get(
            reverse("institution_detail", args=[999])
        )
        self.assertEqual(response.status_code, 404)

    # 5. Search by institution name works
    def test_search_institution_name(self):
        response = self.client.get(
            reverse("institution_list") + "?category=University&q=Aberdeen"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "University of Aberdeen")
        self.assertNotContains(response, "Robert Gordon University")

    # 6. Filter by category works
    def test_filter_by_category(self):
        response = self.client.get(
            reverse("institution_list") + "?category=Primary School"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aberdeen Primary School")
        self.assertNotContains(response, "University of Aberdeen")

    # 7. Filter by region works
    def test_filter_by_region(self):
        response = self.client.get(
            reverse("institution_list") + "?category=University&region=Scotland"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "University of Aberdeen")
        self.assertContains(response, "Robert Gordon University")

    # 8. Top institutions page loads
    def test_top_institutions_page_loads(self):
        response = self.client.get(reverse("top_institutions"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Top Institutions")

    # 9. Top institutions filter works
    def test_top_institutions_filter(self):
        response = self.client.get(
            reverse("top_institutions") + "?category=University&region=Scotland"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "University of Aberdeen")
        self.assertContains(response, "Robert Gordon University")

    # 10. Compare same category institutions works
    def test_compare_same_category(self):
        response = self.client.get(
            reverse("compare_institutions"),
            {
                "institution_ids": [self.uni1.id, self.uni2.id]
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Best Overall")
        self.assertContains(response, "University of Aberdeen")

    # 11. Compare different categories redirects
    def test_compare_different_categories_redirects(self):
        response = self.client.get(
            reverse("compare_institutions"),
            {
                "institution_ids": [self.uni1.id, self.primary_school.id]
            }
        )
        self.assertEqual(response.status_code, 302)

    # 12. Compare with fewer than 2 institutions redirects
    def test_compare_requires_two_institutions(self):
        response = self.client.get(
            reverse("compare_institutions"),
            {
                "institution_ids": [self.uni1.id]
            }
        )
        self.assertEqual(response.status_code, 302)

    # 13. Register page loads
    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")

    # 14. User registration works
    def test_user_registration(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "ComplexPass123",
            "password2": "ComplexPass123"
        })

        self.assertEqual(User.objects.filter(username="newuser").count(), 1)
        self.assertRedirects(response, reverse("home"))

    # 15. Invalid registration password mismatch
    def test_registration_password_mismatch(self):
        response = self.client.post(reverse("register"), {
            "username": "user2",
            "email": "user2@example.com",
            "password1": "ComplexPass123",
            "password2": "DifferentPass123"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(username="user2").count(), 0)

    # 16. Login page loads
    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    # 17. User login works
    def test_user_login(self):
        login = self.client.login(
            username="testuser",
            password="user1234"
        )
        self.assertTrue(login)

    # 18. Favourite page redirects without login
    def test_favourites_redirect_without_login(self):
        response = self.client.get(reverse("favourite_list"))
        self.assertRedirects(
            response,
            f'/login/?next={reverse("favourite_list")}'
        )

    # 19. Add favourite redirects without login
    def test_add_favourite_redirect_without_login(self):
        response = self.client.post(
            reverse("add_favourite", args=[self.uni1.id])
        )
        self.assertRedirects(
            response,
            f'/login/?next={reverse("add_favourite", args=[self.uni1.id])}'
        )

    # 20. Logged in user can add favourite
    def test_logged_in_user_can_add_favourite(self):
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

    # 21. Duplicate favourites are prevented
    def test_duplicate_favourites_prevented(self):
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

    # 22. Logged in user can view favourites page
    def test_logged_in_user_can_view_favourites(self):
        self.client.login(username="testuser", password="user1234")

        FavouriteInstitution.objects.create(
            user=self.user,
            institution=self.uni1
        )

        response = self.client.get(reverse("favourite_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "University of Aberdeen")

    # 23. Logged in user can remove favourite
    def test_logged_in_user_can_remove_favourite(self):
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

    # 24. Remove favourite redirects without login
    def test_remove_favourite_redirect_without_login(self):
        response = self.client.post(
            reverse("remove_favourite", args=[self.uni1.id])
        )

        self.assertRedirects(
            response,
            f'/login/?next={reverse("remove_favourite", args=[self.uni1.id])}'
        )
