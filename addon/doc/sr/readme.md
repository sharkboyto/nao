# Nao - NVDA napredni OCR

* Autori: Alessandro Albano, Davide De Carne, Simone Dal Maso
* Preuzmi [stabilnu verziju][1]
* NVDA kompatibilnost: 2019.3  i noviji

Nao (NVDA napredni OCR) je dodatak koji poboljšava standardne OCR sposobnosti koje NVDA pruža na modernim Windows verzijama.
Iako NVDA standardna komanda za OCR prepoznaje ekran, NAO može da izvrši OCR na datotekama koje su sačuvane na vašem disku ili USB uređajima, 
Koristite NVDA-šift-R da biste prepoznali bilo koju sliku i pdf! 
Jednostavno se fokusirajte ili stanite kursorom na željenu datoteku, ne otvarajte je, već pritisnite NVDA-šift-r. 
Dokument će biti prepoznat i pojaviće se jednostavan prozor sa tekstom, koji vam dozvoljava da pročitate sadržaj, sačuvate ga, pretražite tekst ili kopirate sadržaj u privremenu memoriju.
Nao takođe može da obradi PDF dokumente sa više stranica, pa ako imate dokument koji nije pristupačan, ne brinite, Windows OCR će odraditi posao.

## Sistemski zahtevi
Dodatak radi na sistemima Windows 10 i Windows 11, budući da oni imaju ugrađene OCR mogućnosti. 
Nao je kompatibilan od NVDA verzije 2019.3, pa nemojte koristiti starije verzije čitača ekrana.
Imajte na umu da Nao radi sa Windows istraživačem datoteka, na radnoj površini, sa Total Commanderom ili xplorerom² upravljačem datoteka; ne koristite druge programe kao što su 7zip ili Winrar, budući da oni nisu podržani.
For e-mail attachments, it also works with Microsoft Outlook 2016 or beyond.

## Karakteristike i komande
* NVDA + šift + R: Prepoznaje bilo koje slike i pdf datoteke u sistemu;
  * PageUp / PageDown: Pomera kursor između pravih stranica u dokumentu sa više stranica.
  * Ctrl + S: Čuva dokument u nao-document formatu. Možete ga ponovo otvoriti prečicom NVDA + šift + R.
  * P: Prijavljuje broj stranice na poziciji kursora, u dokumentu sa više stranica.
  * L: Prijavljuje broj reda na poziciji kursora, na trenutnoj stranici.
  * Šift + L: Prijavljuje broj reda na poziciji kursora, u celom dokumentu.
  * G: Direktno prelazi na određenu stranicu.
  * C: Kopira ceo tekst u privremenu memoriju.
  * S: Čuva kopiju dokumenta u tekstualnom formatu.
  * F: Pronalazi tekst i čita nekoliko reči pre i nakon pojma za pretragu.
* NVDA + šift + Ctrl + R: Slika ceo ekran i prepoznaje sliku.
  * Molimo imajte na umu da možete koristiti standardne NVDA komande da istražite prozor i da se fokusirate na neki element. Na primer možete se kretati strelicama i pritisnuti enter na dugmetu da biste ga aktivirali. Možete takođe prebaciti miš na vašu poziciju komandom NVDA-numerički taster podeljeno a zatim izvršiti levi ili desni klik.
* NVDA + šift + Ctrl + W: Slika trenutni prozor i prepoznaje sliku (iste funkcije za navigaciju kao i sa funkcijom slikanja celog ekrana).

Imajte na umu da možete da prilagodite Nao prečice jednostavno iz dijaloga ulaznih komandi programa NVDA. Otvorite NVDA meni, uđite u opcije, i iz tog podmenija izaberite ulazne komande. Zapamtite da ove funkcije nisu globalne, već rade samo tamo gde NAO može da izvrši OCR. To znači da će se komande pojaviti samo ako ste na radnoj površini, ili u istraživaču datoteka, Total Commanderu ili Xploreru.

Možete takođe otkazati dugotrajni OCR proces tako što ćete pritisnuti dugme "Otkaži" u prozoru sa trakom napredovanja; Ovaj prozor vam takođe daje informacije o stanju za OCR, a te informacije se ažuriraju svakih 5 sekundi. Možete da podesite kako ćete primati informacije o traci napredovanja standardnom komandom NVDA-u.

Možete pronaći podmeni koji se zove Nao, u NVDA meniju alati. It contains following items:
* Select file: allow you to select a file for processing without using a shortkey.
* Make a donation: it's self-explanatory, if you feel like it we'll be very happy!
* Nao Website: brings you to the homepage of Nao.
* Git: brings you to the source codeò where you can check it, make commit or open an issue.
* Check for updates: queries the server for a new version of Nao.
* Empty cache: If you encounter problems with the add-on, receive error messages or find it slow, clear your cache to resolve the issue.

