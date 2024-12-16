# NAO - NVDA Advanced OCR

* Tekijät: Alessandro Albano, Davide De Carne, Simone Dal Maso
* Lataa [vakaa versio][1]
* Yhteensopivuus: NVDA 2019.3 ja uudemmat

NAO (NVDA Advanced OCR) on lisäosa, joka parantaa tavanomaisia tekstintunnistustoimintoja, joita NVDA tarjoaa uusissa Windows-versioissa.
NVDA:n vakiokomento käyttää Windowsin tekstintunnistustoimintoa näytön sisällön tunnistamiseen, mutta NAO voi suorittaa tunnistuksen kiintolevylle tai USB-muistitikuille tallennetuille tiedostoille tai sähköpostiviestien liitteille.
Käytä NVDA+Vaihto+R-komentoa kuva- ja PDF-tiedostojen tunnistamiseen.
Siirrä kohdistus haluamasi tiedoston kohdalle ja paina NVDA+Vaihto+R.
Kun tiedoston tunnistus on suoritettu, näkyviin tulee yksinkertainen teksti-ikkuna, joka mahdollistaa koko sisällön lukemisen, tallentamisen, tekstin etsimisen tai sisällön kopioimisen leikepöydälle.
NAO pystyy käsittelemään myös monisivuisia PDF-tiedostoja, joten saavuttamaton asiakirja voidaan tehdä saavutettavaksi.

## Järjestelmävaatimukset
Lisäosa toimii Windows 10- ja Windows 11 -järjestelmissä, koska niissä on sisäänrakennettu tekstintunnistusominaisuus.
NAO on yhteensopiva NVDA 2019.3:n ja sitä uudempien versioiden kanssa.
Huom: NAO toimii Windowsin Resurssienhallinnassa, työpöydällä, Total Commanderissa tai xplorer²-tiedostonhallinnassa. Älä käytä muita ohjelmistoja kuten 7-Zipiä tai WinRARia, koska niitä ei tueta.
Sähköpostiviestien liitetiedostojen tunnistus toimii Microsoft Outlook 2016:ssa tai sitä uudemmassa.

## Ominaisuudet ja komennot
* NVDA+Vaihto+R: Tunnista kaikenlaiset kuva- ja PDF-tiedostot kiintolevyltä tai sähköpostin liitteistä.
* Page up / Page down: Siirrä kohdistinta monisivuisen dokumentin todellisten sivujen välillä.
* Ctrl+S: Tallenna dokumentti NAO-asiakirjamuodossa. Voit avata sen uudelleen NVDA+Vaihto+R-näppäinkomentoa käyttäen.
* P: Ilmoita sivunumero monisivuisessa dokumentissa suhteessa kohdistimen sijaintiin.
* L: Ilmoita rivinumero kohdistimen sijainnissa suhteessa nykyiseen sivuun.
* Vaihto+L: Ilmoita rivinumero kohdistimen sijainnissa suhteessa koko dokumenttiin.
* G: Siirry suoraan tietylle sivulle.
* C: Kopioi koko dokumentin teksti leikepöydälle.
* S: Tallenna dokumentin kopio tekstimuodossa.
* F: Etsi tekstiä ja lue muutama sana ennen ja jälkeen löytyneen merkkijonon.
* NVDA+Vaihto+Ctrl+R: Ota koko näytön kuvakaappaus ja tunnista se.
* Huom: Voit käyttää tavallisia NVDA-komentoja ikkunan tutkimiseen ja kohdistuksen siirtämiseen haluamaasi elementtiin. Voit esimerkiksi liikkua nuolinäppäimillä ja painaa painiketta Enterillä. Voit myös siirtää hiiren nykyiseen sijaintiisi NVDA+Laskinnäppäimistön / -näppäinkomennolla ja napsauttaa sitten vasemmalla/oikealla näppäimellä.
* NVDA+Vaihto+Ctrl+W: Ota kuvakaappaus nykyisestä ikkunasta ja tunnista se (voit käyttää samoja navigointikomentoja kuin koko näytön ruutukaappausta otettaessa).

