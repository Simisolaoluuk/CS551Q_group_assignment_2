# script for making the uk institution dataset
# generates regions, institutions and performance records as csv files

import csv
import random
import os

random.seed(42)


# uk regions with main city
# (region name, country, main city)
REGIONS = [
    ("North East England", "England", "Newcastle upon Tyne"),
    ("North West England", "England", "Manchester"),
    ("Yorkshire and the Humber", "England", "Leeds"),
    ("East Midlands", "England", "Nottingham"),
    ("West Midlands", "England", "Birmingham"),
    ("East of England", "England", "Cambridge"),
    ("Greater London", "England", "London"),
    ("South East England", "England", "Oxford"),
    ("South West England", "England", "Bristol"),
    ("Scotland", "Scotland", "Edinburgh"),
    ("Wales", "Wales", "Cardiff"),
    ("Northern Ireland", "Northern Ireland", "Belfast"),
]

# cities for each region
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

# real uk universities (city must match CITY_BY_REGION above)
UNIVERSITIES = [
    ("Imperial College London", "Greater London", "London"),
    ("University College London", "Greater London", "London"),
    ("King's College London", "Greater London", "London"),
    ("London School of Economics", "Greater London", "London"),
    ("Queen Mary University of London", "Greater London", "London"),
    ("City, University of London", "Greater London", "London"),
    ("Goldsmiths, University of London", "Greater London", "Camden"),
    ("SOAS University of London", "Greater London", "London"),
    ("University of Westminster", "Greater London", "Westminster"),
    ("University of East London", "Greater London", "London"),
    ("Middlesex University", "Greater London", "London"),
    ("London South Bank University", "Greater London", "London"),
    ("Kingston University", "Greater London", "Croydon"),
    ("University of Roehampton", "Greater London", "Bromley"),
    ("University of West London", "Greater London", "Ealing"),
    ("University of Greenwich", "Greater London", "Hackney"),

    ("University of Oxford", "South East England", "Oxford"),
    ("Oxford Brookes University", "South East England", "Oxford"),
    ("University of Reading", "South East England", "Reading"),
    ("University of Sussex", "South East England", "Brighton"),
    ("University of Brighton", "South East England", "Brighton"),
    ("University of Southampton", "South East England", "Southampton"),
    ("Solent University", "South East England", "Southampton"),
    ("University of Portsmouth", "South East England", "Portsmouth"),
    ("University of Kent", "South East England", "Canterbury"),
    ("Canterbury Christ Church University", "South East England", "Canterbury"),
    ("University of Buckingham", "South East England", "Milton Keynes"),

    ("University of Cambridge", "East of England", "Cambridge"),
    ("Anglia Ruskin University", "East of England", "Cambridge"),
    ("University of East Anglia", "East of England", "Norwich"),
    ("Norwich University of the Arts", "East of England", "Norwich"),
    ("University of Suffolk", "East of England", "Ipswich"),
    ("University of Essex", "East of England", "Colchester"),
    ("University of Hertfordshire", "East of England", "Luton"),
    ("University of Bedfordshire", "East of England", "Luton"),
    ("Anglia Ruskin Peterborough", "East of England", "Peterborough"),

    ("University of Manchester", "North West England", "Manchester"),
    ("Manchester Metropolitan University", "North West England", "Manchester"),
    ("University of Liverpool", "North West England", "Liverpool"),
    ("Liverpool John Moores University", "North West England", "Liverpool"),
    ("Lancaster University", "North West England", "Lancaster"),
    ("University of Cumbria", "North West England", "Lancaster"),
    ("University of Central Lancashire", "North West England", "Preston"),
    ("Edge Hill University", "North West England", "Blackpool"),
    ("University of Chester", "North West England", "Chester"),
    ("University of Bolton", "North West England", "Bolton"),

    ("University of Leeds", "Yorkshire and the Humber", "Leeds"),
    ("Leeds Beckett University", "Yorkshire and the Humber", "Leeds"),
    ("University of Sheffield", "Yorkshire and the Humber", "Sheffield"),
    ("Sheffield Hallam University", "Yorkshire and the Humber", "Sheffield"),
    ("University of York", "Yorkshire and the Humber", "York"),
    ("York St John University", "Yorkshire and the Humber", "York"),
    ("University of Bradford", "Yorkshire and the Humber", "Bradford"),
    ("University of Hull", "Yorkshire and the Humber", "Hull"),
    ("University of Doncaster", "Yorkshire and the Humber", "Doncaster"),

    ("University of Birmingham", "West Midlands", "Birmingham"),
    ("Birmingham City University", "West Midlands", "Birmingham"),
    ("Aston University", "West Midlands", "Birmingham"),
    ("University of Warwick", "West Midlands", "Coventry"),
    ("Coventry University", "West Midlands", "Coventry"),
    ("University of Wolverhampton", "West Midlands", "Wolverhampton"),
    ("Keele University", "West Midlands", "Stoke-on-Trent"),
    ("Staffordshire University", "West Midlands", "Stoke-on-Trent"),
    ("University of Worcester", "West Midlands", "Worcester"),

    ("University of Nottingham", "East Midlands", "Nottingham"),
    ("Nottingham Trent University", "East Midlands", "Nottingham"),
    ("University of Leicester", "East Midlands", "Leicester"),
    ("De Montfort University", "East Midlands", "Leicester"),
    ("University of Derby", "East Midlands", "Derby"),
    ("University of Lincoln", "East Midlands", "Lincoln"),
    ("University of Northampton", "East Midlands", "Northampton"),

    ("University of Bristol", "South West England", "Bristol"),
    ("University of the West of England", "South West England", "Bristol"),
    ("University of Bath", "South West England", "Bath"),
    ("Bath Spa University", "South West England", "Bath"),
    ("University of Exeter", "South West England", "Exeter"),
    ("University of Plymouth", "South West England", "Plymouth"),
    ("Bournemouth University", "South West England", "Bournemouth"),
    ("Arts University Bournemouth", "South West England", "Bournemouth"),
    ("University of Gloucestershire", "South West England", "Gloucester"),

    ("Newcastle University", "North East England", "Newcastle upon Tyne"),
    ("Northumbria University", "North East England", "Newcastle upon Tyne"),
    ("University of Sunderland", "North East England", "Sunderland"),
    ("Durham University", "North East England", "Durham"),
    ("Teesside University", "North East England", "Middlesbrough"),
    ("Gateshead College HE", "North East England", "Gateshead"),

    ("University of Edinburgh", "Scotland", "Edinburgh"),
    ("Heriot-Watt University", "Scotland", "Edinburgh"),
    ("Edinburgh Napier University", "Scotland", "Edinburgh"),
    ("University of Glasgow", "Scotland", "Glasgow"),
    ("University of Strathclyde", "Scotland", "Glasgow"),
    ("Glasgow Caledonian University", "Scotland", "Glasgow"),
    ("University of Aberdeen", "Scotland", "Aberdeen"),
    ("Robert Gordon University", "Scotland", "Aberdeen"),
    ("University of Dundee", "Scotland", "Dundee"),
    ("Abertay University", "Scotland", "Dundee"),
    ("University of Stirling", "Scotland", "Stirling"),
    ("University of the Highlands and Islands", "Scotland", "Inverness"),

    ("Cardiff University", "Wales", "Cardiff"),
    ("Cardiff Metropolitan University", "Wales", "Cardiff"),
    ("Swansea University", "Wales", "Swansea"),
    ("University of Wales Trinity Saint David", "Wales", "Swansea"),
    ("University of South Wales", "Wales", "Newport"),
    ("Bangor University", "Wales", "Bangor"),
    ("Wrexham University", "Wales", "Wrexham"),
    ("Aberystwyth University", "Wales", "Aberystwyth"),

    ("Queen's University Belfast", "Northern Ireland", "Belfast"),
    ("Ulster University", "Northern Ireland", "Belfast"),
    ("Stranmillis University College", "Northern Ireland", "Belfast"),
    ("Open University in Ireland", "Northern Ireland", "Londonderry"),
    ("Lisburn Institute HE", "Northern Ireland", "Lisburn"),
    ("Newry Institute HE", "Northern Ireland", "Newry"),
    ("Armagh Theological College", "Northern Ireland", "Armagh"),
]

