from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.db.models import OuterRef, Subquery, FloatField
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm
from .models import (
    Region,
    Institution,
    PerformanceRecord,
    FavouriteInstitution
)


# Add latest performance data to institution queryset
def institutions_with_latest_performance(queryset):

    # Get newest performance record for each institution
    latest_record = PerformanceRecord.objects.filter(
        institution=OuterRef("pk")
    ).order_by("-year")

    # Attach latest score and attendance using subqueries
    return queryset.annotate(
        latest_score=Subquery(
            latest_record.values("overall_score")[:1],
            output_field=FloatField()
        ),
        latest_attendance=Subquery(
            latest_record.values("attendance_rate_pct")[:1],
            output_field=FloatField()
        ),
    )


# Homepage view
def home(request):

    # Store top institutions grouped by category
    top_institutions_by_category = []

    # Loop through each institution category
    for category_value, category_label in Institution.CATEGORY_CHOICES:

        # Get top 3 institutions by latest score
        top_institutions = institutions_with_latest_performance(
            Institution.objects.filter(category=category_value)
        ).order_by("-latest_score")[:3]

        # Save results
        top_institutions_by_category.append({
            "category_label": category_label,
            "institutions": top_institutions,
        })

    return render(request, "institutions/home.html", {
        "top_institutions_by_category": top_institutions_by_category
    })


# Institution list page with filtering and sorting
def institution_list(request):

    # Get filter values from URL
    institution_category = request.GET.get(
        "category",
        "Primary School"
    )

    region = request.GET.get("region")
    search_query = request.GET.get("q")

    # Default sorting by score
    sort = request.GET.get("sort", "score")

    # Start queryset
    institutions = Institution.objects.filter(
        category=institution_category
    )

    # Filter by region
    if region:
        institutions = institutions.filter(
            region__name__iexact=region
        )

    # Search by institution name
    if search_query:
        institutions = institutions.filter(
            name__icontains=search_query
        )

    # Add latest performance data
    institutions = institutions_with_latest_performance(
        institutions
    )

    # Sorting
    if sort == "name":
        institutions = institutions.order_by("name")
    else:
        institutions = institutions.order_by("-latest_score")

    # Pagination (20 per page)
    paginator = Paginator(institutions, 20)

    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(request, "institutions/institution_list.html", {
        "page_obj": page_obj,
        "regions": Region.objects.all().order_by("name"),
        "selected_category": institution_category,
        "selected_region": region,
        "selected_sort": sort,
        "search_query": search_query,
        "category_choices": Institution.CATEGORY_CHOICES,
    })


# Institution detail page
def institution_detail(request, pk):

    # Get institution or return 404
    institution = get_object_or_404(
        Institution,
        pk=pk
    )

    # Get all performance records
    records = PerformanceRecord.objects.filter(
        institution=institution
    ).order_by("year")

    # Get latest performance record
    latest_record = records.order_by("-year").first()

    # Data for charts
    chart_years = [record.year for record in records]

    chart_scores = [
        record.overall_score
        for record in records
    ]

    chart_attendance = [
        record.attendance_rate_pct
        if record.attendance_rate_pct is not None
        else 0
        for record in records
    ]

    # Check if institution is in user's favourites
    is_favourite = False

    if request.user.is_authenticated:
        is_favourite = FavouriteInstitution.objects.filter(
            user=request.user,
            institution=institution
        ).exists()

    return render(request, "institutions/institution_detail.html", {
        "institution": institution,
        "records": records,
        "latest_record": latest_record,
        "chart_years": chart_years,
        "chart_scores": chart_scores,
        "chart_attendance": chart_attendance,
        "is_favourite": is_favourite,
    })


