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
  * P: lee el número de página relativo a la posición del cursor, en un documento de varias páginas.
  * l: Lee el número de línea relativo con la posición del cursor, en un documento de varias páginas.
  * c: copia todo el texto al portapapeles.
  * s: guarda una copia del documento en un formato de texto.
  * f: busca texto y lee algunas palabras antes y después de la cadena.
* NVDA + Shift + Ctrl + R: Toma una captura de pantalla de toda la pantalla y la reconoce.
  * Ten en cuenta que puedes usar comandos estándar de NVDA para explorar la ventana y enfocar un elemento. Por ejemplo, puedes moverte con las teclas de flecha y presionar enter en un botón para activarlo. También puedes llevar el mouse a su posición con la barra del teclado numérico de NVDA y luego hacer clic con las teclas izquierda/derecha.

Ten en cuenta que puedes personalizar los accesos directos de Nao simplemente desde el cuadro de diálogo de gestos de entrada de NVDA. Abre el menú de NVDA, vé a las preferencias y, desde ese submenú, selecciona la opción gestos de entrada. Recuerda que esta característica no es global, pero funciona solo donde Nao puede hacer un OCR. Entonces, los gestos aparecerán solo si está en el escritorio, o en el explorador de archivos, Total Commander o Xplorer.

También puedes cancelar un proceso largo de OCR simplemente presionando "Cancelar" desde la ventana de la barra de progreso; esta ventana también brinda información sobre el estado del OCR, actualizando la información cada 5 segundos. Puede configurar cómo recibir información de la barra de progreso con el comando estándar de NVDA-u.

Puedes encontrar un submenú llamado Nao, bajo el menú de herramientas de NVDA. Por el momento, solo contiene un elemento que te permite hacer una donación, ¡pero lo mejoraremos con nuevas funciones!

## Apoyo y donaciones
Nao es absolutamente gratuito. De todos modos, recuerda que este complemento se realiza durante el tiempo libre de los desarrolladores.
¡Agradeceríamos cualquier contribución que nos pudieras dar!
Si cree que nuestro trabajo es bueno y mejora su vida, a <a href="https://nvda-nao.org/donate">Considere hacer una donación.</a>.

¿Quieres informar de un error, sugerir nuevas funciones, traducir el complemento a tu idioma? ¡Tenemos el correo electrónico para ti! Simplemente escribe a support@nvda-nao.org y estaremos encantados de ayudarte.

## Historial
### 2021.2
* El OCR de pdf e imágenes se presentan en una nueva ventana de texto, con algunas teclas de acceso rápido para operaciones simples.
* Soporte para el administrador de archivos Xplorer.
* Los atajos de Nao se pueden personalizar desde el Diálogo de gestos de entrada de NVDA.
* Nao solo funciona cuando es posible, por lo que si se encuentra en una ventana no admitida, el complemento ignorará la tecla de acceso rápido; esto resolvió un problema importante en el que los usuarios de Excel y Word no podían presionar la tecla NVDA-Shift-r, ya que Nao la interceptó incorrectamente.
* Un proceso largo de OCR se puede cancelar simplemente presionando el botón "Cancelar" en la ventana de la barra de progreso.
* Añadidas traducciones al turco, ruso, español, chino y francés.
* Los usuarios pueden realizar donaciones al proyecto.
* Se corrigió un error con algunos caracteres en el nombre del archivo que impedía que OCR funcione correctamente.
### 2021.1
* primera versión pública!


[1]: https://nvda-nao.org/download
