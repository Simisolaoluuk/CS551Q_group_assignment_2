from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.db.models import OuterRef, Subquery, FloatField
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm
from .models import Region, Institution, PerformanceRecord, FavouriteInstitution


def institutions_with_latest_performance(queryset):
    latest_record = PerformanceRecord.objects.filter(
        institution=OuterRef("pk")
    ).order_by("-year")

    return queryset.annotate(
        latest_score=Subquery(latest_record.values("overall_score")[:1], output_field=FloatField()),
        latest_attendance=Subquery(latest_record.values("attendance_rate_pct")[:1], output_field=FloatField()),
    )


def home(request):
    top_institutions_by_category = []

    for category_value, category_label in Institution.CATEGORY_CHOICES:
        top_institutions = institutions_with_latest_performance(
            Institution.objects.filter(category=category_value)
        ).order_by("-latest_score")[:3]

        top_institutions_by_category.append({
            "category_label": category_label,
            "institutions": top_institutions,
        })

    return render(request, "institutions/home.html", {
        "top_institutions_by_category": top_institutions_by_category
    })


def institution_list(request):
    institution_category = request.GET.get("category", "Primary School")
    region = request.GET.get("region")
    search_query = request.GET.get("q")
    sort = request.GET.get("sort", "score")

    institutions = Institution.objects.filter(category=institution_category)

    if region:
        institutions = institutions.filter(region__name__iexact=region)

    if search_query:
        institutions = institutions.filter(name__icontains=search_query)

    institutions = institutions_with_latest_performance(institutions)

    if sort == "name":
        institutions = institutions.order_by("name")
    else:
        institutions = institutions.order_by("-latest_score")

    paginator = Paginator(institutions, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "institutions/institution_list.html", {
        "page_obj": page_obj,
        "regions": Region.objects.all().order_by("name"),
        "selected_category": institution_category,
        "selected_region": region,
        "selected_sort": sort,
        "search_query": search_query,
        "category_choices": Institution.CATEGORY_CHOICES,
    })


def institution_detail(request, pk):
    institution = get_object_or_404(Institution, pk=pk)

    records = PerformanceRecord.objects.filter(
        institution=institution
    ).order_by("year")

    latest_record = records.order_by("-year").first()

    chart_years = [record.year for record in records]
    chart_scores = [record.overall_score for record in records]
    chart_attendance = [
        record.attendance_rate_pct if record.attendance_rate_pct is not None else 0
        for record in records
    ]

    # Favourite check
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


def compare_institutions(request):
    ids = request.GET.getlist("institution_ids")

    if len(ids) < 2:
        messages.error(request, "Please select at least 2 institutions to compare.")
        return redirect("institution_list")

    if len(ids) > 3:
        messages.error(request, "You can compare a maximum of 3 institutions.")
        return redirect("institution_list")

    institutions = list(institutions_with_latest_performance(
        Institution.objects.filter(id__in=ids)
    ))

    if len(institutions) < 2:
        messages.error(request, "Selected institutions could not be found.")
        return redirect("institution_list")

    if len({institution.category for institution in institutions}) > 1:
        messages.error(request, "You can only compare institutions of the same category.")
        return redirect("institution_list")

    best_score = max(institution.latest_score or 0 for institution in institutions)
    best_attendance = max(institution.latest_attendance or 0 for institution in institutions)

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


def top_institutions(request):
    institution_category = request.GET.get("category", "University")
    region_name = request.GET.get("region")

    institutions = Institution.objects.filter(category=institution_category)

    if region_name:
        institutions = institutions.filter(region__name__iexact=region_name)

    institutions = institutions_with_latest_performance(institutions).order_by("-latest_score")[:10]

    return render(request, "institutions/top_institutions.html", {
        "institutions": institutions,
        "regions": Region.objects.all().order_by("name"),
        "selected_category": institution_category,
        "selected_region": region_name,
        "category_choices": Institution.CATEGORY_CHOICES,
    })


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"]
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(request, "institutions/login.html", {
        "form": form
    })

def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)

        messages.success(request, "Registration successful.")

        return redirect("home")

    return render(request, "institutions/register.html", {
        "form": form
    })


@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def add_favourite(request, pk):
    institution = get_object_or_404(Institution, pk=pk)

    FavouriteInstitution.objects.get_or_create(
        user=request.user,
        institution=institution
    )

    messages.success(request, "Institution added to favourites.")
    return redirect("institution_detail", pk=pk)


@login_required
def remove_favourite(request, pk):
    institution = get_object_or_404(Institution, pk=pk)

    FavouriteInstitution.objects.filter(
        user=request.user,
        institution=institution
    ).delete()

    messages.success(request, "Institution removed from favourites.")
    return redirect("institution_detail", pk=pk)


@login_required
def favourite_list(request):
    favourites = FavouriteInstitution.objects.filter(
        user=request.user
    ).select_related("institution", "institution__region")

    return render(request, "institutions/favourites.html", {
        "favourites": favourites
    })