> [!WARNING] 
> _Work in Progress_

# Hofzuweisungslisten

This repository is used to manage the dataset __Hofzuweisungslisten.csv__. It documents resettlement campaigns of Volhynian and Galician Germans (stemming from regions in today's western Ukraine, south-western Belarus and eastern Poland) into former polish territories, during 1940.

The dataset was derived from around 750 scanned pages containing mostly tabular data (see *[Provenance](/Provenance/)* folder for more information).

## Dataset Description

The dataset comprises 4838 records with 21 fields and is provided as CSV (Comma-Separated-Values). Empty fields denote that no information was present in the original document. The field names correspond as far as possible to the field names in the original documents.

> [!IMPORTANT]
> Despite extensive curation efforts, the dataset is not free from erroneous data. **Please see [Issues](/../../issues/)**.

| Field Name                | Data Type | Description |
|---------------------------|-----------|-------------|
| **signature**             | String    | Signature string derived from the filename of the scanned sheet (*filename = <signature_string>_<sheet_number>*).|
| **sheet_number**          | Integer   | Sheet number derived from the filename of the scanned sheet (*filename = <signature_string>_<sheet_number>*). |
| **Datum_Liste**           | Date      | Date when the list was created or documented. |
| **Datum_Ansiedlung**      | Date      | Date of resettlement event. |
| **Ansiedlungsdorf**       | String    | Name of the settlement village. |
| **Gemeinde**              | String    | Name of the community or municipality. |
| **Kreis**                 | String    | Name of the district or region. |
| **Lfd.Nr.**               | Integer   | Sequential or running number for a certain resettlement event. |
| **Heimatort**             | String    | Place of origin or hometown of the German settlers. |
| **Lager_lt_Vomi**         | String    | Name or number of the camp according to VoMi (Volksdeutsche Mittelstelle). |
| **Lager_lt_AKK**          | String    | Name or number of the camp according to AKK. |
| **Name**                  | String    | Last name of the family head of the German settlers. . |
| **Vorname**               | String    | First name of the family head of the German settlers. . |
| **Umsiedlungsnummer**     | String    | Resettlement number assigned to the individual or family (Germans). |
| **Vomi-Kenn-Nummer**      | String    | VoMi identification number. |
| **Kopfzahl_der_Familie**  | Integer   | Number of family members (German Settlers). |
| **Hofnummer**             | String    | Farm or homestead identification number. |
| **Ehemalige_Besitzer**    | String    | Previous owner(s) of the property. |
| **Kopfzahl_ehemalige_Besitzer** | Integer | Number of individuals in the previous owner's family. |
| **Bemerkung**             | String    | Additional remarks or comments regarding the record. |
| **notes_from_editors**    | String    | Notes or annotations provided by the editors of the record. |


## Further Context

In 1940, the propaganda slogan "Heim ins Reich" (en: back home to the Reich) called upon numerous German-speaking population groups from Eastern and South-Eastern Europe to resettle in areas within the borders of the German Reich. However, the majority of these settlers were not granted land in the heartland but in the annexed territories. This “Germanization” of the east focused on formerly Polish territories, such as the Reichsgauen Wartheland (“Warthegau”) and Danzig-West Prussia. However, before the settlers were granted any land, they were placed in camps and  underwent   racial profiling, which (in essence) ascertained their degree of “Germaness”. If deemed insufficient, “inferior” settlers were deployed as cheap workforce in the heartland (Stephan Döring: Umsiedlung der Wolhyniendeutschen in den Jahren 1939 bis 1940
). Conversely, the settlement of racially acceptable "returnees" was meticulously planned—often there were only a few hours between the expulsion of the former owners and the arrival of the German settlers. 

The resettlement campaigns were administered by the “Volksdeutsche Mittelstelle” (VoMi). Coordination and documentation was realized through so-called “Hofzuweisungslisten” (en: farm allocation lists). These were preprinted tabular forms, including the date of settlement, the settlement village, the names and family size of the settlers as well as those of the expelled former inhabitants, the settlers' place of origin and the camp in which the settlers lived. The columns of preprints were filled using typewriters some days ahead of the relocation of a family from the camp to their new homestead.


<!-- The poster presents a semi-automated workflow for creating a high-quality digital dataset from scans of such farm allocation lists. It focuses on recognizing the texts and the table structure using optical character recognition (OCR) methods and geocoding (assigning coordinates) the toponyms contained in the documents. Due to its exceptional performance with tables and typewriting, Amazon Textract was choosen for the initial OCR analysis. Subsequent analysis was instrumented with tools of the open source OCR suite OCR-D. To establish interoperability of the Textract output with OCR-D, a new OCR-D module which converts Amazon Textract outputs into the open PRImA-Page-XML format was developed (https://github.com/slub/textract2page). High accuracy geocoding was achieved by deriving a specialized gazetteer for the period and regions.
The resulting  dataset was derived from approximately 750 scans, which mostly cover the resettlement campaigns of Volhynian and Galician Germans (stemming from regions in today's western Ukraine, south-western Belarus and eastern Poland). The dataset resolves to nearly 5000 entries, where each entry documents the settlement of a family and the expulsion of another. With a conservative estimate of a mean family size of five people, this would correspond to the documentation of 25,000 resettlements and just as many expulsions. The dataset is made available open and according to the FAIR principles (https://doi.org/10.5281/zenodo.10665221). It is provided in the tabular CSV file format and accompanied by a describing CSVW metadata file. This enables easy re-usability  of the data by common spreadsheet software, but also allows the conversion of the dataset into Linked Data formats for more advanced analysis.

The central element of the poster is a multimodal exploration and presentation of the dataset on a map. -->