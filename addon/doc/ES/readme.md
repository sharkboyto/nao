# Nao - NVDA Advanced OCR

* Autores: Alessandro Albano, Davide De Carne, Simone Dal Maso
* Descargar [versión estable][1]
* Compatibilidad con NVDA: 2021.2 y posterior

NAO (NVDA Advanced OCR) es un complemento que mejora las funciones estándar de OCR proporcionadas por NVDA en versiones modernas de Windows.
Mientras que la orden estándar de NVDA usa el OCR de Windows para reconocer la pantalla, NAO es capaz de aplicar el OCR en archivos guardados en tu disco duro o dispositivo USB.
¡Usa NVDA+shift+r para reconocer cualquier tipo de imagen o PDF!
Simplemente posiciona el cursor sobre el archivo que desees, y sin abrirlo, pulsa NVDA+shift+r
Se reconocerá el documento y aparecerá un cuadro de texto simple que te permitirá leer todo el contenido.
NAO también es capaz de manejar documentos PDF de varias páginas, por lo que si tienes un documento inaccesible, no te preocupes: el OCR de Windows se encargará de hacer todo el trabajo.

## Requisitos del sistema
El complemento solo funciona en sistemas Windows 10 y Windows 11, ya que tienen capacidades de OCR integradas.
Nao es compatible con la versión 2021.2 de NVDA, por lo tanto, no funcionará en versiones anteriores del lector de pantalla
Ten en cuenta que NAO funciona con el explorador de Windows, en el escritorio, o con el gestor de archivos Total Commander; no uses otro software como 7-zip o WinRar, ya que no se soportan.

## Funciones y comandos
* NVDA + Shift + R: reconoce cualquier tipo de imagen y pdf desde el sistema de archivos;
  * Avance / Retroceso de página: mueve el cursor entre las páginas reales de un documento de varias páginas.
  * NVDA + Shift + P: lee el número de página relativo a la posición del cursor, en un documento de varias páginas.
* NVDA + Shift + Ctrl + R: Toma una captura de pantalla de toda la pantalla y la reconoce.

[1]: https://github.com/sharkboyto/nao/releases/download/v_2021.1.07/nao-2021.1.07.nvda-addon