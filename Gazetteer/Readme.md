# Gazetteer for [Hofzuweisungslisten](../hofzuweisungslisten.csv)

The dataset [Hofzuweisungslisten](../hofzuweisungslisten.csv) contains toponyms (terms that refer to a location on earth) in the fields Ansiedlungsdorf, Gemeinde, Kreis, Heimatort, Lager_lt_Vomi, Lager_lt_AK-K, Umsiedlungsnummer and Hofnummer. These gazetteers aim to collect these toponyms, identify different spellings or alternate terms, and provide geodata for them.

The gazetteers are provided according to the [LP-TSV v0.5](https://github.com/LinkedPasts/linked-places-format/blob/main/tsv_0.5.md#lp-tsv-v05-linked-places-delimited-derivative) (Linked Places delimited derivative) specification in csv-format.

## References

### [Gazetteer Resettlement Areas (Galicia, Volhynia, Narew region)](./gazetteer_resettlement_area_ga-wo-b.csv)

**Döring, 2001, p. 88f and p. 105:** Decoding and explanation of the Umsiedlungsnummer (see [dataset Readme](../README.md##the-meaning-of-the-column-umsiedlungsnummer)).

### [Gazetteer Camps]()

Transcription of **Döring, 2001, p. 367**, as CSV [here](./resources/camps_doering_2001_p367.csv). The column names translate to *withdrawl date*, *local district* (in [dataset Readme](../README.md#the-meaning-of-the-column-umsiedlungsnummer) referred to as *area*), *administrative center of the local destrict* (no column name in original table), *assembly camp*, and *availability camp*.

| Abberufungsdatum | Ortsbezirk   |   | Sammellager       | Bereitstellungslager   |
|------------------|--------------|---------|-------------------|------------------------|
| 16.04.1940       | Wo I/1       | Rozyszcze | Oderberg         | Kirschberg             |
| 07.05.1940       | Wo I/2       | Luck      | Oderberg         | Kirschberg             |
| 15.06.1940       | Wo I/4       | Marianowka | Oderberg        | Zgierz                 |
| nach Wo I/2      | Wo I/5       | Stanislawowka | Oderberg     | Tuschen                |
| 26.04.1940       | Wo I/6       | Bryszcze  | Pirna            | Kirschberg             |
| 07.05.1940       | Wo I/7       | Helenow   | Pirna            | Zgierz, Kloster        |
| 07.06.1940       | Wo I/8       | Gnidawa   | Pirna            | Grotniki               |
| 07.06.1940       | Wo I/9       | Podhajce  | Tetschen         | Kirschberg             |
| 07.06.1940       | Wo I/10      | Boszkiewicze | Tetschen      | Waldhorst              |
| 19.05.1940       | Wo I/11      | Zielona   | Sonderk. Portmann | Zgierz, Rogy         |
| 15.06.1940       | Wo I/12      | Bludow    | Pirna            | Zdunska-Wola           |
| 07.06.1940       | Wo I/13      | Torczyn   | Pirna            | Kirschberg             |
| 30.05.1940       | Wo I/14      | Wolka     | Oderberg         | Zdunska-Wola, Kloster  |
| 19.05.1940       | Wo I/15      | Alexandrowka | Oderberg      | Tuschin                |
| 26.04.1940       | Wo I/16      | Krzemieniec | Oderberg       | Zgierz, Waldfrieden    |
| 26.04.1940       | Wo I/17      | Kamien-Koszyrsk | Rumburg    | Zgierz, Dombrowska     |
| 20.06.1940       | Wo II/1      | Zademle   | Oderberg         | Waldhorst              |
| 15.06.1940       | Wo II/2      | Derazno   | Oderberg         | Waldhorst              |
| 19.05.1940       | Wo II/3      | Kostopol  | Pirna            | Waldhorst              |
| 30.05.1940       | Wo II/4      | Zuszyn    | Tetschen         | Tuschin                |
| 16.04.1940       | Wo II/5      | Maczulki  | Pirna            | Kirschberg             |
| 02.04.1940       | Wo II/6      | Topcza    | Oderberg         | Kirschberg             |
| 20.06.1940       | Wo III/1     | Swiezowska | Frankfurt       | Waldhorst              |
| nach Wo I/7      | Wo III/2     | Wanda-Wola | Pirna           | Tuschin                |
| 20.06.1940       | Wo III/3     | Janow     | Pirna            | Zdunska-Wola           |


### Döring, 2001, p. 372

Transcription of page 372, as CSV [here](./resources/districts_wartheland_doering_2001_p372.csv). The column names translate to *resettled local districts*, and *district in Reichsgau Wartheland*.

| Angesiedelte Ortsbezirke | Kreis im Reichsgau Wartheland                                               |
|--------------------------|----------------------------------------------------------------------------|
| Wo I/1 (Rozyszcze)        | Gostynin, Kalisch, Kutno, Lask, Lentschütz, Leslau, Litzmannstadt, Nessau, Sieradsch |
| Wo I/2 (Luck)             | Kolo, Konin, Lask, Leslau, Nessau, Sieradsch                              |
| Wo I/4 (Marianowka)       | Lask, Leslau, Litzmannstadt, Sieradsch, Wielun                            |
| Wo I/5 (Stanislawowka)    | Kolo, Kutno, Lask, Leslau, Lentschütz, Litzmannstadt, Nessau, Wielun      |
| Wo I/6 (Bryszcze)         | Gostynin, Kalisch, Konin, Lask, Lentschütz, Leslau, Wielun                |
| Wo I/7 (Helenow)          | Altburgund, Dietfurt, Gostynin, Kalisch, Kolo, Konin, Lask, Leslau, Litzmannstadt, Nessau, Sieradsch, Turek, Wielun |
| Wo I/8 (Gniedau)          | Dietfurt, Gostynin, Kalisch, Nessau, Wielun                               |
| Wo I/9 (Podhaice)         | Kolo, Lask, Leslau, Nessau, Sieradsch, Wielun                             |
| Wo I/10 (Boszkiewicze)    | Kutno, Lask, Lentschütz, Leslau, Litzmannstadt, Nessau, Sieradsch, Wielun |
| Wo I/11 (Zielona)         | Kutno, Nessau, Sieradsch                                                  |
| Wo I/12 (Bludow)          | Kutno, Lentschütz                                                         |
| Wo I/13 (Torczyn)         | Kolo, Kutno, Lask, Nessau, Sieradsch, Wielun                              |
| Wo I/14 (Wolka)           | Kutno, Lentschütz, Litzmannstadt, Turek                                   |
| Wo I/15 (Alexandrowka)    | Turek                                                                     |
| Wo I/16 (Krzemienice)     | Gostynin, Kutno, Lask, Lentschütz, Leslau, Litzmannstadt, Sieradsch, Turek |
| Wo I/17 (Kamien-Koszyrsk) | Lask, Turek                                                               |
| Wo II/1 (Zademle)         | Gnesen, Gostynin, Kutno, Lentschütz, Leslau, Nessau, Sieradsch, Turek     |
| Wo II/2 (Derazne)         | Kalisch, Lask, Lentschütz, Leslau, Litzmannstadt, Sieradsch, Turek        |
| Wo II/3 (Kostopol)        | Kutno, Lask, Lentschütz, Litzmannstadt, Turek                             |
| Wo II/4 (Tuczyn)          | Lask, Lentschütz, Litzmannstadt, Nessau, Turek, Wielun                    |
| Wo II/5 (Maczulki)        | Gostynien, Kalisch, Kutno, Kolo, Lask, Leslau, Sieradsch, Turek           |
| Wo II/6 (Topcza)          | Gostynien, Kolo, Kutno, Lask, Lentschütz, Nessau, Sieradsch, Turek, Wielun |
| Wo III/1 (Swiezowska)     | Gostynien, Kolo, Kutno, Lask, Lentschütz, Litzmannstadt, Nessau, Sieradsch, Turek |
| Wo III/2 (Wandawola)      | Gostynien, Lask, Lentschütz, Litzmannstadt, Sieradsch, Turek              |
| Wo III/3 (Janow)          | Gostynien, Konien, Lentschütz, Leslau, Nessau, Sieradsch, Turek           |

