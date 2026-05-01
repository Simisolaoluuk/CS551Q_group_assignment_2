"""
Generate a realistic UK Institutions dataset (1000+ records) for the
CS551Q group project. Covers Primary Schools, Secondary Schools,
Colleges and Universities across all UK regions.

Output files:
  - regions.csv
  - institutions.csv
  - performance_records.csv

Author: Database Manager
"""

import csv
import random
import os

random.seed(42)  # reproducible

# ---------------------------------------------------------------------------
# 1. UK Regions (real official regions / nations)
# ---------------------------------------------------------------------------
REGIONS = [
    # England regions
    ("North East England", "England"),
    ("North West England", "England"),
    ("Yorkshire and the Humber", "England"),
    ("East Midlands", "England"),
    ("West Midlands", "England"),
    ("East of England", "England"),
    ("Greater London", "England"),
    ("South East England", "England"),
    ("South West England", "England"),
    # Devolved nations
    ("Scotland", "Scotland"),
    ("Wales", "Wales"),
    ("Northern Ireland", "Northern Ireland"),
]

# Cities mapped to each region (real cities)
CITY_BY_REGION = {
    "North East England": ["Newcastle upon Tyne", "Sunderland", "Durham", "Middlesbrough", "Gateshead"],
    "North West England": ["Manchester", "Liverpool", "Preston", "Lancaster", "Blackpool", "Chester", "Bolton"],
    "Yorkshire and the Humber": ["Leeds", "Sheffield", "York", "Bradford", "Hull", "Doncaster"],
    "East Midlands": ["Nottingham", "Leicester", "Derby", "Lincoln", "Northampton"],
    "West Midlands": ["Birmingham", "Coventry", "Wolverhampton", "Stoke-on-Trent", "Worcester"],
    "East of England": ["Cambridge", "Norwich", "Ipswich", "Peterborough", "Colchester", "Luton"],
    "Greater London": ["London", "Croydon", "Bromley", "Ealing", "Camden", "Westminster", "Hackney"],
    "South East England": ["Oxford", "Reading", "Brighton", "Southampton", "Portsmouth", "Canterbury", "Milton Keynes"],
    "South West England": ["Bristol", "Bath", "Exeter", "Plymouth", "Bournemouth", "Gloucester"],
    "Scotland": ["Edinburgh", "Glasgow", "Aberdeen", "Dundee", "Stirling", "Inverness"],
    "Wales": ["Cardiff", "Swansea", "Newport", "Bangor", "Wrexham", "Aberystwyth"],
    "Northern Ireland": ["Belfast", "Londonderry", "Lisburn", "Newry", "Armagh"],
}

