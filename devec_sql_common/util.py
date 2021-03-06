#!/usr/bin/env python3

import sys


def mysql_quote(x):
    '''
    Quote the string x using MySQL quoting rules. If x is the empty string,
    return "NULL". Probably not safe against maliciously formed strings, but
    whatever; our input is fixed and from a basically trustable source..
    '''
    if not x:
        return "NULL"
    x = x.replace("\\", "\\\\")
    x = x.replace("'", "''")
    x = x.replace("\n", "\\n")
    return "'{}'".format(x)


def mysql_number(x, typeconv=lambda x: x, factor=1, replace=",%"):
    if not x:
        return "NULL"
    x = x.strip()
    for char in replace:
        x = x.replace(char, "")
    if factor != 1:
        return str(typeconv(x) * factor)
    else:
        return str(typeconv(x))


def mysql_int(x, factor=1, replace=",%"):
    return mysql_number(x, typeconv=int, factor=factor, replace=replace)


def mysql_float(x, factor=1, replace=",%"):
    return mysql_number(x, typeconv=float, factor=factor, replace=replace)


def mysql_string_date(x):
    """
    Return x as a string of the form "YYYYMMDD". This allows for representing a
    wider range of dates than is supported in MySQL's date type ('1000-01-01'
    to '9999-12-31'). Just the year can be stored as "YYYY0000", and just the
    year and month can be stored as "YYYYMM00". The input x should be an
    integer representing the year or a string of the form "YYYY", "YYYY-MM", or
    "YYYY-MM-DD".
    """
    x = str(x)
    if "-" not in x:
        assert len(x) <= 4, x
        return mysql_quote(("0" * (4 - len(x))) + x + "0000")
    if len(x) == len("YYYY-MM"):
        lst = x.split("-")
        return mysql_quote(lst[0] + lst[1] + "00")
    if len(x) == len("YYYY-MM-DD"):
        return mysql_quote("".join(x.split("-")))