# Compare multiple institutions
def compare_institutions(request):

    # Get selected institution IDs
    ids = request.GET.getlist("institution_ids")

    # Validation: minimum 2 institutions
    if len(ids) < 2:
        messages.error(
            request,
            "Please select at least 2 institutions to compare."
        )
        return redirect("institution_list")

    # Validation: maximum 3 institutions
    if len(ids) > 3:
        messages.error(
            request,
            "You can compare a maximum of 3 institutions."
        )
        return redirect("institution_list")

    # Fetch selected institutions
    institutions = list(
        institutions_with_latest_performance(
            Institution.objects.filter(id__in=ids)
        )
    )

    # Validation: ensure institutions exist
    if len(institutions) < 2:
        messages.error(
            request,
            "Selected institutions could not be found."
        )
        return redirect("institution_list")

    # Validation: same category only
    if len({
        institution.category
        for institution in institutions
    }) > 1:

        messages.error(
            request,
            "You can only compare institutions of the same category."
        )

        return redirect("institution_list")

    # Find highest latest score
    best_score = max(
        institution.latest_score or 0
        for institution in institutions
    )

    # Find highest attendance
    best_attendance = max(
        institution.latest_attendance or 0
        for institution in institutions
    )

    # Best overall institution
    best_overall = max(
        institutions,
        key=lambda institution: (
            institution.latest_score or 0,
            institution.latest_attendance or 0
        )
    )

    return render(request, "institutions/comparison.html", {
        "institutions": institutions,
        "comparison_type": institutions[0].get_category_display(),
        "best_score": best_score,
        "best_attendance": best_attendance,
        "best_overall": best_overall,
    })


# Top institutions page
def top_institutions(request):

    # Get filters
    institution_category = request.GET.get(
        "category",
        "University"
    )

    region_name = request.GET.get("region")

    # Filter institutions by category
    institutions = Institution.objects.filter(
        category=institution_category
    )

    # Optional region filter
    if region_name:
        institutions = institutions.filter(
            region__name__iexact=region_name
        )

    # Get top 10 institutions
    institutions = institutions_with_latest_performance(
        institutions
    ).order_by("-latest_score")[:10]

    return render(request, "institutions/top_institutions.html", {
        "institutions": institutions,
        "regions": Region.objects.all().order_by("name"),
        "selected_category": institution_category,
        "selected_region": region_name,
        "category_choices": Institution.CATEGORY_CHOICES,
    })


# User login view
def login_view(request):

    form = LoginForm(request.POST or None)

    # Handle form submission
    if request.method == "POST" and form.is_valid():

        # Authenticate user
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )

        # Successful login
        if user is not None:
            login(request, user)
            return redirect("home")

        # Invalid login
        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "institutions/login.html", {
        "form": form
    })


# User registration view
def register_view(request):

    form = RegisterForm(request.POST or None)

    # Handle registration form
    if request.method == "POST" and form.is_valid():

        # Save user
        user = form.save()

        # Auto login after registration
        login(request, user)

        messages.success(
            request,
            "Registration successful."
        )

        return redirect("home")

    return render(request, "institutions/register.html", {
        "form": form
    })


# Logout user
@require_POST
def logout_view(request):

    logout(request)

    return redirect("home")


# Add institution to favourites
@login_required
@require_POST
def add_favourite(request, pk):

    institution = get_object_or_404(
        Institution,
        pk=pk
    )

    # Prevent duplicate favourites
    FavouriteInstitution.objects.get_or_create(
        user=request.user,
        institution=institution
    )

    messages.success(
        request,
        "Institution added to favourites."
    )

    return redirect("institution_detail", pk=pk)


# Remove institution from favourites
@login_required
@require_POST
def remove_favourite(request, pk):

    institution = get_object_or_404(
        Institution,
        pk=pk
    )

    FavouriteInstitution.objects.filter(
        user=request.user,
        institution=institution
    ).delete()

    messages.success(
        request,
        "Institution removed from favourites."
    )

    return redirect("institution_detail", pk=pk)


# Show logged-in user's favourites
@login_required
def favourite_list(request):

    favourites = FavouriteInstitution.objects.filter(
        user=request.user
    ).select_related(
        "institution",
        "institution__region"
    )

    return render(request, "institutions/favourites.html", {
        "favourites": favourites
    })