# ---------------------------------------------------------------------------
# 2. Real UK Universities (a curated sample - all real institutions)
# ---------------------------------------------------------------------------
UNIVERSITIES = [
    # London
    ("Imperial College London", "Greater London", "London"),
    ("University College London", "Greater London", "London"),
    ("King's College London", "Greater London", "London"),
    ("London School of Economics", "Greater London", "London"),
    ("Queen Mary University of London", "Greater London", "London"),
    ("City, University of London", "Greater London", "London"),
    ("Brunel University London", "Greater London", "London"),
    ("Goldsmiths, University of London", "Greater London", "London"),
    ("SOAS University of London", "Greater London", "London"),
    ("University of Westminster", "Greater London", "London"),
    ("University of East London", "Greater London", "London"),
    ("Middlesex University", "Greater London", "London"),
    ("London South Bank University", "Greater London", "London"),
    ("Kingston University", "Greater London", "London"),
    # Oxbridge
    ("University of Oxford", "South East England", "Oxford"),
    ("University of Cambridge", "East of England", "Cambridge"),
    # Russell Group + others
    ("University of Manchester", "North West England", "Manchester"),
    ("University of Liverpool", "North West England", "Liverpool"),
    ("Lancaster University", "North West England", "Lancaster"),
    ("University of Central Lancashire", "North West England", "Preston"),
    ("Liverpool John Moores University", "North West England", "Liverpool"),
    ("Manchester Metropolitan University", "North West England", "Manchester"),
    ("University of Leeds", "Yorkshire and the Humber", "Leeds"),
    ("University of Sheffield", "Yorkshire and the Humber", "Sheffield"),
    ("University of York", "Yorkshire and the Humber", "York"),
    ("University of Bradford", "Yorkshire and the Humber", "Bradford"),
    ("University of Hull", "Yorkshire and the Humber", "Hull"),
    ("Sheffield Hallam University", "Yorkshire and the Humber", "Sheffield"),
    ("Leeds Beckett University", "Yorkshire and the Humber", "Leeds"),
    ("University of Birmingham", "West Midlands", "Birmingham"),
    ("University of Warwick", "West Midlands", "Coventry"),
    ("Aston University", "West Midlands", "Birmingham"),
    ("Coventry University", "West Midlands", "Coventry"),
    ("Birmingham City University", "West Midlands", "Birmingham"),
    ("Keele University", "West Midlands", "Stoke-on-Trent"),
    ("University of Nottingham", "East Midlands", "Nottingham"),
    ("Nottingham Trent University", "East Midlands", "Nottingham"),
    ("University of Leicester", "East Midlands", "Leicester"),
    ("De Montfort University", "East Midlands", "Leicester"),
    ("University of Lincoln", "East Midlands", "Lincoln"),
    ("University of Derby", "East Midlands", "Derby"),
    ("University of Bristol", "South West England", "Bristol"),
    ("University of Bath", "South West England", "Bath"),
    ("University of Exeter", "South West England", "Exeter"),
    ("University of Plymouth", "South West England", "Plymouth"),
    ("Bath Spa University", "South West England", "Bath"),
    ("University of the West of England", "South West England", "Bristol"),
    ("Bournemouth University", "South West England", "Bournemouth"),
    ("University of Southampton", "South East England", "Southampton"),
    ("University of Reading", "South East England", "Reading"),
    ("University of Sussex", "South East England", "Brighton"),
    ("University of Brighton", "South East England", "Brighton"),
    ("University of Portsmouth", "South East England", "Portsmouth"),
    ("University of Kent", "South East England", "Canterbury"),
    ("Oxford Brookes University", "South East England", "Oxford"),
    ("University of Surrey", "South East England", "Reading"),
    ("Anglia Ruskin University", "East of England", "Cambridge"),
    ("University of East Anglia", "East of England", "Norwich"),
    ("University of Essex", "East of England", "Colchester"),
    ("University of Hertfordshire", "East of England", "Luton"),
    ("Newcastle University", "North East England", "Newcastle upon Tyne"),
    ("Durham University", "North East England", "Durham"),
    ("Northumbria University", "North East England", "Newcastle upon Tyne"),
    ("Teesside University", "North East England", "Middlesbrough"),
    # Scotland
    ("University of Edinburgh", "Scotland", "Edinburgh"),
    ("University of Glasgow", "Scotland", "Glasgow"),
    ("University of St Andrews", "Scotland", "Edinburgh"),
    ("University of Aberdeen", "Scotland", "Aberdeen"),
    ("University of Dundee", "Scotland", "Dundee"),
    ("University of Stirling", "Scotland", "Stirling"),
    ("Heriot-Watt University", "Scotland", "Edinburgh"),
    ("University of Strathclyde", "Scotland", "Glasgow"),
    ("Edinburgh Napier University", "Scotland", "Edinburgh"),
    ("Glasgow Caledonian University", "Scotland", "Glasgow"),
    ("Robert Gordon University", "Scotland", "Aberdeen"),
    # Wales
    ("Cardiff University", "Wales", "Cardiff"),
    ("Swansea University", "Wales", "Swansea"),
    ("Aberystwyth University", "Wales", "Aberystwyth"),
    ("Bangor University", "Wales", "Bangor"),
    ("Cardiff Metropolitan University", "Wales", "Cardiff"),
    ("University of South Wales", "Wales", "Newport"),
    # Northern Ireland
    ("Queen's University Belfast", "Northern Ireland", "Belfast"),
    ("Ulster University", "Northern Ireland", "Belfast"),
]

