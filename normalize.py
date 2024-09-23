# %%
"""
This script performs data cleaning, converts specific fields to numeric types, 
and finds geographic coordinates for specific locations. The main steps include:

1. **Data Loading**: Reads in data from CSV files for household lists and geographic information.
2. **Data Cleaning**: Drops unnecessary columns, converts date fields, and fills in missing values.
3. **Data Transformation**: Cleans up the 'Umsiedlungsnummer' field and converts household size and owner count to integers, replacing invalid values with NaN.
4. **Geolocation Matching**: Uses similarity matching to associate origin and settlement data with geographic coordinates.
5. **Output**: Saves the cleaned and enriched DataFrame to a new CSV file.
"""

from difflib import get_close_matches
import pandas as pd
from shapely import wkt
from datetime import timedelta


def find_most_similar_term_from_df(in_term, df, target_col, sep=";"):
    if pd.isna(in_term):
        return pd.DataFrame()
    term_indices_dict = {}
    for index, terms in enumerate(df[target_col]):
        if sep not in terms:
            continue
        for term in terms.split(sep):
            term_indices_dict[term] = index

    matched_term = get_close_matches(in_term, term_indices_dict.keys(), n=1)
    return (
        df.iloc[term_indices_dict[matched_term[0]]] if matched_term else pd.DataFrame()
    )


hoflisten = pd.read_csv("hofzuweisungslisten.csv")
camps = pd.read_csv("Gazetteer/gazetteer_camps.csv")
origin_districts = pd.read_csv("Gazetteer/gazetteer_vomi_emigration_areas_ga-wo-b.csv")
target_districts = pd.read_csv("Gazetteer/gazetteer_target_districts.csv")
target_setttlements = pd.read_csv("Gazetteer/gazetteer_target_settlements.csv")

hoflisten = hoflisten.drop(columns=["image_filename"])

hoflisten["Datum_Liste"] = pd.to_datetime(hoflisten["Datum_Liste"], errors="coerce")
hoflisten["Datum_Ansiedlung"] = pd.to_datetime(
    hoflisten["Datum_Ansiedlung"], errors="coerce"
)
hoflisten["Datum_Ansiedlung"] = hoflisten["Datum_Ansiedlung"].fillna(
    hoflisten["Datum_Liste"] + timedelta(days=5)
)

hoflisten["Ansiedlungsdorf_geometry"] = pd.NA
hoflisten["Gemeinde_geometry"] = pd.NA
hoflisten["Kreis_geometry"] = pd.NA
hoflisten["Heimatort_geometry"] = pd.NA
hoflisten["Lager_lt_Vomi_geometry"] = pd.NA
hoflisten["Lager_lt_AK-K_geometry"] = pd.NA
hoflisten["Umsiedlungsnummer_geometry"] = pd.NA

missing_data_indices = []
for i, row in hoflisten.iterrows():
    umsdlnr = row["Umsiedlungsnummer"]
    if pd.isna(umsdlnr):
        missing_data_indices.append(i)
        continue

    if not umsdlnr.startswith(("Ga", "Wo", "Bi")):
        missing_data_indices.append(i)
        continue

    splitted = umsdlnr.split("/")
    part = splitted.pop(1).strip(" ")
    for symbol in [" ", ",", ".", "=", "-"]:
        part = part.replace(symbol, "/")
    while " " in part:
        part.replace(" ", "")
    splitted.insert(1, part)
    umsdlnr = "/".join([s.strip() for s in splitted])
    hoflisten.at[i, "Umsiedlungsnummer"] = umsdlnr

hoflisten["Kopfzahl_der_Familie"] = pd.to_numeric(
    hoflisten["Kopfzahl_der_Familie"], errors="coerce"
).astype("Int64")

hoflisten["Kopfzahl_ehemalige_Besitzer"] = pd.to_numeric(
    hoflisten["Kopfzahl_ehemalige_Besitzer"], errors="coerce"
).astype("Int64")

for i, row in hoflisten.iterrows():
    if i not in missing_data_indices:
        origin_code = row["Umsiedlungsnummer"].replace("/", " ", 1)
        origin_code = f"{origin_code.split(' ')[0]} {origin_code.split(' ')[1]}"
    else:
        origin_code = pd.NA
    origin = find_most_similar_term_from_df(origin_code, origin_districts, "variants")
    camp_akk = find_most_similar_term_from_df(row["Lager_lt_AK-K"], camps, "variants")
    camp_vomi = find_most_similar_term_from_df(row["Lager_lt_Vomi"], camps, "variants")
    settlement = find_most_similar_term_from_df(
        row["Gemeinde"], target_setttlements, "variants"
    )
    district = find_most_similar_term_from_df(
        row["Kreis"], target_districts, "variants"
    )

    if not camp_akk.empty:
        hoflisten.at[i, "Lager_lt_AK-K_geometry"] = wkt.loads(
            f"POINT ({camp_akk['lon'].item()} {camp_akk['lat'].item()})"
        )

    if not camp_vomi.empty:
        hoflisten.at[i, "Lager_lt_Vomi_geometry"] = wkt.loads(
            f"POINT ({camp_vomi['lon'].item()} {camp_vomi['lat'].item()})"
        )

    if not settlement.empty:
        hoflisten.at[i, "Gemeinde_geometry"] = wkt.loads(
            f"POINT ({settlement['lon'].item()} {settlement['lat'].item()})"
        )

    if not district.empty:
        hoflisten.at[i, "Kreis_geometry"] = wkt.loads(
            f"POINT ({district['lon'].item()} {district['lat'].item()})"
        )

    if not origin.empty:
        hoflisten.at[i, "Umsiedlungsnummer_geometry"] = origin["geowkt"]

hoflisten.to_csv("hoflisten_ready2use.csv", index=False)