REGION_MAP_ = {
        "(Centre-   North)           Italy": "Center-North Italy",
        "12 W. Europe": "",
        "14 small WEC": "",
        "15 L. America": "",
        "15 W. Asia": "",
        "16 E. Asia": "",
        "21 Caribbean": "",
        "24 Sm. E. Asia": "",
        "3 Small Afr.": "",
        "30 E. Asia": "",
        "30 W. Europe": "",
        "7 E. Europe": "",
        "8 L. America": "",
        "Advanced Countries": "",
        "Afghanistan": "Afghanistan",
        "Africa": "",
        "Albania": "Albania",
        "Algeria": "Algeria",
        "American Samoa": "American Samoa",
        "Andorra": "Andorra",
        "Angola": "Angola",
        "Anguilla": "Anguilla",
        "Antigua": "Antigua",
        "Antigua & Barbuda": "Antigua and Barbuda",
        "Antigua and Barbuda": "Antigua and Barbuda",
        "Arab World": "",
        "Argentina": "Argentina",
        "Armenia": "Armenia",
        "Aruba": "Aruba",
        "Asia": "",
        "Australia": "Australia",
        "Austria": "Austria",
        "Azerbaijan": "Azerbaijan",
        "Bahamas": "The Bahamas",
        "Bahamas, The": "The Bahamas",
        "Bahrain": "Bahrain",
        "Bangladesh": "Bangladesh",
        "Barbados": "Barbados",
        "Belarus": "Belarus",
        "Belgium": "Belgium",
        "Belize": "Belize",
        "Benin": "Benin",
        "Bermuda": "Bermuda",
        "Bhutan": "Bhutan",
        "Bolivia": "Bolivia",
        "Bolivia (Plurinational State of)": "Bolivia",
        "Bolivia, Plurinational State of": "Bolivia",
        "Bosnia": "Bosnia and Herzegovina",
        "Bosnia & Herzegovina": "Bosnia and Herzegovina",
        "Bosnia and Herzegovina": "Bosnia and Herzegovina",
        "Botswana": "Botswana",
        "Brazil": "Brazil",
        "British Virgin Islands": "British Virgin Islands",
        "Brunei": "Brunei Darussalam",
        "Brunei Darussalam": "Brunei Darussalam",
        "Bulgaria": "Bulgaria",
        "Burkina Faso": "Burkina Faso",
        "Burma": "Myanmar",
        "Burundi": "Burundi",
        "Byzantium/  Ottoman Empire/ Turkey": "",
        "Cabo Verde": "Cape Verde",
        "Cambodia": "Cambodia",
        "Cameroon": "Cameroon",
        "Canada": "Canada",
        "Cape Colony/ South Africa": "",
        "Cape Verde": "Cape Verde",
        "CAPE VERDE IS.": "Cape Verde",
        "Caribbean small states": "",
        "Cayman Islands": "Cayman Islands",
        "Centr. Afr. Rep.": "Central African Republic",
        "Central & Eastern Europe": "",
        "CENTRAL AFR.R.": "Central African Republic",
        "Central African Republic": "Central African Republic",
        "Central Europe and the Baltics": "",
        "Chad": "Chad",
        "Channel Islands": "",
        "Chile": "Chile",
        "China": "China",
        "China - old": "China (old)",
        "China (Alternative)": "China (alternative)",
        "China (Official)": "China",
        "China Version 1": "China",
        "China Version 2": "China (version 2)",
        "China, Hong Kong SAR": "Hong Kong",
        "China, Macao SAR": "Macau",
        "China, People's Republic of": "China",
        "China: Hong Kong SAR": "Hong Kong",
        "China: Macao SAR": "Macau",
        "Colombia": "Colombia",
        "Comoro Islands": "Comoro Islands",
        "Comoros": "Comoros",
        "CONGO": "Republic of the Congo",
        "Congo 'Brazzaville'": "Republic of the Congo",
        "Congo-Kinshasa": "Democratic Republic of the Congo",
        "Congo, Dem. Rep.": "Democratic Republic of the Congo",
        "Congo, Rep.": "Republic of the Congo",
        "Congo, Republic of": "Republic of the Congo",
        "Cook Islands": "Cook Islands",
        "Costa Rica": "Costa Rica",
        "Cote d`Ivoire": "Ivory Coast",
        "Cote d'Ivoire": "Ivory Coast",
        "Côte d'Ivoire": "Ivory Coast",
        "Croatia": "Croatia",
        "Cuba": "Cuba",
        "Curacao": "Curaçao",
        "Cyprus": "Cyprus",
        "Czech Rep.": "Czech Republic",
        "Czech Republic": "Czech Republic",
        "Czechia": "Czech Republic",
        "Czecho-slovakia": "Czechoslovakia",
        "Czechoslovakia": "Czechoslovakia",
        "D.R. of the Congo": "Democratic Republic of the Congo",
        "Democratic Republic of the Congo": "Democratic Republic of the Congo",
        "Denmark": "Denmark",
        "Djibouti": "Djibouti",
        "Dominica": "Dominica",
        "Dominican Rep.": "Dominican Republic",
        "Dominican Republic": "Dominican Republic",
        "DR Congo": "Democratic Republic of the Congo",
        "Early-demographic dividend": "",
        "East Asia & Pacific": "",
        "East Asia & Pacific (excluding high income)": "",
        "East Asia & Pacific (IDA & IBRD countries)": "",
        "East Germany": "East Germany",
        "East Timor (included in Indonesia until 1999)": "",
        "Ecuador": "Ecuador",
        "Egypt": "Egypt",
        "Egypt, Arab Rep.": "Egypt",
        "El Salvador": "El Salvador",
        "Emerging Market and Developing Countries": "",
        "Emerging Markets and Developing Economies": "",
        "England/GB/UK": "United Kingdom",
        "Equatorial Guinea": "Equatorial Guinea",
        "Eritrea": "Eritrea",
        "Eritrea & Ethiopia": "Eritrea and Ethiopia",
        "Eritrea and Ethiopia": "Eritrea and Ethiopia",
        "Estonia": "Estonia",
        "Ethiopia": "Ethiopia",
        "EU-12": "",
        "EU-13": "",
        "EU-15": "",
        "EU-27": "",
        "EU-28": "",
        "Euro area": "",
        "Europe": "",
        "Europe & Central Asia": "",
        "Europe & Central Asia (excluding high income)": "",
        "Europe & Central Asia (IDA & IBRD countries)": "",
        "European Union": "",
        "F. Czecho-slovakia": "Former Czechoslovakia",
        "F. USSR": "Former Soviet Union",
        "F. Yugoslavia": "Former Yugoslavia",
        "Faeroe Islands": "Faroe Islands",
        "Faroe Islands": "Faroe Islands",
        "Fiji": "Fiji",
        "Finland": "Finland",
        "Former Czechoslovakia": "Former Czechoslovakia",
        "Former Yugoslavia": "Former Yugoslavia",
        "Fragile and conflict affected situations": "",
        "France": "France",
        "French Polynesia": "French Polynesia",
        "Gabon": "Gabon",
        "Gambia": "The Gambia",
        "Gambia, The": "The Gambia",
        "Georgia": "Georgia",
        "Germany": "Germany",
        "GERMANY, EAST": "East Germany",
        "GERMANY, WEST": "West Germany",
        "Ghana": "Ghana",
        "Gibraltar": "Gibraltar",
        "Greece": "Greece",
        "Greenland": "Greenland",
        "Grenada": "Grenada",
        "Guadeloupe": "Guadeloupe",
        "Guam": "Guam",
        "Guatemala": "Guatemala",
        "Guernsey": "Guernsey",
        "Guinea": "Guinea",
        "Guinea Bissau": "Guinea-Bissau",
        "GUINEA-BISS": "Guinea-Bissau",
        "Guinea-Bissau": "Guinea-Bissau",
        "Guyana": "Guyana",
        "Guyana (Fr.)": "French Guiana",
        "Haïti": "Haiti",
        "Heavily indebted poor countries (HIPC)": "",
        "High income": "",
        "Holland/     Netherlands": "",
        "Honduras": "Honduras",
        "Hong Kong": "Hong Kong",
        "Hong Kong SAR, China": "Hong Kong",
        "Hungary": "Hungary",
        "IBRD only": "",
        "Iceland": "Iceland",
        "IDA & IBRD total": "",
        "IDA blend": "",
        "IDA only": "",
        "IDA total": "",
        "India": "India",
        "Indonesia": "Indonesia",
        "Indonesia (including Timor until 1999)": "",
        "Indonesia (Java before 1880)": "",
        "Iran": "Iran",
        "Iran (Islamic Republic of)": "Iran",
        "Iran, Islamic Rep.": "Iran",
        "Iran, Islamic Republic of": "Iran",
        "Iraq": "Iraq",
        "Ireland": "Ireland",
        "Isle of Man": "Isle of Man",
        "Israel": "Israel",
        "Italy": "Italy",
        "IVORY COAST": "Ivory Coast",
        "Jamaica": "Jamaica",
        "Japan": "Japan",
        "Jersey": "Jersey",
        "Jordan": "Jordan",
        "Kazakhstan": "Kazakhstan",
        "Kenya": "Kenya",
        "Kiribati": "Kiribati",
        "Korea, Dem. People’s Rep.": "North Korea",
        "Korea, Dem. Rep.": "North Korea",
        "Korea, Rep.": "South Korea",
        "Korea, Republic of": "South Korea",
        "Kosovo": "Kosovo",
        "Kuwait": "Kuwait",
        "Kyrgyz Republic": "Kyrgyzstan",
        "Kyrgyzstan": "Kyrgyzstan",
        "L. America": "Latin America",
        "Lao PDR": "Laos",
        "Lao People's Democratic Republic": "Laos",
        "Lao People's DR": "Laos",
        "Laos": "Laos",
        "Late-demographic dividend": "",
        "Latin America": "",
        "Latin America & Caribbean": "",
        "Latin America & Caribbean (excluding high income)": "",
        "Latin America & the Caribbean (IDA & IBRD countries)": "",
        "Latvia": "Latvia",
        "Least developed countries: UN classification": "",
        "Lebanon": "Lebanon",
        "Lesotho": "Lesotho",
        "Liberia": "Liberia",
        "Libya": "Libya",
        "Liechtenstein": "Liechtenstein",
        "Lithuania": "Lithuania",
        "Low & middle income": "",
        "Low income": "",
        "Lower middle income": "",
        "Luxembourg": "Luxembourg",
        "Macao": "Macau",
        "Macao SAR, China": "Macau",
        "Macedonia": "Macedonia",
        "Macedonia, FYR": "Macedonia",
        "Macedonia, Republic of": "Macedonia",
        "Madagascar": "Madagascar",
        "Malawi": "Malawi",
        "Malaysia": "Malaysia",
        "Maldives": "Maldives",
        "Mali": "Mali",
        "Malta": "Malta",
        "Marshall Islands": "Marshall Islands",
        "Martinique": "Martinique",
        "Mature Economies": "",
        "Mauritania": "Mauritania",
        "Mauritius": "Mauritius",
        "Mayotte": "Mayotte",
        "Mexico": "Mexico",
        "Micronesia": "Micronesia",
        "Micronesia, Fed. Sts.": "Federated States of Micronesia",
        "Micronesia, Federated States of": "Federated States of Micronesia",
        "Middle East": "",
        "Middle East & North Africa": "",
        "Middle East & North Africa (excluding high income)": "",
        "Middle East & North Africa (IDA & IBRD countries)": "",
        "Middle income": "",
        "Moldova": "Moldova",
        "Moldova, Republic of": "Moldova",
        "Monaco": "Monaco",
        "Mongolia": "Mongolia",
        "Montenegro": "Montenegro",
        "Montserrat": "Montserrat",
        "Morocco": "Morocco",
        "Mozambique": "Mozambique",
        "Myanmar": "Myanmar",
        "N. Zealand": "New Zealand",
        "Namibia": "Namibia",
        "Nauru": "Nauru",
        "Nepal": "Nepal",
        "Neth. Antilles": "Netherlands Antilles",
        "Netherlands": "Netherlands",
        "Netherlands Antilles": "Netherlands Antilles",
        "New Caledonia": "New Caledonia",
        "New Zealand": "New Zealand",
        "Nicaragua": "Nicaragua",
        "Niger": "Niger",
        "Nigeria": "Nigeria",
        "North America": "",
        "North Korea": "North Korea",
        "Northern Mariana Islands": "Northern Mariana Islands",
        "Norway": "Norway",
        "OECD": "OECD",
        "OECD members": "OECD",
        "of which: Brazil": "",
        "of which: Euro Area": "",
        "of which: Mexico": "",
        "Oman": "Oman",
        "Other Advanced": "",
        "Other developing Asia": "",
        "Other Mature": "",
        "Other Mature Economies": "",
        "Other small states": "",
        "Pacific island small states": "",
        "Pakistan": "Pakistan",
        "Palau": "Palau",
        "Panama": "Panama",
        "PAPUA N.GUINEA": "Papua New Guinea",
        "Papua New Guinea": "Papua New Guinea",
        "Paraguay": "Paraguay",
        "Peru": "Peru",
        "Philippines": "Philippines",
        "Poland": "Poland",
        "Portugal": "Portugal",
        "Post-demographic dividend": "",
        "Pre-demographic dividend": "",
        "Puerto Rico": "Puerto Rico",
        "Qatar": "Qatar",
        "Republic of Korea": "South Korea",
        "Republic of Moldova": "Moldova",
        "Reunion": "Réunion",
        "Romania": "Romania",
        "Russia": "Russia",
        "Russia and other CIS": "",
        "Russia, Central Asia and Southeast Europe": "Russia, Central Asia, and Southeast Europe",
        "Russia, Central Asia, and Southeast Europe": "Russia, Central Asia, and Southeast Europe",
        "Russian Federation": "Russia",
        "Rwanda": "Rwanda",
        "S. Korea": "South Korea",
        "Saint Helena": "Saint Helena",
        "Saint Kitts and Nevis": "Saint Kitts And Nevis",
        "Saint Lucia": "Saint Lucia",
        "Saint Vincent and the Grenadines": "Saint Vincent And The Grenadines",
        "Samoa": "Samoa",
        "San Marino": "San Marino",
        "Sao Tomé & Principe": "São Tomé and Príncipe",
        "São Tomé and Principe": "São Tomé and Príncipe",
        "Saudi Arabia": "Saudi Arabia",
        "Senegal": "Senegal",
        "Serbia": "Serbia",
        "Serbia & Montenegro": "Serbia and Montenegro",
        "Serbia and Montenegro": "Serbia and Montenegro",
        "Serbia/Montenegro/Kosovo": "",
        "Seychelles": "Seychelles",
        "Sierra Leone": "Sierra Leone",
        "Singapore": "Singapore",
        "Sint Maarten (Dutch part)": "Sint Maarten (Dutch part)",
        "Slovak Republic": "Slovakia",
        "Slovakia": "Slovakia",
        "Slovenia": "Slovenia",
        "Small states": "",
        "SOLOMON IS.": "Solomon Islands",
        "Solomon Islands": "Solomon Islands",
        "Somalia": "Somalia",
        "South Africa": "South Africa",
        "South Asia": "",
        "South Asia (IDA & IBRD)": "",
        "South Korea": "South Korea",
        "South Sudan": "South Sudan",
        "Spain": "Spain",
        "Sri Lanka": "Sri Lanka",
        "St. Kitts & Nevis": "Saint Kitts and Nevis",
        "St. Kitts and Nevis": "Saint Kitts and Nevis",
        "St. Kitts Nevis": "Saint Kitts and Nevis",
        "St. Lucia": "Saint Lucia",
        "St. Martin (French part)": "Saint Martin (French part)",
        "St. Pierre and Miquelon": "Saint Pierre and Miquelon",
        "St. Vincent (and the grenadines)": "Saint Vincent and the Grenadines",
        "St. Vincent and the Grenadines": "Saint Vincent and the Grenadines",
        "ST.KITTS&NEVIS": "Saint Kitts and Nevis",
        "St.Lucia": "Saint Lucia",
        "St.Vincent & Grenadines": "Saint Vincent and the Grenadines",
        "ST.VINCENT&GRE": "Saint Vincent and the Grenadines",
        "State of Palestine": "Palestine",
        "Sub-Saharan Africa": "",
        "Sub-Saharan Africa (excluding high income)": "",
        "Sub-Saharan Africa (IDA & IBRD countries)": "",
        "Sudan": "Sudan",
        "Sudan (Former)": "Former Sudan",
        "Suriname": "Suriname",
        "Swaziland": "Swaziland",
        "Sweden": "Sweden",
        "Switzerland": "Switzerland",
        "Syria": "Syria",
        "Syrian Arab Republic": "Syria",
        "T. & Tobago": "Trinidad and Tobago",
        "Taiwan": "Taiwan",
        "Taiwan, Province of China": "Taiwan",
        "Tajikistan": "Tajikistan",
        "Tanzania": "Tanzania",
        "Tanzania, United Republic of": "Tanzania",
        "TFYR of Macedonia": "Macedonia",
        "Thailand": "Thailand",
        "The Former Yugoslav Republic of Macedonia": "Macedonia",
        "Timor-Leste": "Timor-Leste",
        "Togo": "Togo",
        "Tonga": "Tonga",
        "Total": "",
        "Total 12 Western Europe": "",
        "Total 14 small WEC countries": "",
        "Total 14 small west European countries": "",
        "Total 15 Latin American countries": "",
        "Total 15 West Asian countries": "",
        "Total 16 East Asian countries": "",
        "Total 21 small Caribbean countries": "",
        "Total 24 Small East Asian countries": "",
        "Total 3 Small African countries": "",
        "Total 30  Western Europe": "",
        "Total 30 East Asian countries": "",
        "Total 7 East European Countries": "",
        "Total 8 Latin American countries": "",
        "Total Africa": "",
        "Total Asia": "",
        "Total Eritrea and Ethiopia": "",
        "Total Former USSR": "Former Soviet Union",
        "Total Latin America": "",
        "Total Western Offshoots": "",
        "Total World": "",
        "Trinidad & Tobago": "Trinidad and Tobago",
        "Trinidad &Tobago": "Trinidad and Tobago",
        "Trinidad and Tobago": "Trinidad and Tobago",
        "TRINIDAD&TOBAGO": "Trinidad and Tobago",
        "Tunisia": "Tunisia",
        "Turk-menistan": "Turkmenistan",
        "Turkey": "Turkey",
        "Turkmenistan": "Turkmenistan",
        "Turks and Caicos Islands": "Turks and Caicos Islands",
        "Tuvalu": "Tuvalu",
        "U.K.": "United Kingdom",
        "U.R. of Tanzania: Mainland": "Tanzania (mainland)",
        "U.S.A.": "United States",
        "U.S.S.R.": "Soviet Union",
        "UAE": "United Arab Emirates",
        "Uganda": "Uganda",
        "Ukraine": "Ukraine",
        "UNITED ARAB E.": "United Arab Emirates",
        "United Arab Emirates": "United Arab Emirates",
        "United Kingdom": "United Kingdom",
        "United Republic of Tanzania: Mainland": "Tanzania (mainland)",
        "United States": "United States",
        "Upper middle income": "",
        "Uruguay": "Uruguay",
        "US": "United States",
        "USA": "United States",
        "USSR": "Soviet Union",
        "Uzbekistan": "Uzbekistan",
        "Vanuatu": "Vanuatu",
        "Venezuela": "Venezuela",
        "Venezuela (Bolivarian Republic of)": "Venezuela",
        "Venezuela, Bolivarian Republic of": "Venezuela",
        "Venezuela, RB": "Venezuela",
        "Viet Nam": "Vietnam",
        "Vietnam": "Vietnam",
        "Virgin Islands": "British Virgin Islands",
        "Virgin Islands (U.S.)": "United States Virgin Islands",
        "W. Bank & Gaza": "Palestine",
        "W. Offshoots": "",
        "Wallis and Fortuna": "Wallis and Futuna",
        "West Bank and Gaza": "Palestine",
        "West Germany": "West Germany",
        "Western Sahara": "Western Sahara",
        "WESTERN SAMOA": "Samoa",
        "World": "",
        "World Average": "",
        "World Total": "",
        "Yemen": "Yemen",
        "Yemen, Rep.": "Yemen",
        "Yugoslavia": "",
        "ZAIRE": "Democratic Republic of the Congo",
        "Zaire (Congo Kinshasa)": "Democratic Republic of the Congo",
        "Zambia": "Zambia",
        "Zimbabwe": "Zimbabwe",
    }

