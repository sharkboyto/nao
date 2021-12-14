# Nao - NVDA Advanced OCR

* Autori: Alessandro Albano, Davide Decarne, Simone Dal Maso
* Download [versione stabile][1]
* Compatibilità NVDA: 2021.2 e successive

Nao (NVDA Advanced OCR) è un addon che migliora le capacità OCR standard fornite da NVDA nelle versioni moderne di Windows.
Mentre il comando standard NVDA utilizza l'OCR di Windows per riconoscere lo schermo, NAO è in grado di eseguire l'OCR sui file salvati sul disco rigido o sui dispositivi USB.
Usa NVDA-Shift-R per riconoscere qualsiasi tipo di immagine e pdf!
Porta semplicemente il focus / cursore sul file che desideri, non aprirlo, ma premi NVDA-Shift-r.
Il documento verrà riconosciuto e apparirà una semplice casella di testo, che consentirà di leggere l'intero contenuto.
Nao è in grado di gestire anche pdf multipagina, quindi se hai un documento non accessibile, non preoccuparti, l'OCR di Windows sarà in grado di fare tutto il lavoro.

## Requisiti di sistema
L'addon lavora soltanto sui sistemi Windows 10 e Windows 11, poiché dispongono di funzionalità OCR integrate.
Nao è compatibile dalla versione NVDA 2021.2, quindi non utilizzare versioni precedenti dello screen reader.
Si noti che Nao funziona con Windows Explorer, sul desktop o con il file manager di Total Commander; non utilizzare altri software come 7zip o Winrar, poiché non sono supportati.

## Funzionalità e comandi
* NVDA + Shift + R: riconosce qualsiasi tipo di immagine e pdf dal file system;
  * PgUp / PgDown: sposta il cursore tra le pagine reali di un documento multipagina.
  * NVDA + Shift + P: legge il numero di pagina relativo alla posizione del cursore, in un documento multipagina.
* NVDA + Shift + Ctrl + R: Effettua lo screenshot dell'intera videata e la riconosce.

[1]: https://github.com/sharkboyto/nao/releases/download/v_2021.1.07/nao-2021.1.07.nvda-addon