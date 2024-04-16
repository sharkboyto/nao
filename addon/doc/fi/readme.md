# NAO - NVDA Advanced OCR

* Tekijät: Alessandro Albano, Davide De Carne, Simone Dal Maso
* Lataa [vakaa versio][1]
* Yhteensopivuus: NVDA 2019.3 ja uudemmat

NAO (NVDA Advanced OCR) on lisäosa, joka parantaa tavanomaisia tekstintunnistustoimintoja, joita NVDA tarjoaa uusissa Windows-versioissa.
NVDA:n vakiokomento käyttää Windowsin tekstintunnistustoimintoa näytön tunnistamiseen, mutta NAO voi suorittaa tekstintunnistuksen kiintolevylle tai USB-laitteille tallennetuille tiedostoille.
Tunnista kuva- ja PDF-tiedostoja NVDA+Vaihto+R-komentoa käyttäen.
Siirrä kohdistus haluamasi tiedoston kohdalle ja paina NVDA+Vaihto+R.
Kun tiedoston tunnistus on suoritettu, näkyviin tulee yksinkertainen teksti-ikkuna, joka mahdollistaa koko sisällön lukemisen, tallentamisen, tekstin etsimisen tai sisällön kopioimisen leikepöydälle.
NAO voi  käsitellä myös monisivuisia PDF-tiedostoja, joten jos sinulla on saavuttamaton asiakirja, Windowsin tekstintunnistus voi tehdä siitä saavutettavan.

## Järjestelmävaatimukset
Lisäosa toimii Windows 10- ja Windows 11 -järjestelmissä, koska niissä on sisäänrakennettu tekstintunnistusominaisuus.
NAO on yhteensopiva NVDA 2019.3:n ja sitä uudempien kanssa, joten älä käytä vanhempia versioita.
Huom: NAO toimii Windowsin resurssienhallinnassa, työpöydällä, Total Commanderissa tai xplorer²-tiedostonhallinnassa. Älä käytä muita ohjelmistoja kuten 7-Zipiä tai WinRARia, koska niitä ei tueta.

## Ominaisuudet ja komennot
* NVDA+Vaihto+R: tunnista kaikenlaiset kuva- ja PDF-tiedostot.
* Page up / Page down: siirrä kohdistin monisivuisen dokumentin todellisten sivujen välillä.
* Ctrl+S: tallenna dokumentti NAO-asiakirjamuodossa. Voit avata sen uudelleen NVDA+Vaihto+R-näppäinkomentoa käyttäen.
* P: ilmoita sivunumero monisivuisessa dokumentissa suhteessa kohdistimen sijaintiin.
* L: ilmoita rivinumero kohdistimen sijainnissa suhteessa nykyiseen sivuun.
* Vaihto+L: ilmoita rivinumero kohdistimen sijainnissa suhteessa koko dokumenttiin.
* G: siirry suoraan tietylle sivulle.
* C: kopioi koko dokumentin teksti leikepöydälle.
* S: tallenna dokumentin kopio tekstimuodossa.
* F: etsi tekstiä ja lue muutama sana ennen ja jälkeen löytyneen merkkijonon.
* NVDA+Vaihto+Ctrl+R: ota koko näytön kuvakaappaus ja tunnista se.
* Huom: Voit käyttää tavallisia NVDA-komentoja ikkunan tutkimiseen ja siirtääksesi kohdistuksen haluamaasi elementtiin. Voit esimerkiksi liikkua nuolinäppäimillä ja painaa Enteriä painikkeen painamiseksi. Voit myös siirtää hiiren senhetkiseen sijaintiisi NVDA+Laskinnäppäimistön / -näppäinkomennolla ja napsauttaa sitten vasemmalla/oikealla näppäimellä.
* NVDA+Vaihto+Ctrl+W: ota kuvakaappaus senhetkisestä ikkunasta ja tunnista se (voit käyttää samoja navigointikomentoja kuin koko näytön ruutukaappausta otettaessa).

Huom: Voit mukauttaa NAO:n näppäinkomentoja helposti NVDA:n Näppäinkomennot-valintaikkunasta. Avaa NVDA-valikko, siirry Asetukset-alivalikkoon ja valitse sieltä Näppäinkomennot-kohta. Muista, että tämä ominaisuus ei ole järjestelmänlaajuinen, vaan se toimii vain siellä, missä NAO voi suorittaa tekstintunnistuksen. Toisin sanoen näppäinkomennot näkyvät vain, jos olet työpöydällä, resurssienhallinnassa, Total Commanderissa tai Xplorerissa.