Huom: Voit mukauttaa NAO:n näppäinkomentoja helposti NVDA:n Näppäinkomennot-valintaikkunasta. Avaa NVDA-valikko, siirry Asetukset-alivalikkoon ja valitse sieltä Näppäinkomennot-kohta. Muista, että tämä ominaisuus ei ole järjestelmänlaajuinen vaan se toimii vain siellä, missä NAO voi suorittaa tekstintunnistuksen. Toisin sanoen näppäinkomennot näkyvät vain, jos olet työpöydällä, Resurssienhallinnassa, Total Commanderissa tai Xplorerissa.

Voit myös keskeyttää kauan kestävän tekstintunnistusprosessin painamalla Peruuta-painiketta tunnistuksen etenemisen ikkunassa. Tämä ikkuna antaa tietoa tekstintunnistuksen tilasta 5 sekunnin välein. Voit määrittää edistymispalkin tilan ilmoittamisen tavalliseen tapaan NVDA+U-näppäinkomennolla.

NVDA-valikon Työkalut-alivalikosta löytyy NAO-kohta. Se sisältää seuraavat kohteet:
* Tiedostonvalitsin: Voit valita tiedoston käsiteltäväksi ilman pikanäppäintä.
* Lahjoita: Lahjoita NAO-lisäosan tekijöille.
* NAO:n verkkosivu: Avaa NAO:n kotisivun.
* Git: Avaa NAO:n lähdekoodivaraston Gitin sivustolla, jossa voit tarkastella sitä, tehdä muutoksia tai avata aiheen.
* Tarkista päivitys: Tarkistaa palvelimelta uuden NAO:n version saatavuuden.
* Tyhjennä välimuisti: Jos kohtaat ongelmia lisäosan kanssa, saat virheilmoituksia tai huomaat sen olevan hidas, tyhjennä välimuisti ongelman ratkaisemiseksi.


## Tuki ja lahjoitukset
NAO on täysin ilmainen. Muista kuitenkin, että se on tehty kehittäjien vapaa-ajalla.
Arvostamme mitä tahansa tukea, jota voit meille antaa.
<a href="https://nvda-nao.org/donate">Harkitse lahjoittamista</a>, jos työmme on mielestäsi hyvää ja parantaa elämääsi.

Haluatko ilmoittaa bugista, ehdottaa uusia ominaisuuksia tai kääntää lisäosan omalle kielellesi? Meillä on sähköpostiosoite sinua varten. Kirjoita osoitteeseen support@nvda-nao.org, niin autamme mielellämme.

## Versiohistoria
### 2025.1
* Yhteensopiva NVDA 2025.1:n kanssa
* Toteutettu tekstintunnistus valitulle avatun Outlook-viestin liitteelle Outlook 2016:ssa ja sitä uudemmissa
* Lisätty suomenkielinen käännös

### 2024.1
* NVDA 2024.1:n yhteensopivuus

### 2023.1.1
* Palautettu NVDA 2023.3:n yhteensopivuus
* Uusi NVDA+Ctrl+Vaihto+W-näppäinkomento ottaa kuvakaappauksen nykyisestä ikkunasta ja tunnistaa sen
* Lisätty brasilianportugalilainen käännös
* Tietoturvakorjaus suojatuille ruuduille
* NAO-työkaluvalikko poistettu suojatuista ruuduista
* Dokumenttien välimuisti poistettu suojatuista ruuduista
* NAO:n verkkosivun ja Git-koodivaraston linkit lisätty NAO-työkaluvalikkoon

### 2023.1
* Yhteensopivuus NVDA 2023.1:lle

### 2022.1.3
* Yhteensopivuus NVDA 2022.1:lle
* Päivitetty yksinkertaistetun kiinan ja ranskankieliset käännökset
* Espanjankielinen dokumentaatio päivitetty