# ---------------------------------------------------------------------------
# 3. Real UK Colleges (a curated sample of FE / sixth form colleges)
# ---------------------------------------------------------------------------
COLLEGES = [
    ("City of Bristol College", "South West England", "Bristol"),
    ("Bath College", "South West England", "Bath"),
    ("Exeter College", "South West England", "Exeter"),
    ("Plymouth College of Art", "South West England", "Plymouth"),
    ("South Devon College", "South West England", "Plymouth"),
    ("Gloucestershire College", "South West England", "Gloucester"),
    ("Cornwall College", "South West England", "Plymouth"),
    ("New College Swindon", "South West England", "Bristol"),

    ("Manchester College", "North West England", "Manchester"),
    ("Liverpool City College", "North West England", "Liverpool"),
    ("Preston College", "North West England", "Preston"),
    ("Blackpool and The Fylde College", "North West England", "Blackpool"),
    ("Bolton College", "North West England", "Bolton"),
    ("Salford City College", "North West England", "Manchester"),
    ("Lancaster and Morecambe College", "North West England", "Lancaster"),

    ("Leeds City College", "Yorkshire and the Humber", "Leeds"),
    ("Sheffield College", "Yorkshire and the Humber", "Sheffield"),
    ("Bradford College", "Yorkshire and the Humber", "Bradford"),
    ("York College", "Yorkshire and the Humber", "York"),
    ("Doncaster College", "Yorkshire and the Humber", "Doncaster"),
    ("Hull College", "Yorkshire and the Humber", "Hull"),

    ("Birmingham Metropolitan College", "West Midlands", "Birmingham"),
    ("South and City College Birmingham", "West Midlands", "Birmingham"),
    ("Solihull College", "West Midlands", "Birmingham"),
    ("Coventry College", "West Midlands", "Coventry"),
    ("City of Wolverhampton College", "West Midlands", "Wolverhampton"),
    ("Stoke on Trent College", "West Midlands", "Stoke-on-Trent"),

    ("Nottingham College", "East Midlands", "Nottingham"),
    ("Leicester College", "East Midlands", "Leicester"),
    ("Derby College", "East Midlands", "Derby"),
    ("Lincoln College", "East Midlands", "Lincoln"),
    ("Northampton College", "East Midlands", "Northampton"),

    ("Cambridge Regional College", "East of England", "Cambridge"),
    ("City College Norwich", "East of England", "Norwich"),
    ("Suffolk New College", "East of England", "Ipswich"),
    ("Peterborough College", "East of England", "Peterborough"),
    ("Colchester Institute", "East of England", "Colchester"),

    ("City and Islington College", "Greater London", "London"),
    ("Westminster Kingsway College", "Greater London", "London"),
    ("Ealing, Hammersmith and West London College", "Greater London", "Ealing"),
    ("Croydon College", "Greater London", "Croydon"),
    ("Hackney Community College", "Greater London", "Hackney"),
    ("Newham College", "Greater London", "London"),
    ("Lambeth College", "Greater London", "London"),
    ("Bromley College", "Greater London", "Bromley"),

    ("Oxford City College", "South East England", "Oxford"),
    ("Reading College", "South East England", "Reading"),
    ("Brighton MET College", "South East England", "Brighton"),
    ("Southampton City College", "South East England", "Southampton"),
    ("Portsmouth College", "South East England", "Portsmouth"),
    ("Canterbury College", "South East England", "Canterbury"),
    ("Milton Keynes College", "South East England", "Milton Keynes"),

    ("Newcastle College", "North East England", "Newcastle upon Tyne"),
    ("Sunderland College", "North East England", "Sunderland"),
    ("New College Durham", "North East England", "Durham"),
    ("Middlesbrough College", "North East England", "Middlesbrough"),
    ("Gateshead College", "North East England", "Gateshead"),

    ("Edinburgh College", "Scotland", "Edinburgh"),
    ("Glasgow Clyde College", "Scotland", "Glasgow"),
    ("North East Scotland College", "Scotland", "Aberdeen"),
    ("Dundee and Angus College", "Scotland", "Dundee"),
    ("Forth Valley College", "Scotland", "Stirling"),
    ("Inverness College UHI", "Scotland", "Inverness"),
    ("City of Glasgow College", "Scotland", "Glasgow"),

    ("Cardiff and Vale College", "Wales", "Cardiff"),
    ("Gower College Swansea", "Wales", "Swansea"),
    ("Coleg Gwent", "Wales", "Newport"),
    ("Coleg Cambria", "Wales", "Wrexham"),
    ("Coleg Sir Gar", "Wales", "Swansea"),

    ("Belfast Metropolitan College", "Northern Ireland", "Belfast"),
    ("Northern Regional College", "Northern Ireland", "Lisburn"),
    ("South Eastern Regional College", "Northern Ireland", "Newry"),
    ("South West College", "Northern Ireland", "Armagh"),
]

