TKT20019

# Ryhmä Chat

Tämä web-applikaatio antaa käyttäjän lähettää viestejä eri ryhmissä muille käyttäjille. Käyttäjä voi luoda uusia ryhmiä ja kutsua muita käyttäjiä näihin ryhmiin.

## Valipalautus 3:

Sovelluksen kaikki toiminnot on toteutettu ja perus tietoturvahuolet niin kuin CSRF ja SQL-injektio ja salasanan salaaminen on otettu huomioon. Ulkonäköa ei ole vielä hiottu.

## Välipalautus 2:

Sovelluksen ulkonäköä ei ole hiottu, ei ole vielä reaaliaikaista viestintää ja jotkut toiminnot, esim. ryhmästä poistuminen ei ole vielä toteutettu.

## Setup

Asennusohjeet:

1. **Ympäristön valmistelu**: Varmista, että sinulla on asennettuna Python ja virtuaaliympäristötyökalu, kuten `venv` tai `virtualenv`.

2. **Virtuaaliympäristön luominen**: Luo ja aktivoi virtuaaliympäristö projektin juurikansiossa:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. **Riippuvuuksien asentaminen**: Asenna tarvittavat Python-kirjastot `requirements.txt`-tiedostosta:

   ```bash
   pip install -r requirements.txt
   ```

4. **Tietokannan alustaminen**: Voit alustaa tietokannan kahdella tavalla: joko käyttämällä valmista `docker-compose`-tiedostoa tai oman tietokantapalvelimen avulla.

   **Vaihtoehto 1: Docker-compose**

   Jos haluat käyttää `docker-compose`-työkalua, varmista, että se on asennettuna järjestelmääsi. Projektin juurikansiossa on valmiina `docker-compose.yml`-tiedosto, joka määrittelee Postgres palvelun:

   ```bash
   docker-compose up
   ```

   Tämä käynnistää PostgreSQL-tietokannan dockerissa ja alustaa sen automaattisesti portilla 6543

   **Vaihtoehto 2: Oma tietokantapalvelin**

   Jos haluat käyttää omaa tietokantapalvelinta, varmista, että PostgreSQL on asennettuna ja käynnissä. Suorita `schema.sql`-tiedosto luodaksesi tarvittavat tietokantataulut. Tämä voidaan tehdä esimerkiksi `psql`-komennolla:

   ```bash
   psql -U käyttäjänimi -d tietokanta -f schema.sql
   ```

   Sinun pitää myös lisätä Käyttäjänimen, portin, etc. tiedostoihin ./reset_db.sh ja ./config.py.

5. **Tietokannan alustaminen**:
   Suorita `./reset_db.sh` -skripti tietokannan nollaamiseksi ja alustamiseksi tarvittavilla tauluilla ja tiedoilla. Tämä skripti pudottaa olemassa olevat taulukot ja luo uudet schema.sql mukaisesti.

6. **Ympäristön alustaminen**:
   Suorita ./init_env.sh -skripti joka luo uuden .flaskenv tiedoston mallin perusteella.

7. **Sovelluksen käynnistäminen**: Käynnistä Flask-sovellus:

   ```bash
   flask run
   ```

8. **Käyttö**: Avaa selain ja siirry osoitteeseen `http://127.0.0.1:5000` käyttääksesi sovellusta.

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
  $$