REGION_MAP = {}
for k, v in REGION_MAP_.items():
    REGION_MAP[k.lower()] = v

def region_normalized(x, region_map=REGION_MAP):
    """Normalize the region or country name x."""
    k = x.lower()
    if k in region_map and region_map[k]:
        return region_map[k]
    else:
        return x

# Set to keep track of the (region, odate, database_url, metric, units)
# combinations we have seen.
UNIQ_JOIN_SET = set()


def uniq_join(lst=[], delim=",", method="string_concat"):
    """Join lst using delim like delim.join(lst), but ensure the joined items
    are unique across calls for the combination (region, odate, database_url,
    metric, units). In particular, if we call uniq_join with the same lst
    twice, it should fail.

    The parameter method is the method used to store the combination.
    tuple_with_db_url and tuple_without_db_url use tuples to store combinations
    while string_concat uses a string of the concatenated fields. The latter
    can result in some false positives because e.g. both (ab, c) and (a, bc)
    result in the string "abc". In practice this shouldn't be a problem because
    the fields are different enough. The latter can also hold the most amount
    of data in memory."""
    region, odate, database_url, _, metric, units, _, _ = lst

    if method == "tuple_with_db_url":
        # Can hold 4 million of these on 4GB RAM
        tup = (region, odate, database_url, metric, units)
    elif method == "tuple_without_db_url":
        # Can hold about 6.5 million of these on 4GB RAM; we don't really need to
        # check for database_url because each script has a single database_url
        # anyway
        tup = (region, odate, metric, units)
    elif method == "string_concat":
        # This can do 7.6 million required for WDI
        tup = region + odate + metric + units
    else:
        # Don't check for uniqueness
        tup = None

    if tup:
        if tup in UNIQ_JOIN_SET:
            raise ValueError("We have seen this combination before!", tup)
        UNIQ_JOIN_SET.add(tup)
        if len(UNIQ_JOIN_SET) % 100000 == 0:
            print("UNIQ_JOIN_SET size:", len(UNIQ_JOIN_SET), file=sys.stderr)
    return delim.join(lst)


def print_insert_header():
    """Print the insert header to speed up insertions for bulk inserts."""
    print("set autocommit = 0;")


def print_insert_footer():
    """Print the insert footer. Cleans up after print_insert_header."""
    print("commit;")
    print("set autocommit = 1;")