# ---------------------------------------------------------------------------
# 4. Templates for generating realistic Primary / Secondary school names
# ---------------------------------------------------------------------------
PRIMARY_PREFIXES = [
    "St Mary's", "St John's", "St Peter's", "St Paul's", "St Thomas'",
    "St Andrew's", "St George's", "Holy Trinity", "All Saints", "Sacred Heart",
    "Greenfield", "Oakwood", "Riverside", "Hillside", "Meadow", "Westfield",
    "Eastfield", "Northfield", "Southfield", "Brookfield", "Park", "Highfield",
    "Hawthorn", "Beech", "Elm", "Cedar", "Willow", "Birch", "Maple",
    "Victoria", "Albert", "Queen Elizabeth", "King Edward",
    "Town End", "The Grove", "The Manor", "The Avenue",
    "Ashwood", "Beechwood", "Pinewood", "Forestdale",
]

PRIMARY_SUFFIXES = [
    "Primary School",
    "C of E Primary School",
    "Catholic Primary School",
    "Community Primary School",
    "Junior School",
    "Infant School",
    "Primary Academy",
    "Church School",
]

SECONDARY_PREFIXES = [
    "St Mary's", "St John's", "St Peter's", "St Bede's", "St Edmund's",
    "Holy Cross", "Our Lady's", "Sacred Heart",
    "Highfield", "Westfield", "Eastfield", "Northgate", "Southgate",
    "Park", "Manor", "Heath", "Grange", "Castle", "Abbey",
    "Queen Elizabeth", "King Edward VI", "King's", "Queen's",
    "The Henry", "The William", "The Thomas",
    "Greenacre", "Brookvale", "Riverdale", "Oakridge",
    "City", "County", "Regional",
]

SECONDARY_SUFFIXES = [
    "Academy",
    "High School",
    "Secondary School",
    "Grammar School",
    "Comprehensive School",
    "School",
    "College",  # in UK secondaries are sometimes called Colleges
    "Sixth Form",
]

# Ofsted ratings (England) – used as the rating system for schools
OFSTED = ["Outstanding", "Good", "Requires Improvement", "Inadequate"]
OFSTED_WEIGHTS = [0.20, 0.65, 0.12, 0.03]  # realistic UK distribution

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def make_school_name(level, used_names):
    """Generate a unique realistic school name."""
    if level == "Primary":
        prefixes, suffixes = PRIMARY_PREFIXES, PRIMARY_SUFFIXES
    else:
        prefixes, suffixes = SECONDARY_PREFIXES, SECONDARY_SUFFIXES

    for _ in range(50):  # try up to 50 times to avoid duplicates
        name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
        if name not in used_names:
            used_names.add(name)
            return name
    # fallback: append a number
    n = 1
    while True:
        name = f"{random.choice(prefixes)} {random.choice(suffixes)} {n}"
        if name not in used_names:
            used_names.add(name)
            return name
        n += 1


