# %%
"""
- script analyzes text in table and and text outside the table separatly
- text outside table:
    - interesting information are dates and places
    - ignore information where the minimum y-coordinate is < 300 or > image_size/2 (non-interesting)
    - for dates:
        - create combines string of residual text after removal of uninteresting parts
        - transform roman numbers and written out months to arabic numbers
        - remove all white spaces
        - remove all "40"s from text (this is part of the orginial form -- the year is always 40) 
        - try to detect day-month-dates with regex "\d{1,2}[./]\d{1,2}"
        - try to convert found dates into python datetime objects -> store if successful, discard otherwise
    - for places:
        - remove anything string from the list of strings that is part of the original preprintet form
        (make list of all preprintet strings, if detected string has Levenshtein dist < 3 to one of these
        string: remove)
        - remove any string that contains at least one digit
        - remaining strings should be the places in the order: village, township, district
- text inside table
    - 0th col
        - ignore
        - sometimes the numbers are left of the border -> this causes the creation of a new 0th col and the
        first col is empty. check this by counting col, if nb == 8: remove 0th col
    - 1st col:
        - try to split into three cols (Heimatort, lager VOMI, lager AKK) by splitting at \n:
        - if nb(\n)>3: write all cell information in Heimatort col and fill the other cols with empty strings (mark this with >ERR(...))
        - if nb(\n)<3: fill remaining cols with empty strings
        - if len of string in cell <2 e. string contains '' or " or similar, which indicates equality of content with top cell): 
            - write contents of cells from the row atop into current row        
    - 2nd col: 
        - same as frist col but try to split into 4 cols (last_name, first_name, settling_nb and vomi_nb): 
        - names and numbers are distinguished by \n
        - fist and last name by " " or ","
        - if something fails also write everything into first_name col and mark with >ERR(...)
    - 3rd col:
        - insert if text is a number
    - 4th col:
        - copy text
    - 5th col: 
        - split into name and headcount col 
        - search for numbers in string ("\d+"), if found write them into headcount col
        - remove "(" and ")"
        - write the rest into name col
    - 6th col:
        - copy text
"""


from ocrd_models.ocrd_page import parseEtree, PcGtsType, TextRegionType, TableRegionType
from ocrd_models.ocrd_page import to_xml
from typing import Tuple
import numpy as np
import pandas as pd
import os, json
import re
import Levenshtein
from datetime import datetime


def get_table_shape(table_region: TableRegionType) -> Tuple[int, int]:
    """Iterate through all TextRegions of a TableRegion and analyze
    their TableCellRole properties to determine the tables shape.

    For the Hofzuweisungslisten data, row and column indices start at
    one and not at zero.
    """
    row_indices = []
    col_indices = []
    for text_region in table_region.get_TextRegion():
        roles = text_region.get_Roles()
        table_role = roles.get_TableCellRole()
        row_index = table_role.get_rowIndex()
        col_index = table_role.get_columnIndex()
        row_indices.append(row_index)
        col_indices.append(col_index)

    rows = max(row_indices) + 1
    cols = max(col_indices) + 1

    return rows, cols


def get_text_from_TextRegion(text_region: TextRegionType) -> str:
    """Get Text from text region.
    For the Hofzuweisungslisten pages, we know that the text ist
    stored in TextLines. If the text in a TextLine was corrected
    in Larex, the corrected text is inserted a index 0. If no
    correction was neccessary there is no index zero, but only
    index one, which contains the "original" text that was produced
    by AmazonTextract. If the file was not opend in Larex there is no
    index, we then assume its the first equiv we find.
    """

    region_text = []
    for line in text_region.get_TextLine():
        text_equivs = line.get_TextEquiv()
        text = ""
        text = text_equivs[0].get_Unicode()
        for text_equiv in text_equivs:
            if text_equiv.index == 1:
                text = text_equiv.get_Unicode()

        for text_equiv in text_equivs:
            if text_equiv.index == 0:
                text = text_equiv.get_Unicode()
        region_text.append(text)

    return f"{os.linesep}".join(region_text)


def analyze_line(line, indicator_string):
    if line == "Übertrag von Seite:" and indicator_string == "Übertrag":
        return False
    if indicator_string in line:
        # check if date is in curr line
        if len(line.split(indicator_string)[-1].strip()) > 0:
            return line.split(indicator_string)[-1].strip()
        return "flag"
    return False


