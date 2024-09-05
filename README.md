> [!WARNING] 
> _Work in Progress_

# Hofzuweisungslisten

This repository is used to manage the dataset __Hofzuweisungslisten.csv__. It documents resettlement campaigns of Volhynian, Galician, and Narew Germans (stemming from regions in today's western Ukraine, western Belarus, and southern and eastern Poland) into former Polish territories, during 1940.

The dataset was derived from around 750 scanned pages containing mostly tabular data (see *[Preprocessing](/Preprocessing/)* folder for more information).

## Further Context

In 1940, the propaganda slogan Heim ins Reich (en: back home to the Reich) called upon numerous German-speaking population groups from Eastern and South-Eastern Europe to resettle in areas within the borders of the German Reich. However, the majority of these settlers were not granted land in the heartland but in the annexed territories. This “Germanization” of the east focused on formerly Polish territories, such as the Reichsgauen Wartheland (“Warthegau”) and Danzig-West Prussia. However, before the settlers were granted any land, they were placed in camps and  underwent racial profiling, which (in essence) ascertained their degree of “Germaness”. If deemed insufficient, “inferior” settlers were deployed as cheap workforce in the heartland (Stephan Döring: Umsiedlung der Wolhyniendeutschen in den Jahren 1939 bis 1940). Conversly, the settlement of “racially acceptable” returnees was meticulously planned—often there were only a few hours between the expulsion of the former Polish owners from their farms and the arrival of the German settlers. 

The resettlement campaigns were administered by the “Volksdeutsche Mittelstelle” (Vomi). Coordination and documentation was realized through so-called “Hofzuweisungslisten” (en: farm allocation lists). These were preprinted tabular forms, including the date of settlement, the settlement village, the names and family size of the settlers as well as those of the expelled former inhabitants, the settlers' place of origin and the camp in which the settlers lived. The columns of preprints were filled using typewriters some days ahead of the relocation of a family from the camp to their new homestead.


<!-- The poster presents a semi-automated workflow for creating a high-quality digital dataset from scans of such farm allocation lists. It focuses on recognizing the texts and the table structure using optical character recognition (OCR) methods and geocoding (assigning coordinates) the toponyms contained in the documents. Due to its exceptional performance with tables and typewriting, Amazon Textract was choosen for the initial OCR analysis. Subsequent analysis was instrumented with tools of the open source OCR suite OCR-D. To establish interoperability of the Textract output with OCR-D, a new OCR-D module which converts Amazon Textract outputs into the open PRImA-Page-XML format was developed (https://github.com/slub/textract2page). High accuracy geocoding was achieved by deriving a specialized gazetteer for the period and regions.
The resulting  dataset was derived from approximately 750 scans, which mostly cover the resettlement campaigns of Volhynian and Galician Germans (stemming from regions in today's western Ukraine, south-western Belarus and eastern Poland). The dataset resolves to nearly 5000 entries, where each entry documents the settlement of a family and the expulsion of another. With a conservative estimate of a mean family size of five people, this would correspond to the documentation of 25,000 resettlements and just as many expulsions. The dataset is made available open and according to the FAIR principles (https://doi.org/10.5281/zenodo.10665221). It is provided in the tabular CSV file format and accompanied by a describing CSVW metadata file. This enables easy re-usability  of the data by common spreadsheet software, but also allows the conversion of the dataset into Linked Data formats for more advanced analysis.

The central element of the poster is a multimodal exploration and presentation of the dataset on a map. -->

## Dataset Description

The dataset comprises 4838 records with 21 fields and is provided as CSV (Comma-Separated-Values). Empty fields denote that no information was present in the original document. The field names correspond as far as possible to the field names in the original documents: spaces were replaced with underscore, stacked or otherwise combined columns were resolved into separate columns. Fields that were added by the editors are marked with an asterisk (*).

> [!IMPORTANT]
> Despite extensive curation efforts, the dataset is not free from erroneous data. **Please see [Issues](/../../issues/)**.

| Field Name                | Data Type | Description |
|---------------------------|-----------|-------------|
| ***id**                    | String    | ID of the record. ID = <file_signature>-<sheet_number>-<row_number>. Both sheet number and row number begin with 0. The row number is not equal to the value in the field _Lfd.Nr._
| **Datum_Liste**           | Date      | Date when the list was created or documented. |
| **Datum_Ansiedlung**      | Date      | Date of resettlement event. |
| **Ansiedlungsdorf**       | String    | Name of the settlement village. |
| **Gemeinde**              | String    | Name of the community or municipality. |
| **Kreis**                 | String    | Name of the district or region. |
| **Lfd.Nr.**               | Integer   | Sequential or running number for a certain resettlement event. |
| **Heimatort**             | String    | Place of origin or hometown of the German settlers. |
| **Lager_lt_Vomi**         | String    | Name of the camp according to Vomi (see below). |
| **Lager_lt_AK-K**         | String    | Name of the camp according to AK-K (see below). |
| **Name**                  | String    | Last name of the family head of the German settlers. |
| **Vorname**               | String    | First name of the family head of the German settlers. |
| **Umsiedlungsnummer**     | String    | Resettlement number assigned to the individual or family (Germans). The number holds coded information about the settlers origin (see  below). |
| **Vomi-Kenn-Nummer**      | String    | Vomi identification number. |
| **Kopfzahl_der_Familie**  | Integer   | Number of family members (German Settlers). |
| **Hofnummer**             | String    | Farm or homestead identification number. |
| **Ehemalige_Besitzer**    | String    | Previous owner(s) of the property. |
| **Kopfzahl_ehemalige_Besitzer** | Integer | Number of individuals in the previous owner's family. |
| **Bemerkung**             | String    | Additional remarks or comments regarding the record. |
| ***notes_from_editors**    | String    | Notes or annotations provided by the editors of the record. |
| ***image_filename**    | String    | Filename of the scan of the original document. |



### The Meaning of the Column Umsiedlungsnummer

In "Die Umsiedlung der Wolhyniendeutschen in den Jahren 1939 bis 1940" (Stephan Döring, 2001, en: Resettlement of the Wolhynian Germans in the years from 1939 to 1940), p. 88 f, p. 105, the meaning of the Umsiedlungsnummer and the resettlement process in general are explained: 

Before the resettlement (some would say uprooting) took place, each household/family that qualified to settle in the former West-Polish territories (namely Warthegau) was registered. The registration was organized by subdividing the territory in 50 areas (within 7 districts, within 3 regions). Each person that was willing and qualified for resettlement was registered and given a metal plate with their resettlement id (Umsiedlungsnummer), e.g. `Ga I 3/16/4/24`, stamped in. If we define an according scheme, `a b c/d/e/f`, then:

- `a` (a one or two letter string, e.g. ,`Ga`) identifies the region in which the registration took place. According to Döring, there are Wo for Volhynia, Ga for Galicia and B for Bilsk (Narew region),
- `b` (a Roman numeral, e.g., `I`) identifies the district within the according region. Ga and Wo were divided in 3 regions, B was a singular districts. Each district had a authorized district representative, who had a seat within the region. The seats for the 7 districts are: 

    - `Ga I` - Lemberg, 
    - `Ga II` - Stanislau, 
    - `Ga III` -Stryi, 
    - `Wo I` - Luck, 
    - `Wo II` - Kostopol, 
    - `Wo III` - Wladimir-Wolynsk, and 
    - `B` - Bilsk, 
  
- `c` (an Arabic numeral, e.g., `3`) identifies the area within the according district,
- `d` (an Arabic numeral, e.g., `16`) identifies the number of the according governmental list (what this list is is not explained),
- `e` (an Arabic numeral, e.g., `4`) identifies the running registration number of the registered household within the according registering area, and
- `f` (an Arabic numeral, e.g., `24`) identifies the running number in the registration list.

#### Application for this dataset

The scheme described by Döring does not exactly match the data present in the field Umsiedlungsnummer. This is mostly due to inconsistent separators across the dataset (the scheme in this dataset would be `a b/c( ,.-=/)d/e/f`, see [Issue 9](/../../issues/9) for a Python snippet to normalize the separators). Also in this dataset `B` (for Blisk) does not appear, instead there are two occurrences of `Bi I`. Finally, sometimes the field is empty or contains information why data is missing, e.g., the string `Vorumsiedler` is a rather common entry.

### Course of Resettlement and the Meaning of the Columns Lager_lt_Vomi and Lager_lt_AK-K 

Vomi – Volksdeutsche Mittelstelle<br>
AK-K – AK-Karte, Arbeitskarteikarte

The settlers left their homes by train (women, old people and children) or by covered wagon (men and older boys). Once they reached German territory, they were placed in camps to organise their resettlement. The first camps were set up by the Vomi in and around Lodz. As there was not enough space most of the settlers were only deloused, (initially) registered by the EWZ (Einwandererzentralstelle, Immigration Central Office), and then transferred to observation camps  (*Beobachtungslager*) in the German heartland (Altreich), where they remained for a longer period. During this initial phase of the resettlement many families were separated.

Before a decision on the resettlement could be made, the settlers had to undergo a full registration by the EWZ. This entailed a racial profiling (*Durchschleusung*), which was kept secret from the settlers, but was crucial in determining whether or not they would be granted land. The results of this procedure were recorded on the AK-Ks of the EWZ.

Once the settlers had been allocated a new farm, they were moved to (*Sammellager*) on the eastern border of the Altreich, where the EWZ carried out any outstanding full registrations and reunited separated families. Finally, they were transferred to preparation camps (*Bereitstellungslager*), from where they were taken to their new homes.

Compiling this information, we think that the column Lager\_lt\_Vomi denotes the settler's initial camp at Lodz, and Lager\_lt\_AK-K the camp where the full registration by the EWZ, i.e. the racial profiling, was conducted.

(Die Umsiedlung der Wolhyniendeutschen in den Jahren 1939 bis 1940, Stephan Döring, 2001, p. 335 ff.)