# real uk colleges
COLLEGES = [
    ("City of Bristol College", "South West England", "Bristol"),
    ("Bath College", "South West England", "Bath"),
    ("Exeter College", "South West England", "Exeter"),
    ("Plymouth College of Art", "South West England", "Plymouth"),
    ("South Devon College", "South West England", "Plymouth"),
    ("Gloucestershire College", "South West England", "Gloucester"),
    ("Bournemouth and Poole College", "South West England", "Bournemouth"),

    ("Manchester College", "North West England", "Manchester"),
    ("Liverpool City College", "North West England", "Liverpool"),
    ("Preston College", "North West England", "Preston"),
    ("Blackpool and The Fylde College", "North West England", "Blackpool"),
    ("Bolton College", "North West England", "Bolton"),
    ("Salford City College", "North West England", "Manchester"),
    ("Lancaster and Morecambe College", "North West England", "Lancaster"),
    ("Cheshire College South and West", "North West England", "Chester"),

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
    ("Heart of Worcestershire College", "West Midlands", "Worcester"),

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
    ("Luton Sixth Form College", "East of England", "Luton"),

    ("City and Islington College", "Greater London", "London"),
    ("Westminster Kingsway College", "Greater London", "Westminster"),
    ("Ealing, Hammersmith and West London College", "Greater London", "Ealing"),
    ("Croydon College", "Greater London", "Croydon"),
    ("Hackney Community College", "Greater London", "Hackney"),
    ("Newham College", "Greater London", "London"),
    ("Lambeth College", "Greater London", "London"),
    ("Bromley College", "Greater London", "Bromley"),
    ("Camden College", "Greater London", "Camden"),

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

    ("Cardiff and Vale College", "Wales", "Cardiff"),
    ("Gower College Swansea", "Wales", "Swansea"),
    ("Coleg Gwent", "Wales", "Newport"),
    ("Coleg Cambria", "Wales", "Wrexham"),
    ("Coleg Ceredigion", "Wales", "Aberystwyth"),
    ("Bangor College", "Wales", "Bangor"),

    ("Belfast Metropolitan College", "Northern Ireland", "Belfast"),
    ("Northern Regional College", "Northern Ireland", "Lisburn"),
    ("South Eastern Regional College", "Northern Ireland", "Newry"),
    ("South West College", "Northern Ireland", "Armagh"),
    ("North West Regional College", "Northern Ireland", "Londonderry"),
]