def export(in_path, includes_yard_size_col):
    page = parseEtree(in_path)[0].get_Page()
    table_regions = page.get_TableRegion()
    if len(table_regions) > 2:
        print(f">2 Tabelllen in: {in_path}")
    df = None
    for table_region in table_regions:
        rows = table_region.get_rows()
        cols = table_region.get_columns()

        if not (rows and cols):
            rows, cols = get_table_shape(table_region)

        # TODO remove when indexation in textract2page is fixed (also in for loop)
        rows = rows - 1
        cols = cols - 1

        table_list = []
        max_text_len = 0
        # iterate through table region and fill array accordingly
        for text_region in table_region.get_TextRegion():
            roles = text_region.get_Roles()
            table_role = roles.get_TableCellRole()
            row_index = table_role.get_rowIndex() - 1
            col_index = table_role.get_columnIndex() - 1
            text = get_text_from_TextRegion(text_region)
            table_list.append((row_index, col_index, text))
            # print(row_index, col_index, text)
            max_text_len = max(max_text_len, len(text))

        table_arr = np.empty((rows, cols), dtype=np.dtype(f"<U{max_text_len}"))
        for row, col, text in table_list:
            table_arr[row, col] = text
        # print(table_arr)
        table_dict = {
            key: []
            for key in [
                "Signatur",
                "Blattnummer",
                "Datum_Liste",
                "Datum_Ansiedlung",
                "Ansiedlungsdorf",
                "Gemeinde",
                "Kreis",
                "Heimatort",
                "Lager_lt_Vomi",
                "Lager_lt_AKK",
                "Name",
                "Vorname",
                "Umsiedlungsnummer",
                "Vomi-Kenn-Nummer",
                "Kopfzahl_der_Familie",
                "Hofnummer",
                "Ehemalige_Besitzer",
                "Kopfzahl",
                "Bemerkung",
            ]
        }

        (
            signature,
            page_nb,
            list_date,
            settling_date,
            village,
            township,
            district,
            origin,
            camp_vomi,
            camp_akk,
            last_name,
            first_name,
            resettlement_nb,
            vomi_nb,
            headcount_new,
            yard_nb,
            owner_old,
            headcount_old,
            comment,
        ) = (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )

        image_height = page.get_imageHeight()
        meta_text_lines = []
        meta_text_regions = page.get_TextRegion()
        for meta_text_region in meta_text_regions:
            # ignore bottom half text equivs, they have no relevant information
            if (
                min(
                    [
                        int(point.split(",")[1])
                        for point in meta_text_region.get_Coords()
                        .get_points()
                        .split(" ")
                    ]
                )
                > image_height / 2
            ):
                continue
            # ignore document header text equivs, they have no relevant information
            if (
                min(
                    [
                        int(point.split(",")[1])
                        for point in meta_text_region.get_Coords()
                        .get_points()
                        .split(" ")
                    ]
                )
                < 300
            ):
                continue

            text_line = get_text_from_TextRegion(meta_text_region)
            meta_text_lines.append(text_line)

        # --- SIGNATURE AND PAGE NUMBER ---
        # str.rpartition() only splits once but always returns a fixed number of elements (prefix, delimiter & postfix)
        signature, _, page_nb = os.path.basename(in_path).rpartition("_")
        signature = signature.split("OCR-D-IMG_")[1]
        page_nb = page_nb.split(".xml")[0]

        # --- DATES ---
        roman_numerals = {
            "I": "1",
            "II": "2",
            "III": "3",
            "IV": "4",
            "V": "5",
            "VI": "6",
            "VII": "7",
            "VIII": "8",
            "IX": "9",
            "X": "10",
            "XI": "11",
            "XII": "12",
        }
        months = {
            "Januar": "1.",
            "Februar": "2.",
            "März": "3.",
            "April": "4.",
            "Mai": "5.",
            "Juni": "6.",
            "Juli": "7.",
            "August": "8.",
            "September": "9.",
            "Oktober": "10.",
            "November": "11.",
            "Dezember": "12.",
        }

        all_meta_text = "".join(meta_text_lines)
        # rm "40" -> it's always the year 40, but the number can lead to errors
        all_meta_text = all_meta_text.replace("40", "")
        # roman to arabic
        for key, val in roman_numerals.items():
            all_meta_text = all_meta_text.replace(key, val)
        # # months to numbers
        for key, val in months.items():
            all_meta_text = all_meta_text.replace(key, val)
        all_meta_text = all_meta_text.replace(" ", "")
        date_pattern = re.compile(r"\d{1,2}[./]\d{1,2}")
        dates = date_pattern.findall(all_meta_text)
        # print(all_meta_text)
        # print(dates)
        dates = [date.replace("/", ".").replace("..", ".") + ".1940" for date in dates]
        dates = [
            ".".join([f"{int(number):02}" for number in date.split(".")])
            for date in dates
        ]
        # iterate revese, bcs pop()
        for i in range(len(dates) - 1, -1, -1):
            try:
                dates[i] = datetime.strptime(dates[i], "%d.%m.%Y").strftime("%Y-%m-%d")
            except:
                dates.pop(i)
        # append "", until line reaches len 2
        dates = dates + [""] * (2 - len(dates))
        # print(dates)
        list_date, settling_date = dates

        # --- PLACES ---
        # remmove any strings with digits
        places = [
            place
            for place in meta_text_lines
            if not any(char.isdigit() for char in place)
        ]
        # remove strings that are similar to strngs from the form
        form_strings = [
            # "Der Höhere 44 und Polizeiführer",
            # "Vertraulich!",
            # "S.",
            "Ansiedlungsstab",
            "Hofzuweisungsliste vom",
            "Ansiedlungsdorf",
            "Ansiedlungstag",
            "Gemeinde",
            "Verteiler: Aussenstellen",
            "Kreis",
            # "Summe:",
            # "Übertrag von Seite:",
            # "Übertrag",
        ]
        # remove anything that is similar to strings from the form
        places = [
            place
            for place in places
            if all(
                Levenshtein.distance(place, form_string) > 2
                for form_string in form_strings
            )
        ]
        if len(places) == 3:
            village, township, district = places
            if "Ansiedlungsdorf" in village:
                village = village.split("Ansiedlungsdorf")[1].strip()
            if "Gemeinde" in township:
                township = township.split("Gemeinde")[1].strip()
            if "Kreis" in district:
                district = district.split("Kreis")[1].strip()
        else:
            village = f">ERR({places})"
            township, district = "", ""

        # --- TABLE CONTENTS ---
        # rm first col if some of the running numers created an 8th col left (don't do if the file has
        # the extra yard size collumn)
        if in_path in includes_yard_size_col:
            # print(table_arr)
            pass
        else:
            if table_arr.shape[1] > 7:
                table_arr = table_arr[:, 1:]
        for i, row in enumerate(table_arr):
            # print(row)

            # ignore 0th row
            if not i:
                continue
            # ignore empty rows (we say a row where less than 3 cells are filled is empty, artifacts might cause non-existant cell-content)
            if sum([bool(field) for field in row]) < 3:
                continue

            for j, col in enumerate(row):

                if j == 1:
                    # check if duplicate_top_content was used
                    if len(col) <= 2 and len(col) > 0:
                        # print(col)
                        origin, camp_vomi, camp_akk = (
                            table_dict["Heimatort"][-1],
                            table_dict["Lager_lt_Vomi"][-1],
                            table_dict["Lager_lt_AKK"][-1],
                        )
                    else:
                        lines = col.strip("\n").split("\n")
                        # if more than 4 rows, append to cell on top
                        # print(lines)
                        if len(lines) > 3:
                            lines = [f">ERR({' '.join(lines)})"]
                        lines = lines + [""] * (3 - len(lines))
                        # print(lines)
                        origin, camp_vomi, camp_akk = lines
                if j == 2:
                    # check if duplicate_top_content was used
                    if len(col) <= 2 and len(col) > 0:
                        # print(col)
                        last_name, first_name, resettlement_nb, vomi_nb = (
                            table_dict["Name"][-1],
                            table_dict["Vorname"][-1],
                            table_dict["Umsiedlungsnummmer"][-1],
                            table_dict["Vomi-Kenn-Nummer"][-1],
                        )
                    else:
                        lines = col.strip("\n").split("\n")
                        # print(lines)
                        # if first line contains only digits it is part of the number from the cell on top
                        if lines[0].isdigit():
                            table_dict["Vomi-Kenn-Nummer"][-1] += lines.pop(0)
                        # append "", until line reaches len 3
                        lines = lines + [""] * (3 - len(lines))
                        # print(lines)
                        # if more than 3 lines, write everything as ERR in last_name
                        if len(lines) > 3:
                            lines = [f">ERR({' '.join(lines)})"]
                            lines = lines + [""] * (4 - len(lines))
                            last_name, first_name, resettlement_nb, vomi_nb = lines
                        else:
                            last_name, _, first_name = lines[0].partition(" ")
                            if "," in lines[0]:
                                last_name, _, first_name = lines[0].partition(",")
                            while len(lines[1:]) > 2:
                                lines[-2] += lines.pop(-1)
                                lines[-1] = f">ERR({lines[-1]})"
                            resettlement_nb, vomi_nb = lines[1:]
                if j == 3:
                    headcount_new = col
                if j == 4:
                    yard_nb = col.replace("\n", " ")
                if j == 5:
                    match = re.search(r"\d+", col)
                    headcount_old = match.group() if match else ""
                    owner_old = (
                        col.replace("\n", "")
                        .replace("(", "")
                        .replace(")", "")
                        .replace(headcount_old, "")
                    )
                comment = ""
                if in_path in includes_yard_size_col:
                    if j == 8:
                        comment = col.replace("\n", " ")
                else:
                    if j == 6:
                        comment = col.replace("\n", " ")

            table_dict["Signatur"].append(signature.strip())
            table_dict["Blattnummer"].append(page_nb.strip())
            table_dict["Datum_Liste"].append(list_date)
            table_dict["Datum_Ansiedlung"].append(settling_date)
            table_dict["Ansiedlungsdorf"].append(village.strip())
            table_dict["Gemeinde"].append(township.strip())
            table_dict["Kreis"].append(district.strip())
            table_dict["Heimatort"].append(origin.strip())
            table_dict["Lager_lt_Vomi"].append(camp_vomi.strip())
            table_dict["Lager_lt_AKK"].append(camp_akk.strip())
            table_dict["Name"].append(last_name.strip())
            table_dict["Vorname"].append(first_name.strip())
            table_dict["Umsiedlungsnummer"].append(resettlement_nb.strip())
            table_dict["Vomi-Kenn-Nummer"].append(vomi_nb.strip())
            table_dict["Kopfzahl_der_Familie"].append(headcount_new.strip())
            table_dict["Hofnummer"].append(yard_nb.strip())
            table_dict["Ehemalige_Besitzer"].append(owner_old.strip())
            table_dict["Kopfzahl"].append(headcount_old.strip())
            table_dict["Bemerkung"].append(comment.strip())

        df = pd.DataFrame(table_dict)

    return df


