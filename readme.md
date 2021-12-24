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
  * f: find text and read some words before and after the string.
* NVDA + Shift + Ctrl + R: take a full screen shot and recognize it.
  * Please note that you can use standard NVDA commands to explore window and bring focus to an element. For example you can move with arrow keys and press enter in a button to activate it. You can also bring the mouse to your position with NVDA-numpad slash and then click with left/right keys.
Note that you can customize shortcuts of Nao simply from the input gestures dialog of NVDA. Open NVDA menu, go to preferences, and from that submenu select input gestures dialog. Remember that this feature is not global, but it works only where Nao can make an ocr. So gestures will appear only if you are in the desktop, or in file explorer, Total Commander or Xplorer. You can assign different gestures for each app.
You can also abort a long Ocr process simply pressing "Cancel" from the progress bar window; this window also gives you information about the state of the OCR, updating informations every 5 seconds. You can configure how to receive progress bar information with the standard NVDA-u command.
You can find a submenu named Nao, under the NVDA - Tools - menu. For the moment it contains only an item that allow you to make a donation, but we will improve that with new features!

## Support and donations
Nao is absolutely free. Anyway, please remember that this addon is made during spare time of developers. 
We'd appreciate any contribute that you could give us!
If you think our work is good and improve your life, a <a href="http://nvda-nao.org/donate">Consider to make a donation.</a>
Do you want to report a bug, suggest new features, translate the addon in your language? We have the email for you! Just write to support@nvda-nao.org and we will be happy to help you.

## History
### 2021.2
* OCR of pdf and images are presented in a new text window, with some hotkeys for simple operations.
* Support for the Xplorer filemanager.
* Nao shortcuts are customizable from the Input Gestures Dialog of NVDA.
* Nao works only where possible, so if you are in a not supported window, the hotkey will be ignored by the addon; this solved an important issue where Excel and Word users couldn't press the NVDA-Shift-r keystroke, since it was incorrectly intercepted by Nao.
* A long Ocr process can be aborted simply pressing the "Cancel" button on the progress bar window.
* Added Turkish, Russian, Spanish, Chinese and french translations.
* Users can make donations to the project.
* Fixed a bug with some characters on the file extensions that prevents the Ocr to work properly.
### 2021.1
* first public version! 


[1]: https://nvda-nao.org/download
