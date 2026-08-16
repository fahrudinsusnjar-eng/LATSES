# LAT-CES Material Catalog

## Namjena

Ovaj direktorij je **read-only ulazni sloj** za naučne/engineering sisteme LAT-CES-a.

AI sloj smije u ovaj katalog unositi samo informativne podatke prikupljene sa **službenih stranica proizvođača** ili službenih tehničkih dokumenata proizvođača.

AI sloj NE donosi:
- izbor konstruktivnog materijala;
- normativno odobrenje;
- proračunske kombinacije;
- parcijalne faktore sigurnosti;
- projektantsku odluku;
- zamjenu za važeće BAS EN / EN norme ili nacionalne anekse.

## Tok podataka

```text
službena stranica proizvođača
        ↓
AI informativni collector
        ↓
data/material_catalog/*.json
        ↓
Engineering / Structural / Thermal / HVAC layer
        ↓
provjera prema važećim normama i projektnoj specifikaciji
```

## Obavezni princip porijekla

Svaki zapis mora imati:

- proizvođača;
- naziv proizvoda;
- službeni URL izvora;
- datum preuzimanja/pregleda;
- referencu na tehnički list ili drugi službeni dokument kada postoji;
- tehničke vrijednosti sa jedinicama;
- napomenu da je vrijednost **manufacturer-declared / informativna**.

## Ne miješati slojeve

`material_catalog` nije projektni model materijala i nije normativna baza.

Drugi sloj može čitati ovaj katalog i koristiti podatke kao ulaz za daljnju provjeru, ali mora samostalno utvrditi:

1. da li je materijal dopušten za konkretnu namjenu;
2. koji standard i nacionalni aneks se primjenjuju;
3. koje projektne vrijednosti treba koristiti;
4. koje sigurnosne faktore i kombinacije djelovanja treba primijeniti.

## Format

- `catalog.schema.json` — mašinski provjerljiv ugovor zapisa;
- `materials/*.json` — pojedinačni proizvodi/materijali;
- `_template.material.json` — predložak za novi zapis.

Katalog je namjerno odvojen od `BuildingModel` i od statičkog solvera.
