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

Kopieer de inhoud van het schema bestand in een nieuwe querytool (rechtmuis klik op `hmsmeetnet_v3LPop`-> query tool), voer het uit.

### data

Download de zip file vanaf: https://drive.google.com/file/d/1aui_UKMYdRdJy07oZ7-97B-7hZFNCYqY/view?usp=sharing
Extraheer de zip file en rechtmuis klik op de nieuwedatabank, 

![afbeelding](https://user-images.githubusercontent.com/28403026/226174489-a954e0bf-0a93-48a7-9697-591109b151a1.png)
