# LAT-CES Reference House Showcase

Model: `LAT-CES-REFERENCE-HOUSE-001`

## Koncept

Tri etaže (`P`, `S1`, `S2`) po 12 × 10 m, visina etaže 2.8 m, dvovodni krov 35°, kotlovnica u prizemlju, kombinacija podnog i radijatorskog grijanja, balansirana ventilacija i parametarski prikaz hlađenja/rasvjete.

## Demonstracijski tokovi

- Kuća 360°: rotacija 0–359° i slojevi konstrukcija/grijanje/ventilacija/hlađenje/svjetlo.
- Ulazak u prostorije: navigacija kroz sve grijane prostorije sa prikazom namještaja i MEP trasa.
- Proračuni: površina, volumen, krov, zidovi, procjena blokova, beton, grijanje, protok vode za grijanje, ventilacija i rasvjeta.
- MEP: podno/radijatorski krugovi, dovod/izvod zraka i demonstracija brzine zraka.
- Komfor: podesivi prikaz zone strujanja i tekstualno tumačenje osjeta propuha.
- Omotač: parametarske usporedbe izolacije i stakla; rezultati su komparativni, ne normativna provjera.

## Energetska logika

Poboljšanje U-procjene zida dobija se povećanjem toplinskog otpora sloja izolacije. Završne podne obloge su uključene u model kao materijal/quantity input, ali se njihova energetska razlika ne smije pogrešno predstavljati kao zamjena za izolaciju omotača.

## GUI

`lat-ces-reference-house` pokreće fullscreen showroom. `F11` uključuje/isključuje fullscreen, `A+ / A-` mijenja veličinu fonta, a rotacija koristi 15° korak.

Sve prikazane vrijednosti su eksplicitni demo ulazi. Za projektantsku upotrebu potrebno je povezati normativni model, nacionalni dodatak i verificirane proizvođačke podatke.