Voit myös keskeyttää kauan kestävän tekstintunnistusprosessin painamalla Peruuta-painiketta tunnistuksen etenemisen ikkunassa. Tämä ikkuna antaa tietoa tekstintunnistuksen tilasta päivittäen tiedot 5 sekunnin välein. Voit määrittää edistymispalkin tilan ilmoittamista tavalliseen tapaan NVDA+U-näppäinkomennolla.

NVDA-valikon Työkalut-alivalikosta löytyy NAO-kohta. Tällä hetkellä se sisältää vain kohdan, joka mahdollistaa lahjoituksen tekemisen, mutta lisäämme siihen uusia ominaisuuksia tulevaisuudessa.

## Tuki ja lahjoitukset
NAO on täysin ilmainen. Muista kuitenkin, että se on tehty kehittäjien vapaa-ajalla.
Arvostaisimme mitä tahansa tukea, jota voit meille antaa.
<a href="https://nvda-nao.org/donate">Harkitse lahjoittamista</a>, jos työmme on mielestäsi hyvää ja parantaa elämääsi.

Haluatko ilmoittaa bugista, ehdottaa uusia ominaisuuksia tai kääntää lisäosan omalle kielellesi? Meillä on sähköpostiosoite sinua varten. Kirjoita osoitteeseen support@nvda-nao.org, niin autamme mielellämme.

## Versiohistoria

### 2023.1.1
* Palautettu NVDA 2023.3:n yhteensopivuus
* Uusi NVDA+Ctrl+Vaihto+W-näppäinkomento ottaa kuvakaappauksen senhetkisestä ikkunasta ja tunnistaa sen
* Lisätty brasilianportugalilainen käännös
* Tietoturvakorjaus suojatuissa ruuduissa
* NAO-työkaluvalikko poistettu suojatuissa ruuduissa
* Dokumenttien välimuisti poistettu suojatuissa ruuduissa
* NAO:n verkkosivun ja Git-koodivaraston linkit lisätty NAO-työkaluvalikkoon

### 2023.1
* Yhteensopivuus NVDA 2023.1:lle

### 2022.1.3
* Yhteensopivuus NVDA 2022.1:lle
* Päivitetty yksinkertaistetun kiinan ja ranskankieliset käännökset
* Espanjankielinen dokumentaatio päivitetty

### 2022.1.2
* NAO-dokumenttimuodon tallennus- ja latausominaisuus.
* Tunnistuksen tulokset voidaan tallentaa dokumenttivälimuistiin, joka nopeuttaa niiden avaamista seuraavalla kerralla. Jos tiedosto löytyy välimuistista, sitä ei tunnisteta uudelleen, vaan käytetään sen sijaan välimuistissa olevaa versiota (tunnistusparametrien on oltava täsmälleen samat).
* Dokumentin viimeisin lukukohta tallennetaan välimuistin metatietoihin.
* Dokumenttivälimuistin automaattinen tyhjennys.
* Manuaalinen välimuistin tyhjennysvaihtoehto Työkalut-valikossa.
* Tiedosto voidaan nyt tunnistaa suoraan "pakatusta kansiosta" Windowsin resurssienhallinnassa.
* Parempi virheellisten tiedostojen tarkistus.
* Parempi Windowsin resurssienhallinnan yhteensopivuus erilaisia tiedostonvalintavaihtoehtoja käyttäen: ensin yritetään Shell.Application-menetelmää NVDA:ssa, sitten samaa menetelmää PowerShellissä ja viimeisenä turvaudutaan manuaaliseen selaamiseen.
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
* Pitkäkestoinen tekstintunnistusprosessi voidaan keskeyttää painamalla Tunnistuksen edistymisikkunassa "Peruuta"-painiketta.
* Lisätty turkin-, venäjän-, espanjan-, kiinan- ja ranskankieliset käännökset.
* Käyttäjien on mahdollista tehdä projektille lahjoituksia.
* Korjattu bugi, jossa tietyt merkit tiedostonimessä estivät tekstintunnistusta toimimasta kunnolla.

### 2021.1
* Ensimmäinen julkinen versio.


[1]: https://nvda-nao.org/download
