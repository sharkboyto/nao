# Nao - NVDA Advanced OCR

* Autori: Alessandro Albano, Davide De Carne, Simone Dal Maso
* Download [versione stabile][1]
* Compatibilità NVDA: 2021.2 e successive

Nao (NVDA Advanced OCR) è un addon che migliora le capacità OCR standard fornite da NVDA nelle versioni moderne di Windows.
Mentre il comando standard NVDA utilizza l'OCR di Windows per riconoscere lo schermo, NAO è in grado di eseguire l'OCR sui file salvati sul disco rigido o sui dispositivi USB.
Usa NVDA-Shift-R per riconoscere qualsiasi tipo di immagine e pdf!
Porta semplicemente il focus / cursore sul file che desideri, non aprirlo, ma premi NVDA-Shift-r.
Il documento verrà riconosciuto e apparirà una semplice casella di testo, che consentirà di leggere l'intero contenuto, salvarlo, copiarlo negli appunti o cercare del testo.
Nao è in grado di gestire anche pdf multipagina, quindi se hai un documento non accessibile, non preoccuparti, l'OCR di Windows sarà in grado di fare tutto il lavoro.

## Requisiti di sistema
L'addon lavora soltanto sui sistemi Windows 10 e Windows 11, poiché dispongono di funzionalità OCR integrate.
Nao è compatibile dalla versione NVDA 2021.2, quindi non utilizzare versioni precedenti dello screen reader.
Si noti che Nao funziona con Windows Explorer, sul desktop, con il file manager Total Commander o Xplorer; non utilizzare altri software come 7zip o Winrar, poiché non sono supportati.

## Funzionalità e comandi
* NVDA + Shift + R: riconosce qualsiasi tipo di immagine e pdf dal file system;
  * PgUp / PgDown: sposta il cursore tra le pagine reali di un documento multipagina.
  * p: legge il numero di pagina relativo alla posizione del cursore, in un documento multipagina.
  * l: legge il numero di riga relativo alla posizione del cursore, in un documento multipagina.
  * c: copia l'intero documento negli appunti.
  * s: Salva una copia del documento in formato testo.
  * f: trova il testo e legge alcune parole prima e dopo la stringa.
* NVDA + Shift + Ctrl + R: Effettua lo screenshot dell'intera videata e la riconosce.
* Si tenga presente che è possibile utilizzare i comandi standard di NVDA per esplorare la finestra e portare il focus su un elemento. Ad esempio ci si può spostare con i tasti freccia e premere invio in un pulsante per attivarlo. Inoltre si può anche portare il mouse in quella posizione premendo la combinazione NVDA+barra del tastierino numerico e quindi fare clic con i tasti sinistro/destro.

Inoltre, si possono personalizzare le scorciatoie di Nao semplicemente dalla finestra di dialogo Tasti e gesti di immissione di NVDA. Aprire il menu NVDA, andare su preferenze e da quel sottomenu selezionare la finestra di dialogo tasti e gesti di immissione. La cosa importante da tenere a mente è che questi gesti non sono globali; essi appariranno soltanto se ci si trova in un ambiente in cui Nao può funzionare: desktop, Esplora file, Total Commander o Xplorer.

È possibile anche interrompere un processo di Ocr molto lungo semplicemente premendo "Annulla" dalla finestra della barra di avanzamento; questa finestra fornisce anche informazioni sullo stato dell'OCR, aggiornando l'utente ogni 5 secondi. È possibile configurare la modalità con cui si desidera ricevere messaggi informativi sulla barra di avanzamento con il comando standard NVDA-u.

È stato aggiunto un sottomenu chiamato "Nao" al menu strumenti di NVDA. Per adesso consente di effettuare una donazione al progetto, ma verrà arricchito in futuro con nuove funzionalità!

## Supporto e donazioni
Nao è completamente gratuito. Ad ogni modo, è bene non dimenticare che questo addon viene realizzato durante il tempo libero degli sviluppatori.
Apprezzeremmo qualsiasi contributo tu potessi darci!
Se pensi che il nostro lavoro sia buono e migliori la tua vita, a <a href="https://nvda-nao.org/donate">Considera di effettuare una donazione.</a>

Vuoi segnalare un bug, suggerire nuove funzionalità, tradurre l'addon nella tua lingua? Abbiamo l'e-mail per te! Scrivi a support@nvda-nao.org e saremo felici di aiutarti.

## Cronologia
### 2022.1
* Update automatico dell'addon.
* Aggiornate traduzioni in spagnolo e francese.
### 2021.2
* L'OCR di pdf e immagini viene presentato in una nuova finestra di testo, con alcuni tasti di scelta rapida per semplici operazioni.
* Supporto per il gestore di file Xplorer.
* Le scorciatoie Nao sono personalizzabili dalla finestra di dialogo Input Gestures di NVDA.
* Nao funziona solo dove possibile, quindi se ti trovi in una finestra non supportata, il tasto di scelta rapida verrà ignorato dall'addon; questo ha risolto un problema importante per cui gli utenti di Excel e Word non potevano premere il tasto NVDA-Shift-r, poiché veniva erroneamente intercettato da Nao.
* Un lungo processo Ocr può essere interrotto semplicemente premendo il pulsante "Annulla" nella finestra della barra di avanzamento.
* Aggiunte traduzioni in turco, russo, spagnolo, cinese e francese.
* Gli utenti possono effettuare donazioni al progetto.
* Risolto un bug con alcuni caratteri sui nomi dei file che impediva all'Ocr di funzionare correttamente.
### 2021.1
* Prima versione pubblica! 


[1]: https://nvda-nao.org/download