# words for making up school names
PRIMARY_PREFIXES = [
    "St Mary's", "St John's", "St Peter's", "St Paul's", "St Thomas'",
    "St Andrew's", "St George's", "Holy Trinity", "All Saints", "Sacred Heart",
    "Greenfield", "Oakwood", "Riverside", "Hillside", "Meadow", "Westfield",
    "Eastfield", "Northfield", "Southfield", "Brookfield", "Park", "Highfield",
    "Hawthorn", "Beech", "Elm", "Cedar", "Willow", "Birch", "Maple",
    "Victoria", "Albert", "Queen Elizabeth", "King Edward",
    "Town End", "The Grove", "The Manor", "The Avenue",
    "Ashwood", "Beechwood", "Pinewood", "Forestdale",
    "Garden", "Lakeside", "Sunnyfield", "Greenview", "Fairfield",
    "Mount Pleasant", "Bridgewater", "Ridgeway", "Hilltop", "Valley",
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
    "The Royal", "Stanton", "Wakefield", "Bromfield", "Ashford",
    "Hartfield", "Lakemoor", "Whitestone", "Greystone", "Northwood",
]

SECONDARY_SUFFIXES = [
    "Academy",
    "High School",
    "Secondary School",
    "Grammar School",
    "Comprehensive School",
    "School",
    "College",
    "Sixth Form",
]

# ofsted ratings
OFSTED = ["Outstanding", "Good", "Requires Improvement", "Inadequate"]
OFSTED_WEIGHTS = [0.20, 0.65, 0.12, 0.03]

# default image url by category (free unsplash images)
CATEGORY_IMAGES = {
    "University": "https://images.unsplash.com/photo-1562774053-701939374585?w=800",
    "College": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
    "Secondary School": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?w=800",
    "Primary School": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800",
}


def make_school_name(level, used_names):
    # pick a random name and check it's not already used
    if level == "Primary":
        prefixes = PRIMARY_PREFIXES
        suffixes = PRIMARY_SUFFIXES
    else:
        prefixes = SECONDARY_PREFIXES
        suffixes = SECONDARY_SUFFIXES

    for i in range(50):
        name = random.choice(prefixes) + " " + random.choice(suffixes)
        if name not in used_names:
            used_names.add(name)
            return name

    # add a number if all combos are used
    n = 1
    while True:
        name = random.choice(prefixes) + " " + random.choice(suffixes) + " " + str(n)
        if name not in used_names:
            used_names.add(name)
            return name
        n += 1


