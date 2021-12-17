 # Nao - NVDA Advanced OCR

* Authors: Alessandro Albano, Davide De Carne, Simone Dal Maso
* Download [stable version][1]
* NVDA compatibility: 2021.2 and beyond

Nao (NVDA Advanced OCR) is an addon that improves the standard OCR capabilities that NVDA provides on modern Windows versions.
While NVDA standard command uses Windows OCR to recognize the screen, NAO is able to make the OCR on files saved on your hard drive or USB devices. 
Use NVDA-Shift-R to recognize any sorts of images and pdf! 
Simply put the focus / cursor on the file you desire, don't open it, but hit NVDA-Shift-r. 
The document will be recognized and a simple text window will appear, allowing you to read the entire content, save it, find text or copy content to clipboard.
Nao is able to handle also multipage pdf, so if you have a not accessible document, don't worry, Windows OCR will be able to make the entire work.

## System Requirements
The addon works on Windows 10 and Windows 11 systems, since they have OCR capabilities builtin. 
Nao is compatible from NVDA version 2021.2, so don't use older versions of the screen reader.
Note that Nao works with Windows Explorer, on desktop, with Total Commander or xplorer² filemanager; don't use other software like 7zip or Winrar, since they are not supported.

## Features and commands
* NVDA + Shift + R: recognize any sorts of images and pdf from file system;
  * PgUp / PgDown: move the cursor between real pages of a multipages document.
  * P: report page number related to the cursor position, in a multipage document.
  * l: report line number related to the cursor position, in a multipage document.
  * c: copy all text to the clipboard.
  * s: Save a copy of the document in text format. 
* NVDA + Shift + Ctrl + R: take a full screen shot and recognize it.
  * Please note that you can use standard NVDA commands to explore window and bring focus to an element. For example you can move with arrow keys and press enter in a button to activate it. You can also bring the mouse to your position with NVDA-numpad slash and then click with left/right keys.

## Support and donations
Nao is absolutely free. Anyway, please remember that this addon is made during spare time of developers. 
We'd appreciate any contribute that you could give us!
If you think our work is good and improve your life, a <a href="http://nvda-nao.org/">Consider to make a donation.</a>

## History
### 2021.8
* OCR of pdf and images are presented in a new text window, with some hotkeys for simple operations.
* Support for the Xplorer filemanager.
* Added Turkish, Russian, Spanish, Chinese and french translations.
* Users can make donations to the project.
* Fixed a bug with some characters on the file extensions that prevents the Ocr to work properly.
### 2021.7
* first public version! 


[1]: https://github.com/sharkboyto/nao/releases/download/v_2021.1.07/nao-2021.1.07.nvda-addon
