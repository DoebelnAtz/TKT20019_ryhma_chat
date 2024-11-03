TKT20019 

# Ryhmä Chat

Tämä web-applikaatio antaa käyttäjän lähettää viestejä eri ryhmissä muille käyttäjille. Käyttäjä voi luoda uusia ryhmiä ja kutsua muita käyttäjiä näihin ryhmiin.

## Näkymät.
- Käyttäjän luominen
- Sisäänkirjautuminen
- Keskusteluryhmien listaus (kotinäkymä)
- Keskustelryhmä
- (\+ joitain virhetilanäkymiä)

## Vaatimukset
- Käyttäjä voi vapaasti luoda chat-ryhmiä.
- Käyttäjä voi kutsua muita käyttäjiä ryhmään.
- Käyttäjä voi liittyä vain kutsuttuihin ryhmiin.
- Käyttäjä näkee ryhmässä omat ja muiden viestit.
- Käyttäjä ei pysty lähettämään viestejä ryhmiin jonne se ei kuulu.
- Käyttäjä ei pysty näkemään viestejä ryhmissä johon se ei kuulu.
- Käyttäjä ei pysty näkemään viestejä jotka ovat lähetetty ennen ryhmään liittymistä.
- Käyttäjä pitää nähdä uusia viestejä ~reaaliajassa ilman että selaimen näkymää tarvitsee päivittää.

## Tietokantataulut

#### Käyttäjät
- Tunniste
- Käyttäjänimi
- Salasana

#### Ryhmät
- Tunniste
- Nimi

#### Ryhmäkäyttäjät
- Käyttäjä(tunniste)
- Ryhmä(tunniste)

#### Viestit
- Tunniste
- Viesti
- Lähettäjä - Käyttäjä(tunniste)
- Lähetetty aika

#### Ryhmäkutsut
- Lähettäjä - Käyttäjä(tunniste)
- Ryhmä(tunniste)
- Käyttäjä(tunniste)