def make_postcode(city):
    # uk postcode prefix by city
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
    letters = "ABDEFGHJLNPQRSTUWXYZ"
    return p + str(random.randint(1, 99)) + " " + str(random.randint(1, 9)) + random.choice(letters) + random.choice(letters)


def get_rating():
    return random.choices(OFSTED, weights=OFSTED_WEIGHTS, k=1)[0]


def get_score(rating):
    if rating == "Outstanding":
        return random.randint(85, 100)
    if rating == "Good":
        return random.randint(65, 84)
    if rating == "Requires Improvement":
        return random.randint(45, 64)
    return random.randint(20, 44)


def make_institution_dict(inst_id, name, category, region, city, region_id_map, founded_year, website=""):
    return {
        "institution_id": inst_id,
        "name": name,
        "category": category,
        "region_id": region_id_map[region],
        "region_name": region,
        "city": city,
        "postcode": make_postcode(city),
        "founded_year": founded_year,
        "website": website,
        "image_url": CATEGORY_IMAGES.get(category, ""),
    }


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))

    # build regions with main_city
    regions_rows = []
    region_id_map = {}
    rid = 1
    for name, country, main_city in REGIONS:
        region_id_map[name] = rid
        regions_rows.append({
            "region_id": rid,
            "name": name,
            "country": country,
            "main_city": main_city,
        })
        rid += 1

    # build institutions
    institutions = []
    used_names = set()
    inst_id = 1

    # add universities
    for uni_name, region, city in UNIVERSITIES:
        clean = uni_name.lower().replace(" ", "").replace(",", "").replace("'", "")
        founded = random.randint(1100, 2010) if "Oxford" in uni_name or "Cambridge" in uni_name else random.randint(1820, 2010)
        institutions.append(make_institution_dict(
            inst_id, uni_name, "University", region, city, region_id_map,
            founded, "https://www." + clean[:25] + ".ac.uk"
        ))
        used_names.add(uni_name)
        inst_id += 1

    # add colleges
    for col_name, region, city in COLLEGES:
        clean = col_name.lower().replace(" ", "").replace(",", "").replace("'", "")
        institutions.append(make_institution_dict(
            inst_id, col_name, "College", region, city, region_id_map,
            random.randint(1900, 2015), "https://www." + clean[:25] + ".ac.uk"
        ))
        used_names.add(col_name)
        inst_id += 1

    # umama wants every city to have at least 1 of each category
    # so first pass: make sure each city has at least 1 primary and 1 secondary
    # (universities and colleges - we already filled most cities above)
    all_cities = []
    for region, cities in CITY_BY_REGION.items():
        for city in cities:
            all_cities.append((region, city))

    # add at least 1 primary and 1 secondary per city
    for region, city in all_cities:
        # 1 primary
        name = make_school_name("Primary", used_names)
        institutions.append(make_institution_dict(
            inst_id, name, "Primary School", region, city, region_id_map,
            random.randint(1880, 2020)
        ))
        inst_id += 1
        # 1 secondary
        name = make_school_name("Secondary", used_names)
        institutions.append(make_institution_dict(
            inst_id, name, "Secondary School", region, city, region_id_map,
            random.randint(1850, 2015)
        ))
        inst_id += 1

    # also make sure every city has at least one university and one college
    # check which cities are missing
    cities_with_uni = set()
    cities_with_college = set()
    for inst in institutions:
        if inst["category"] == "University":
            cities_with_uni.add(inst["city"])
        if inst["category"] == "College":
            cities_with_college.add(inst["city"])

    # add a generic university/college for any city missing one
    for region, city in all_cities:
        if city not in cities_with_uni:
            uni_name = city + " University"
            if uni_name in used_names:
                uni_name = "University of " + city
            used_names.add(uni_name)
            clean = uni_name.lower().replace(" ", "").replace(",", "").replace("'", "")
            institutions.append(make_institution_dict(
                inst_id, uni_name, "University", region, city, region_id_map,
                random.randint(1900, 2010), "https://www." + clean[:25] + ".ac.uk"
            ))
            inst_id += 1
        if city not in cities_with_college:
            col_name = city + " Community College"
            if col_name in used_names:
                col_name = city + " College of FE"
            used_names.add(col_name)
            clean = col_name.lower().replace(" ", "").replace(",", "").replace("'", "")
            institutions.append(make_institution_dict(
                inst_id, col_name, "College", region, city, region_id_map,
                random.randint(1950, 2015), "https://www." + clean[:25] + ".ac.uk"
            ))
            inst_id += 1

    # weights for spreading the rest of schools across regions (roughly by population)
    region_weights = {
        "Greater London": 18, "South East England": 15, "North West England": 12,
        "West Midlands": 9, "East of England": 9, "Yorkshire and the Humber": 9,
        "South West England": 8, "East Midlands": 7, "Scotland": 8,
        "Wales": 5, "North East England": 4, "Northern Ireland": 3,
    }

    # add more primary schools to reach a good total
    PRIMARY_EXTRA = 1200
    for i in range(PRIMARY_EXTRA):
        region = random.choices(list(region_weights.keys()), weights=list(region_weights.values()), k=1)[0]
        city = random.choice(CITY_BY_REGION[region])
        name = make_school_name("Primary", used_names)
        institutions.append(make_institution_dict(
            inst_id, name, "Primary School", region, city, region_id_map,
            random.randint(1880, 2020)
        ))
        inst_id += 1

    # add more secondary schools
    SECONDARY_EXTRA = 530
    for i in range(SECONDARY_EXTRA):
        region = random.choices(list(region_weights.keys()), weights=list(region_weights.values()), k=1)[0]
        city = random.choice(CITY_BY_REGION[region])
        name = make_school_name("Secondary", used_names)
        institutions.append(make_institution_dict(
            inst_id, name, "Secondary School", region, city, region_id_map,
            random.randint(1850, 2015)
        ))
        inst_id += 1

    # build performance records (3 years per institution)
    perf_rows = []
    perf_id = 1
    for inst in institutions:
        cat = inst["category"]
        for year in [2022, 2023, 2024]:
            rating = get_rating()
            score = get_score(rating)

            if cat == "University":
                if score >= 85:
                    rating_label = "Gold"
                elif score >= 65:
                    rating_label = "Silver"
                else:
                    rating_label = "Bronze"
                perf_rows.append({
                    "record_id": perf_id,
                    "institution_id": inst["institution_id"],
                    "year": year,
                    "rating": rating_label,
                    "overall_score": score,
                    "student_satisfaction_pct": round(random.uniform(70, 95), 1),
                    "graduate_outcome_pct": round(random.uniform(60, 95), 1),
                    "attendance_rate_pct": "",
                })
            elif cat == "College":
                perf_rows.append({
                    "record_id": perf_id,
                    "institution_id": inst["institution_id"],
                    "year": year,
                    "rating": rating,
                    "overall_score": score,
                    "student_satisfaction_pct": round(random.uniform(65, 92), 1),
                    "graduate_outcome_pct": round(random.uniform(55, 90), 1),
                    "attendance_rate_pct": round(random.uniform(80, 98), 1),
                })
            else:
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

    # write csv files
    with open(os.path.join(out_dir, "regions.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["region_id", "name", "country", "main_city"])
        w.writeheader()
        w.writerows(regions_rows)

    with open(os.path.join(out_dir, "institutions.csv"), "w", newline="", encoding="utf-8") as f:
        cols = ["institution_id", "name", "category", "region_id", "region_name", "city", "postcode", "founded_year", "website", "image_url"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(institutions)

    with open(os.path.join(out_dir, "performance_records.csv"), "w", newline="", encoding="utf-8") as f:
        cols = ["record_id", "institution_id", "year", "rating", "overall_score",
                "student_satisfaction_pct", "graduate_outcome_pct", "attendance_rate_pct"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(perf_rows)

    # print summary
    print("regions:", len(regions_rows))
    print("institutions:", len(institutions))
    print("performance records:", len(perf_rows))

    by_cat = {}
    for inst in institutions:
        c = inst["category"]
        by_cat[c] = by_cat.get(c, 0) + 1
    for c in by_cat:
        print(" ", c, ":", by_cat[c])

    # check every city has all 4 types
    print("\nchecking each city has all 4 categories...")
    city_cats = {}
    for inst in institutions:
        c = inst["city"]
        if c not in city_cats:
            city_cats[c] = set()
        city_cats[c].add(inst["category"])

    needed = {"University", "College", "Primary School", "Secondary School"}
    missing_count = 0
    for city, cats in city_cats.items():
        miss = needed - cats
        if miss:
            print(" ", city, "missing:", miss)
            missing_count += 1
    if missing_count == 0:
        print("  all cities have all 4 categories!")


main()