## Podrška i donacije
Nao je u potpunosti besplatan. U svakom slučaju, imajte na umu da se dodatak razvija u slobodno vreme programera. 
Zahvalni smo na svakoj saradnji!
Ako mislite da radimo dobar posao i poboljšavamo vaš život, a <a href="https://nvda-nao.org/donate">razmotrite mogućnost doniranja.</a>

Da li želite da prijavite grešku, predložite nove funkcije, prevedete dodatak na vaš jezik? Imamo  e-mail za vas! Pišite nam na support@nvda-nao.org i biće nam zadovoljstvo da vam pomognemo.

## Istorija
### 2025.1
* NVDA version 2025.1 compatibility
* Implement OCR recognition on the selected attachment of an opened Outlook message, from outlook 2016 and beyond
* Added finnish translation
### 2024.1
* NVDA version 2024.1 compatibility
### 2023.1.1
* Vraćena kompatibilnost sa NVDA verzijom 2023.3
* Nova prečica NVDA + Ctrl + šift + W slika ceo trenutni prozor i prepoznaje ga
* Dodat prevod na Portugalski (Brazil)
* Bezbednosna ispravka na bezbednim ekranima
* NAO meni sa alatima uklonjen na bezbednim ekranima
* Keš dokumenata uklonjen na bezbednim ekranima
* NAO websajt i link za Git repozitorijum dodati u meni sa NAO alatima

### 2023.1
* Kompatibilnost za NVDA verziju 2023.1

### 2022.1.3
* Kompatibilnost za NVDA verziju 2022.1
* Ažurirani prevodi za pojednostavljeni kineski i francuski
* Španska dokumentacija ažurirana

### 2022.1.2
* Mogućnost čuvanja i učitavanja nao-document formata datoteka.
* Keš dokumenata može da čuva prepoznavanja kako bi ubrzao otvaranje sledeći put. Ako je datoteka pronađena u kešu ne prepoznaje se ponovo već se umesto toga otvara keširana verzija (podešavanja prepoznavanja se moraju podudarati).
* Čuvanje poslednje pozicije čitanja dokumenta u podacima keša.
* Automatsko brisanje za keš dokumenata.
* Ručno brisanje keša u meniju sa alatima.
* Datoteka se sada može direktno prepoznati iz komprimovanog foldera u Windows istraživaču datoteka.
* Bolja provera neispravnih datoteka.
* Bolja kompatibilnost sa Windows istraživačem datoteka korišćenjem različitih alternativa za izbor datoteka: Prvo se pokušava uz Shell.Application u programu NVDA, zatim se pokušava Shell.Application u PowerShellu a zatim se vraća na ručno istraživanje.
* OCR mogućnost čuva podešavanje jezika u toku celog procesa prepoznavanja čak i ako se promeni u toku prepoznavanja dokumenta sa više stranica.
* OCR u isto vreme može prepoznavati iz više izvora.
* Prečica PageDown na poslednjoj stranici dokumenta ide na kraj dokumenta i prijavljuje broj reda.
* Windows privremeni folder se koristi za alate za pretvaranje datoteka umesto foldera dodatka  (poboljšanja u brzini za prenosni NVDA).
* Rumunski prevod i ažuriran prevod za pojednostavljeni kineski.

### 2022.1.1
* Podrška za DjVu format datoteka.
* Podrška za tiff datoteke sa više stranica.
* PDF ispravka za kodiranje datoteka na operativnim sistemima na kineskom.
* Ručno ažuriranje dodatka u NVDA meniju alati.
* Kompatibilnost od NVDA verzije 2019.3.

### 2022.1
* Automatsko ažuriranje dodatka.
* Španski i Francuski prevodi ažurirani.

### 2021.2
* OCR pdf datoteka i slika se prikazuje u novom tekstualnom prozoru, sa nekim prečicama za jednostavne radnje.
* Podrška za Xplorer upravljač datotekama.
* Nao prečice se mogu prilagoditi iz NVDA dijaloga ulaznih komandi.
* Nao radi samo kada je moguće, pa ako ste u prozoru koji nije podržan, dodatak će ignorisati prečice; ovo je rešilo bitan problem koji je izazivao da Excel i Word korisnici ne  mogu da pritisnu  prečicu NVDA-šift-r, budući da ju je dodatak neispravno preuzimao.
* Dugotrajan Ocr proces se može otkazati jednostavnim pritiskom na dugme "Otkaži" u prozoru trake napredovanja.
* Dodati turski, ruski, španski, kineski i francuski prevodi.
* Korisnici mogu donirati za razvoj projekta.
* Ispravljena greška sa nekim znakovima u imenu datoteke koji su sprečavali da OCR ispravno radi.
### 2021.1
* Prva javna verzija! 


[1]: https://nvda-nao.org/download
