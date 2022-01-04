# Nao - NVDA Advanced OCR

* Auteurs : Alessandro Albano, Davide De Carne, Simone Dal Maso
* Télécharger [version stable][1]
* Compatibilité NVDA : 2019.3 et ultérieure

Nao (NVDA Advanced OCR) est une extension qui améliore les capacités OCR standard fournies par NVDA sur les versions modernes de Windows.
Alors que la commande standard de NVDA utilise l'OCR Windows pour reconnaître l'écran, NAO est capable d'effectuer l'OCR sur les fichiers enregistrés sur votre disque dur ou vos périphériques USB. 
Utilisez NVDA-Shift-R pour reconnaître toutes sortes d'images et de PDF ! 
Placez simplement le focus/curseur sur le fichier que vous désirez, ne l'ouvrez pas, mais appuyez sur NVDA-Shift-r. 
Le document sera reconnu et une simple fenêtre de texte apparaîtra, vous permettant de lire tout le contenu, de l'enregistrer, de rechercher du texte ou de copier du contenu dans le presse-papiers.
Nao est capable de gérer également des pdf multipages, donc si vous avez un document inaccessible, ne vous inquiétez pas, Windows OCR pourra faire tout le travail.

## Configuration requise
L'extension fonctionne sur les systèmes Windows 10 et Windows 11, car ils ont des capacités OCR intégrées. 
Nao est compatible à partir de la version 2019.3 de NVDA, donc n'utilisez pas une version plus ancienne du lecteur d'écran.
Veuillez noter que Nao fonctionne avec l'explorateur Windows, sur le bureau ou avec les gestionnaires de fichiers Total Commander ou xplorer² ; n'utilisez pas d'autres logiciels comme 7zip ou Winrar , car ils ne sont pas pris en charge.

## Fonctionnalités et commandes
* NVDA + Shift + R : reconnaît toutes sortes d'images et de pdf à partir du système de fichiers ;
  * PgPréc / PgSuiv: déplace le curseur entre les pages réelles d'un document multipages.
  * P : annonce le numéro de page à la position du curseur, dans un document multipage.
  * l : annonce le numéro de ligne à la position du curseur, dans un document multipage.
  * c : copie tout le texte dans le presse-papiers.
  * s : enregistre une copie du document au format texte.
  * f : recherche du texte et lit quelques mots avant et après la chaîne recherchée.
* NVDA + Maj + Ctrl + R : Prend une capture de la totalité de l'écran et la reconnaît.
  * Veuillez noter que vous pouvez utiliser les commandes NVDA standard pour explorer la fenêtre et mettre le focus sur un élément. Par exemple, vous pouvez vous déplacer avec les touches fléchées et appuyer sur Entrée sur un bouton pour l'activer. Vous pouvez également amener la souris à votre position avec NVDA + PavNum/, puis cliquer avec les touches gauche/droite.

Veuillez noter que vous pouvez personnaliser les raccourcis de Nao simplement à partir de la boîte de dialogue des gestes de commande de NVDA. Ouvrez le menu NVDA, allez dans les préférences, et à partir de ce sous-menu, sélectionnez la boîte de dialogue des gestes de commande. N'oubliez pas que cette fonctionnalité n'est pas globale, mais qu'elle ne fonctionne que là où Nao peut faire une reconnaissance de caractères. Ainsi, les gestes n'apparaîtront que si vous êtes sur le bureau, ou dans l'explorateur de fichiers, Total Commander ou Xplorer.

Vous pouvez également interrompre un long processus OCR en appuyant simplement sur « Annuler » dans la fenêtre de la barre de progression ; cette fenêtre vous donne également des informations sur l'état de l'OCR, en mettant à jour les informations toutes les 5 secondes. Vous pouvez configurer comment recevoir les informations de la barre de progression avec la commande NVDA-u standard.

Vous trouverez un sous-menu nommé Nao, sous le menu NVDA - Outils. Pour le moment, il ne contient qu'un élément qui vous permet de faire un don, mais nous allons améliorer cela avec de nouvelles fonctionnalités !

## Soutien et dons
Nao est absolument gratuit. Cependant, n'oubliez pas que cette extension est faite durant le temps libre des développeurs.
Nous apprécierions toute contribution que vous pourriez nous apporter !
Si vous pensez que notre travail est bon et qu'il améliore votre vie, <a href="https://nvda-nao.org/donate">Envisagez de faire un don.</a>

Vous souhaitez signaler un bug, proposer de nouvelles fonctionnalités, traduire l'extension dans votre langue ? Nous avons l'adresse e-mail qu'il vous faut ! Écrivez simplement à support@nvda-nao.org (a priori en anglais ou italien) et nous serons heureux de vous aider.

## Historique
### 2021.2
* L'OCR de pdf et des images sont présentés dans une nouvelle fenêtre de texte, avec quelques raccourcis clavier pour des opérations simples.
* Prise en charge du gestionnaire de fichiers Xplorer.
* Les raccourcis Nao sont personnalisables à partir de la boîte de dialogue Gestes d'entrée de NVDA.
* Nao ne fonctionne que là où c'est possible, donc si vous êtes dans une fenêtre non prise en charge, le raccourci clavier sera ignoré par l'extension ; cela a résolu un problème important où les utilisateurs d'Excel et de Word ne pouvaient pas appuyer sur la touche NVDA-Shift-r, car elle était incorrectement interceptée par Nao.
* Un long processus OCR peut être interrompu en appuyant simplement sur le bouton « Annuler » dans la fenêtre de la barre de progression.
* Ajout de traductions en turc, russe, espagnol, chinois et français.
* Les utilisateurs peuvent faire des dons au projet.
* Correction d'un bug avec certains caractères dans le nom du fichier qui empêchait l'OCR de fonctionner correctement.
### 2021.1
* Première version publique !


[1]: https://nvda-nao.org/download
