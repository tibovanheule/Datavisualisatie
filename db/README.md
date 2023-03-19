# Set-up of Database 

Download the pgadmin installer from here: https://www.postgresql.org/download/windows/

Install postgresql on youre system, make sure to also install pgadmin 4 (same installer, but make sure the pgadmin option is checked).


> use the same password everywhere! `dataviz`

## restore db
### set binary path in pgadmin

Voordat restore werk op uw pgadmin installatie, moet je het eerst vertellen waar de pgadmin 
![afbeelding](https://user-images.githubusercontent.com/28403026/226173300-b27d3066-1d9e-400c-aaf1-52e427d353dd.png)

### databank
In een querytool (rechtermuisklik op postgres db -> query tool), maak een nieuwe databank via volgende commando's.

```
CREATE DATABASE "hmsmeetnet_v3LPop" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Dutch_Belgium.1252';


ALTER DATABASE "hmsmeetnet_v3LPop" OWNER TO postgres;
```

> Voer ze best één per één uit! selecteer commando dat je wilt uit voeren voordat je op uitvoeren klikt.

### aanameken van de schema's

schema bestand: https://drive.google.com/file/d/19-fz_YFYEayl5NM_Ku0FyK97rr7uIINy/view?usp=sharing

Kopieer de inhoud van het schema bestand in een nieuwe querytool (rechtmuis klik op `hmsmeetnet_v3LPop`-> query tool), voer het uit.

### data

Download de zip file vanaf: https://drive.google.com/file/d/1aui_UKMYdRdJy07oZ7-97B-7hZFNCYqY/view?usp=sharing
Extraheer de zip file en rechtmuis klik op de nieuwedatabank, 

![afbeelding](https://user-images.githubusercontent.com/28403026/226174489-a954e0bf-0a93-48a7-9697-591109b151a1.png)

## data beschrijving

Belangrijke woordenschat:
- lspi: concatenatie van location_id en parameter.
- parameter: Wat er gemeten wordt. bijvoorbeeld graden of golfhoogte.
-

### functies

Er zijn bepaalde functies beschikbaar. Ze kunnen opgeroepen worden zoals rechts weergegeven in onderstaande figuur. 

![afbeelding](https://user-images.githubusercontent.com/28403026/226182694-e82992be-d7fe-48cf-8b6c-2a7756717708.png)

- beschikbaarheden(series_id): Dit zijn de beschikbaarheden, die berekent wordt door postgresql. seires_id is de id van measurements series.
- is_nan(): Niet van toepaasing hier, kijkt als iets nan is. gebruikt door andere functies.
- not_outliers(series_id): Geeft de datapunten terug van de series_id die geen outliers zijn! gebruikt de normaal verdeelde curve. Geeft dus alle data terug tussen gemiddelde -+ standaard_afwijking*2 ligt => ongeveer 99.97% van de data.
- not_outliers(series_id, multiplier INT): Hetzelfde als not_outliers(series_id), maar met optie om een INT (0,1,2,...) te geven om de formule te aan te passen. gemiddelde -+ standaard_afwijking*?.
- not_outliers(series_id, multiplier float): Hetzelfde als not_outliers(series_id), maar met optie om een Float (bijvoorbeeld 0.5) te geven om de formule te aan te passen. gemiddelde -+ standaard_afwijking*?.
- outliers(series_id): Geeft de datapunten terug van de series_id die outliers zijn! gebruikt de normaal verdeelde curve. Geeft dus alle data terug die niet tussen gemiddelde -+ standaard_afwijking*2 ligt => ongeveer 99.97% van de data.
- outliers(series_id, multiplier INT): Hetzelfde als outliers(series_id), maar met optie om een INT (0,1,2,...) te geven om de formule te aan te passen. gemiddelde -+ standaard_afwijking*?.
- outliers(series_id, multiplier float): Hetzelfde als outliers(series_id), maar met optie om een Float (bijvoorbeeld 0.5) te geven om de formule te aan te passen. gemiddelde -+ standaard_afwijking*?.

### tabellen

![afbeelding](https://user-images.githubusercontent.com/28403026/226183703-3b10957f-8a67-4628-8902-09372a630df7.png)

- aux_lookup: Aangemaakt door een collega, negeer dus best.
- aux_measurements: Aangemaakt door een collega, negeer dus best.
- beschikbaarheden: Om niet alle beschikbaarheden uit te rekenen bij elke fucntie call zijn van de afgelopen campagnes de beschikbaarheden al opgelsagen in een tabel.
- cb1: legt link tussen series_id en een cb1_bitvector
- cb1bitvector: Beschrijft afkomst data en de gebruikte validatie technieken. Sinds de volledige databank gevalideerd is, is deze tabel leeg
- cb2: legt link tussen series_id en een cb1_bitvector
- cb2bitvector: Beschrijft afkomst data en de gebruikte validatie technieken. Sinds de volledige databank gevalideerd is, is deze tabel leeg
- distribution: Aangemaakt door een collega, negeer dus best.
- eenheden: Beschrijft de eenheid van een parameter, bijvoorbeeld KWIZTW (kinte bank temperatuur zeewater) => graden
- estimator: Aangemaakt door een collega, negeer dus best! gebruikt voor bepaalde modellen op de data te draaien en te valideren, volledig buiten de scope van dit project.
- labels:  Aangemaakt door een collega, negeer dus best. LEEG
- locations: Locatie beschrijving van elke paremeters, vul ik nog aan!
- lookup: verbindt lspi, series en parameter aan elkaar.
- measurement_model: Aangemaakt door een collega, negeer dus best! gebruikt voor bepaalde modellen op de data te draaien en te valideren, volledig buiten de scope van dit project.