def make_postcode(city):
    """Generate a plausible UK postcode prefix based on city."""
    prefixes = {
        "London": "SW", "Croydon": "CR", "Bromley": "BR", "Ealing": "W",
        "Camden": "NW", "Westminster": "SW", "Hackney": "E",
        "Manchester": "M", "Liverpool": "L", "Preston": "PR",
        "Lancaster": "LA", "Blackpool": "FY", "Chester": "CH", "Bolton": "BL",
        "Leeds": "LS", "Sheffield": "S", "York": "YO",
        "Bradford": "BD", "Hull": "HU", "Doncaster": "DN",
        "Birmingham": "B", "Coventry": "CV", "Wolverhampton": "WV",
        "Stoke-on-Trent": "ST", "Worcester": "WR",
        "Nottingham": "NG", "Leicester": "LE", "Derby": "DE",
        "Lincoln": "LN", "Northampton": "NN",
        "Cambridge": "CB", "Norwich": "NR", "Ipswich": "IP",
        "Peterborough": "PE", "Colchester": "CO", "Luton": "LU",
        "Oxford": "OX", "Reading": "RG", "Brighton": "BN",
        "Southampton": "SO", "Portsmouth": "PO", "Canterbury": "CT",
        "Milton Keynes": "MK",
        "Bristol": "BS", "Bath": "BA", "Exeter": "EX",
        "Plymouth": "PL", "Bournemouth": "BH", "Gloucester": "GL",
        "Newcastle upon Tyne": "NE", "Sunderland": "SR", "Durham": "DH",
        "Middlesbrough": "TS", "Gateshead": "NE",
        "Edinburgh": "EH", "Glasgow": "G", "Aberdeen": "AB",
        "Dundee": "DD", "Stirling": "FK", "Inverness": "IV",
        "Cardiff": "CF", "Swansea": "SA", "Newport": "NP",
        "Bangor": "LL", "Wrexham": "LL", "Aberystwyth": "SY",
        "Belfast": "BT", "Londonderry": "BT", "Lisburn": "BT",
        "Newry": "BT", "Armagh": "BT",
    }
    p = prefixes.get(city, "XX")
    return f"{p}{random.randint(1, 99)} {random.randint(1, 9)}{random.choice('ABDEFGHJLNPQRSTUWXYZ')}{random.choice('ABDEFGHJLNPQRSTUWXYZ')}"


def weighted_rating():
    return random.choices(OFSTED, weights=OFSTED_WEIGHTS, k=1)[0]


def score_for_rating(rating):
    """Convert Ofsted rating into a numeric score 0–100 (for sorting/ranking)."""
    if rating == "Outstanding":
        return random.randint(85, 100)
    if rating == "Good":
        return random.randint(65, 84)
    if rating == "Requires Improvement":
        return random.randint(45, 64)
    return random.randint(20, 44)


# ---------------------------------------------------------------------------
# Build the dataset
# ---------------------------------------------------------------------------

