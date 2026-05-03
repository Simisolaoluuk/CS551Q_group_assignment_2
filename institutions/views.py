from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import OuterRef, Subquery, FloatField
from .models import Region, Institution, PerformanceRecord


def institutions_with_latest_performance(queryset):
    latest_record = PerformanceRecord.objects.filter(
        institution=OuterRef("pk")
    ).order_by("-year")

    return queryset.annotate(
        latest_score=Subquery(
            latest_record.values("score")[:1],
            output_field=FloatField()
        ),
        latest_attendance=Subquery(
            latest_record.values("attendance")[:1],
            output_field=FloatField()
        ),
    )


def home(request):
    aberdeen = Region.objects.filter(name__iexact="Aberdeen").first()
    top_aberdeen_unis = Institution.objects.none()

    if aberdeen:
        top_aberdeen_unis = institutions_with_latest_performance(
            Institution.objects.filter(region=aberdeen, type="UNIVERSITY")
        ).order_by("-latest_score", "-latest_attendance")[:3]

    return render(request, "institutions/home.html", {
        "top_aberdeen_unis": top_aberdeen_unis
    })


def institution_list(request):
    institution_type = request.GET.get("type", "PRIMARY")
    region = request.GET.get("region")
    search_query = request.GET.get("q")
    sort = request.GET.get("sort", "score")

    institutions = Institution.objects.filter(type=institution_type)

    if region:
        institutions = institutions.filter(region__name__iexact=region)

    if search_query:
        institutions = institutions.filter(name__icontains=search_query)

    institutions = institutions_with_latest_performance(institutions)

    if sort == "name":
        institutions = institutions.order_by("name")
    else:
        institutions = institutions.order_by("-latest_score", "-latest_attendance")

    paginator = Paginator(institutions, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    regions = Region.objects.all().order_by("name")

    return render(request, "institutions/institution_list.html", {
        "page_obj": page_obj,
        "regions": regions,
        "selected_type": institution_type,
    })


def institution_detail(request, pk):
    institution = get_object_or_404(Institution, pk=pk)

    records = PerformanceRecord.objects.filter(
        institution=institution
    ).order_by("year")

    latest_record = records.order_by("-year").first()

    chart_years = [record.year for record in records]
    chart_scores = [record.score for record in records]
    chart_attendance = [record.attendance for record in records]

    return render(request, "institutions/institution_detail.html", {
        "institution": institution,
        "records": records,
        "latest_record": latest_record,
        "chart_years": chart_years,
        "chart_scores": chart_scores,
        "chart_attendance": chart_attendance,
    })


def compare_institutions(request):
    ids = request.GET.getlist("institution_ids")

    if len(ids) < 2:
        messages.error(request, "Please select at least 2 institutions to compare.")
        return redirect("institution_list")

    if len(ids) > 3:
        messages.error(request, "You can compare a maximum of 3 institutions.")
        return redirect("institution_list")

    institutions = institutions_with_latest_performance(
        Institution.objects.filter(id__in=ids)
    )

    institutions = list(institutions)

    if len(institutions) < 2:
        messages.error(request, "Selected institutions could not be found.")
        return redirect("institution_list")

    institution_types = {institution.type for institution in institutions}

    if len(institution_types) > 1:
        messages.error(request, "You can only compare institutions of the same type.")
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
        "comparison_type": institutions[0].get_type_display(),
        "best_score": best_score,
        "best_attendance": best_attendance,
        "best_overall": best_overall,
    })


def top_institutions(request):
    institution_type = request.GET.get("type", "UNIVERSITY")
    region_name = request.GET.get("region", "Aberdeen")

    institutions = Institution.objects.filter(type=institution_type)

    if region_name:
        institutions = institutions.filter(region__name__iexact=region_name)

    institutions = institutions_with_latest_performance(institutions).order_by(
        "-latest_score",
        "-latest_attendance"
    )[:10]

    regions = Region.objects.all().order_by("name")

    return render(request, "institutions/top_institutions.html", {
        "institutions": institutions,
        "regions": regions,
        "selected_type": institution_type,
        "selected_region": region_name,
    })