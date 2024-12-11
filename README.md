TKT20019

# Ryhmä Chat

Tämä web-applikaatio antaa käyttäjän lähettää viestejä eri ryhmissä muille käyttäjille. Käyttäjä voi luoda uusia ryhmiä ja kutsua muita käyttäjiä näihin ryhmiin.

## Valipalautus 3:

Sovelluksen kaikki toiminnot on toteutettu ja perus tietoturvahuolet niin kuin CSRF ja SQL-injektio ja salasanan salaaminen on otettu huomioon. Ulkonäköa ei ole vielä hiottu.

## Välipalautus 2:

Sovelluksen ulkonäköä ei ole hiottu, ei ole vielä reaaliaikaista viestintää ja jotkut toiminnot, esim. ryhmästä poistuminen ei ole vielä toteutettu.

## Setup

1. **Asenna docker compose**

- **Linux:**

  ```bash
  sudo apt-get update
  sudo apt-get install docker-compose-plugin
  ```

  (ohjeet haettu netistä, ei testattu)

- **Mac:**

  Jos sinulla on Homebrew asennettuna, voit asentaa Docker Composen suorittamalla:

  ```bash
  brew install docker-compose
  ```

  Vaihtoehtoisesti voit käyttää Docker Desktop for Mac -ohjelmistoa, joka sisältää Docker Composen. Lataa se [Dockerin virallisilta verkkosivuilta](https://www.docker.com/products/docker-desktop) ja seuraa asennusohjeita.

2. **Run init_local.sh**

   ```bash
   ./init_local.sh
   ```

   Tämä scripti alustaa venv:in, tietokannan ja käynnistää flaskin

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