# Specify the directory path
directory_path = "page-xml-reviewed"

# List all files in the directory
files = [
    os.path.join(directory_path, file)
    for file in os.listdir(directory_path)
    if os.path.isfile(os.path.join(directory_path, file))
]
ignore = [
    "page-xml-reviewed/OCR-D-IMG_Ansiedlung_WD_Wielun_Lentschütz_00" + str(i) + ".xml"
    for i in range(29, 55)
]
includes_yard_size_col = [
    f"page-xml-reviewed/OCR-D-IMG_Lodz_UZS_25_00{i:02}.xml" for i in range(0, 7)
] + ["page-xml-reviewed/OCR-D-IMG_Lodz_UZS_25_0056.xml"]

# files = [
#     "/home/rue_a/hoflisten/page-xml-reviewed/OCR-D-IMG_Evakuierungen_und_Ansiedlungen_Schieratz_EUZ_Syg_30_0015.xml"
# ]
dfs = []
for f in files:
    if f in ignore:
        continue
    # Assume export function returns a DataFrame (df_) and a metadata dictionary
    print(f)
    df = export(f, includes_yard_size_col)
    dfs.append(df)
    # Define the file names for CSV
    # csv_file_name = f"csv/{os.path.basename(f).split('.')[0]}.csv"

    # # Write CSV
    # try:
    #     df.to_csv(csv_file_name, index=False)
    # except Exception as e:
    #     print(f"CSV writing failed: {e}")

try:
    pd.concat(dfs).sort_values(["Signatur", "Blattnummer"]).to_csv(
        "hofzuweisungslisten_as_table.csv", index=False
    )
except Exception as e:
    print(f"CSV writing failed: {e}")


# %%