### 2022.1.2
* NAO-dokumenttimuodon tallennus- ja latausominaisuus.
* Tunnistuksen tulokset voidaan tallentaa dokumenttivälimuistiin, joka nopeuttaa niiden avaamista seuraavalla kerralla. Jos tiedosto löytyy välimuistista, sitä ei tunnisteta uudelleen vaan käytetään sen sijaan välimuistissa olevaa versiota (tunnistusparametrien on oltava täsmälleen samat).
* Dokumentin viimeisin lukukohta tallennetaan välimuistin metatietoihin.
* Dokumenttivälimuistin automaattinen tyhjennys.
* Manuaalinen välimuistin tyhjennysvaihtoehto Työkalut-valikossa.
* Tiedosto voidaan nyt tunnistaa suoraan "pakatusta kansiosta" Windowsin Resurssienhallinnassa.
* Parempi virheellisten tiedostojen tarkistus.
* Parempi Windowsin Resurssienhallinnan yhteensopivuus erilaisia tiedostonvalintavaihtoehtoja käyttäen: ensin yritetään Shell.Application-menetelmää NVDA:ssa, sitten samaa menetelmää PowerShellissä ja viimeisenä turvaudutaan manuaaliseen selaamiseen.
* Tekstintunnistusmoottori säilyttää kieliasetuksen koko tunnistusprosessin ajan, vaikka sitä muutettaisiin monisivuisen tunnistuksen aikana.
* Tekstintunnistusjono useista lähteistä tunnistamista varten.
* Page down -näppäin siirtää monisivuisen dokumentin loppuun sen viimeisellä sivulla oltaessa ja ilmoittaa rivinumeron.
* Tiedostomuunnintyökaluja varten käytetään Windowsin väliaikaistiedostojen kansiota lisäosakansion sijaan (parempi suorituskyky NVDA:n massamuistiversioissa).
* Lisätty romaniankielinen käännös ja yksinkertaistetun kiinan käännös päivitetty.

### 2022.1.1
* Tuki DjVu-tiedostomuodolle.
* Tuki monisivuisille TIFF-tiedostoille.
* PDF-koodauksen bugikorjaus kiinankielisissä käyttöjärjestelmissä.
* Manuaalinen lisäosan päivitystoiminto NVDA:n Työkalut-valikossa.
* Yhteensopivuus NVDA 2019.3:sta lähtien.

### 2022.1
* Automaattinen lisäosan päivitys.
* Espanjan- ja ranskankieliset käännökset päivitetty.

### 2021.2
* PDF- ja kuvatiedostojen tekstintunnistustulokset näytetään uudessa teksti-ikkunassa, jossa on käytettävissä joitakin pikanäppäimiä yksinkertaisia toimintoja varten.
* Tuki Xplorer-tiedostonhallintasovellukselle.
* NAO:n näppäinkomennot ovat mukautettavissa NVDA:n Näppäinkomennot-valintaikkunasta.
* NAO toimii vain sellaisissa ikkunoissa, jossa sitä on mahdollista käyttää, joten jos olet ei-tuetussa ikkunassa, lisäosan näppäinkomento ohitetaan. Tämä ratkaisi merkittävän ongelman, jossa Excelin ja Wordin käyttäjät eivät voineet painaa NVDA+Vaihto+R-näppäinkomentoa, koska se oli virheellisesti NAO:n käytössä.
* Kauan kestävä tekstintunnistusprosessi voidaan keskeyttää painamalla Tunnistuksen edistymisikkunassa "Peruuta"-painiketta.
* Lisätty turkin-, venäjän-, espanjan-, kiinan- ja ranskankieliset käännökset.
* Käyttäjien on mahdollista tehdä projektille lahjoituksia.
* Korjattu bugi, jossa tietyt tiedostonimessä olevat merkit estivät tekstintunnistusta toimimasta kunnolla.

### 2021.1
* Ensimmäinen julkinen versio.


[1]: https://nvda-nao.org/download