def build():
    out_dir = os.path.dirname(os.path.abspath(__file__))

    # ---- Regions ----
    regions_rows = []
    region_id_map = {}
    for i, (name, country) in enumerate(REGIONS, start=1):
        region_id_map[name] = i
        regions_rows.append({"region_id": i, "name": name, "country": country})

    # ---- Institutions ----
    institutions = []
    used_names = set()
    inst_id = 1

    # Add all real Universities
    for uni_name, region, city in UNIVERSITIES:
        institutions.append({
            "institution_id": inst_id,
            "name": uni_name,
            "category": "University",
            "region_id": region_id_map[region],
            "region_name": region,
            "city": city,
            "postcode": make_postcode(city),
            "founded_year": random.randint(1100, 2010) if "Oxford" in uni_name or "Cambridge" in uni_name
                else random.randint(1820, 2010),
            "website": "https://www." + uni_name.lower().replace(' ', '').replace(',', '').replace("'", '')[:25] + ".ac.uk",
        })
        used_names.add(uni_name)
        inst_id += 1

    # Add all real Colleges
    for col_name, region, city in COLLEGES:
        institutions.append({
            "institution_id": inst_id,
            "name": col_name,
            "category": "College",
            "region_id": region_id_map[region],
            "region_name": region,
            "city": city,
            "postcode": make_postcode(city),
            "founded_year": random.randint(1900, 2015),
            "website": "https://www." + col_name.lower().replace(' ', '').replace(',', '').replace("'", '')[:25] + ".ac.uk",
        })
        used_names.add(col_name)
        inst_id += 1

    # Generate Primary Schools – aim to push total well past 1000
    # Distribute across regions weighted by population
    region_weights = {
        "Greater London": 18, "South East England": 15, "North West England": 12,
        "West Midlands": 9, "East of England": 9, "Yorkshire and the Humber": 9,
        "South West England": 8, "East Midlands": 7, "Scotland": 8,
        "Wales": 5, "North East England": 4, "Northern Ireland": 3,
    }

    PRIMARY_TOTAL = 700
    SECONDARY_TOTAL = 250

    # Primary schools
    for _ in range(PRIMARY_TOTAL):
        region = random.choices(
            list(region_weights.keys()),
            weights=list(region_weights.values()),
            k=1,
        )[0]
        city = random.choice(CITY_BY_REGION[region])
        name = make_school_name("Primary", used_names)
        institutions.append({
            "institution_id": inst_id,
            "name": name,
            "category": "Primary School",
            "region_id": region_id_map[region],
            "region_name": region,
            "city": city,
            "postcode": make_postcode(city),
            "founded_year": random.randint(1880, 2020),
            "website": "",
        })
        inst_id += 1

    # Secondary schools
    for _ in range(SECONDARY_TOTAL):
        region = random.choices(
            list(region_weights.keys()),
            weights=list(region_weights.values()),
            k=1,
        )[0]
        city = random.choice(CITY_BY_REGION[region])
        name = make_school_name("Secondary", used_names)
        institutions.append({
            "institution_id": inst_id,
            "name": name,
            "category": "Secondary School",
            "region_id": region_id_map[region],
            "region_name": region,
            "city": city,
            "postcode": make_postcode(city),
            "founded_year": random.randint(1850, 2015),
            "website": "",
        })
        inst_id += 1

    # ---- Performance Records ----
    # Each institution gets 3 yearly records (2022, 2023, 2024)
    perf_rows = []
    perf_id = 1
    for inst in institutions:
        cat = inst["category"]
        for year in (2022, 2023, 2024):
            rating = weighted_rating()
            score = score_for_rating(rating)

            if cat == "University":
                # Universities use student satisfaction + ranking instead of Ofsted
                rating_label = (
                    "Gold" if score >= 85 else
                    "Silver" if score >= 65 else
                    "Bronze"
                )
                student_satisfaction = round(random.uniform(70, 95), 1)
                graduate_outcome = round(random.uniform(60, 95), 1)
                perf_rows.append({
                    "record_id": perf_id,
                    "institution_id": inst["institution_id"],
                    "year": year,
                    "rating": rating_label,
                    "overall_score": score,
                    "student_satisfaction_pct": student_satisfaction,
                    "graduate_outcome_pct": graduate_outcome,
                    "attendance_rate_pct": "",  # not applicable
                })
            elif cat == "College":
                rating_label = rating  # use Ofsted-style for colleges
                perf_rows.append({
                    "record_id": perf_id,
                    "institution_id": inst["institution_id"],
                    "year": year,
                    "rating": rating_label,
                    "overall_score": score,
                    "student_satisfaction_pct": round(random.uniform(65, 92), 1),
                    "graduate_outcome_pct": round(random.uniform(55, 90), 1),
                    "attendance_rate_pct": round(random.uniform(80, 98), 1),
                })
            else:
                # Primary / Secondary – Ofsted rating + attendance
                perf_rows.append({
                    "record_id": perf_id,
                    "institution_id": inst["institution_id"],
                    "year": year,
                    "rating": rating,
                    "overall_score": score,
                    "student_satisfaction_pct": "",
                    "graduate_outcome_pct": "",
                    "attendance_rate_pct": round(random.uniform(85, 99), 1),
                })
            perf_id += 1

    # ---------------------------------------------------------------------
    # Write CSV files
    # ---------------------------------------------------------------------
    with open(os.path.join(out_dir, "regions.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["region_id", "name", "country"])
        w.writeheader()
        w.writerows(regions_rows)

    with open(os.path.join(out_dir, "institutions.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "institution_id", "name", "category", "region_id", "region_name",
            "city", "postcode", "founded_year", "website",
        ])
        w.writeheader()
        w.writerows(institutions)

    with open(os.path.join(out_dir, "performance_records.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "record_id", "institution_id", "year", "rating", "overall_score",
            "student_satisfaction_pct", "graduate_outcome_pct", "attendance_rate_pct",
        ])
        w.writeheader()
        w.writerows(perf_rows)

    # Summary
    by_cat = {}
    for inst in institutions:
        by_cat[inst["category"]] = by_cat.get(inst["category"], 0) + 1
    by_region = {}
    for inst in institutions:
        by_region[inst["region_name"]] = by_region.get(inst["region_name"], 0) + 1

    print("=" * 60)
    print(f"Regions:              {len(regions_rows)}")
    print(f"Institutions total:   {len(institutions)}")
    for c, n in sorted(by_cat.items()):
        print(f"  - {c}: {n}")
    print(f"Performance records:  {len(perf_rows)}")
    print("Institutions by region:")
    for r, n in sorted(by_region.items(), key=lambda x: -x[1]):
        print(f"  - {r}: {n}")
    print("=" * 60)


if __name__ == "__main__":
    build()
