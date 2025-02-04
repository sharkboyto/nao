# Nao - NVDA Advanced OCR

* Auteurs : Alessandro Albano, Davide De Carne, Simone Dal Maso
* Télécharger [version stable][1]
* Compatibilité NVDA : 2019.3 et ultérieure

Nao (NVDA Advanced OCR) est une extension qui améliore les capacités OCR standard fournies par NVDA sur les versions modernes de Windows.
Alors que la commande standard de NVDA utilise l'OCR Windows pour reconnaître l'écran, NAO est capable d'effectuer l'OCR sur les fichiers enregistrés sur votre disque dur ou vos périphériques USB, ou dans les pièces jointes Microsoft Outlook.
Utilisez NVDA-Maj-R pour reconnaître toutes sortes d'images et de PDF ! 
Placez simplement le focus/curseur sur le fichier que vous désirez, ne l'ouvrez pas, mais appuyez sur NVDA-Maj-r. 
Le document sera reconnu et une simple fenêtre de texte apparaîtra, vous permettant de lire tout le contenu, de l'enregistrer, de rechercher du texte ou de copier du contenu dans le presse-papiers.
Nao est capable de gérer également des pdf multipages, donc si vous avez un document inaccessible, ne vous inquiétez pas, Windows OCR pourra faire tout le travail.

## Configuration requise
L'extension fonctionne sur les systèmes Windows 10 et Windows 11, car ils ont des capacités OCR intégrées. 
Nao est compatible à partir de la version 2019.3 de NVDA, donc n'utilisez pas une version plus ancienne du lecteur d'écran.
Veuillez noter que Nao fonctionne avec l'explorateur Windows, sur le bureau ou avec les gestionnaires de fichiers Total Commander ou xplorer² ; n'utilisez pas d'autres logiciels comme 7zip ou Winrar, car ils ne sont pas pris en charge.
Pour les pièces jointes aux e-mails, il fonctionne également avec Microsoft Outlook 2016 ou version ultérieure.

## Fonctionnalités et commandes
* NVDA + Maj + R : reconnaît toutes sortes d'images et de pdf à partir du système de fichiers ou joints à un e-mail ;
  * PgPréc / PgSuiv : déplace le curseur entre les pages réelles d'un document multipages.
  * Ctrl + S : enregistre le document au format nao-document. Vous pouvez l'ouvrir à nouveau avec NVDA + Maj + R.
  * P : annonce le numéro de page à la position du curseur, dans un document multipage.
  * L : annonce le numéro de ligne à la position du curseur, compté sur la page courante.
  * Maj + L : annonce le numéro de ligne à la position du curseur, compté sur l'ensemble du document.
  * G : va directement sur une page déterminée.
  * C : copie tout le texte dans le presse-papiers.
  * S : enregistre une copie du document au format texte.
  * F : recherche du texte et lit quelques mots avant et après la chaîne trouvée.
* NVDA + Maj + Ctrl + R : prend une capture de la totalité de l'écran et effectue une reconnaissance.
  * Veuillez noter que vous pouvez utiliser les commandes NVDA standard pour explorer la fenêtre et mettre le focus sur un élément. Par exemple, vous pouvez vous déplacer avec les touches fléchées et appuyer sur Entrée sur un bouton pour l'activer. Vous pouvez également amener la souris à votre position avec NVDA + PavNum/, puis cliquer avec les touches gauche/droite.
* NVDA + Maj + Ctrl + W : prend une capture d'écran de la fenêtre courante et effectue une reconnaissance (mêmes fonctionnalités de navigation que la fonction de capture de la totalité de l'écran).

Veuillez noter que vous pouvez personnaliser les raccourcis de Nao simplement à partir de la boîte de dialogue des gestes de commande de NVDA. Ouvrez le menu NVDA, allez dans les préférences, et à partir de ce sous-menu, sélectionnez la boîte de dialogue des gestes de commande. N'oubliez pas que cette fonctionnalité n'est pas globale, mais qu'elle ne fonctionne que là où Nao peut faire une reconnaissance de caractères. Ainsi, les gestes n'apparaîtront que si vous êtes sur le bureau, ou dans l'explorateur de fichiers, Total Commander ou Xplorer.

Vous pouvez également interrompre un long processus OCR en appuyant simplement sur « Annuler » dans la fenêtre de la barre de progression ; cette fenêtre vous donne également des informations sur l'état de l'OCR, en mettant à jour les informations toutes les 5 secondes. Vous pouvez configurer comment recevoir les informations de la barre de progression avec la commande NVDA-u standard.

Vous trouverez un sous-menu nommé Nao, sous le menu NVDA - Outils. Il contient les éléments suivants :

* Sélectionner un fichier : vous permet de sélectionner un fichier à traiter sans utiliser de raccourci.
* Faites un don : c'est explicite, si le cœur vous en dit nous en serons très heureux !
* Site Web Nao : vous amène à la page d'accueil de Nao.
* Git : vous amène au code sourceò où vous pouvez le vérifier, effectuer un commit ou ouvrir un ticket.
* Vérifier les mises à jour : interroge le serveur pour une nouvelle version de Nao.
* Cache vide : si vous rencontrez des problèmes avec le module complémentaire, recevez des messages d'erreur ou trouvez-le lent, videz votre cache pour résoudre le problème.

## Soutien et dons
Nao est absolument gratuit. Cependant, n'oubliez pas que cette extension est faite durant le temps libre des développeurs.
Nous apprécierions toute contribution que vous pourriez nous apporter !
Si vous pensez que notre travail est bon et qu'il améliore votre vie, <a href="https://nvda-nao.org/donate">Envisagez de faire un don.</a>

Vous souhaitez signaler un bug, proposer de nouvelles fonctionnalités, traduire l'extension dans votre langue ? Nous avons l'adresse e-mail qu'il vous faut ! Écrivez simplement à support@nvda-nao.org (a priori en anglais ou italien) et nous serons heureux de vous aider.

## Historique
### 2025.1
* Compatibilité avec NVDA version 2025.1
* Implémentation de la reconnaissance OCR sur la pièce jointe sélectionnée d'un message Outlook ouvert, à partir d'Outlook 2016 et au-delà
* Ajout de la traduction finlandaise
### 2024.1
* Compatibilité avec NVDA version 2024.1
### 2023.1.1
* Compatibilité avec NVDA version 2023.3 restaurée
* Un nouveau raccourci clavier NVDA + Ctrl + Maj + W prend une capture d'écran de la fenêtre courante et en effectue la reconnaissance
* Ajout de la traductions en portugais brésilien
* Correctif de sécurité sur les écrans sécurisés
* Menu d'outils NAO supprimé sur les écrans sécurisés
* Cache des documents supprimé sur les écrans sécurisés
* Liens vers le site Web NAO et le référentiel Git ajoutés au menu des outils NAO
### 2023.1
* Compatibilité avec NVDA version 2023.1
### 2022.1.3
* Compatibilité avec NVDA version 2022.1
* Traductions en chinois simpplifié et en français mises à jour
* Documentation espagnole mise à jour
### 2022.1.2
* capacité de sauvegarde et de chargement du format de fichier nao-document.
* Un cache des documents peut stocker les reconnaissances pour accélérer la prochaine ouverture. Si un fichier est trouvé dans le cache, il n'est pas reconnu à nouveau mais la version mise en cache est ouverte à la place (les paramètres de reconnaissance doivent correspondre).
* Enregistre la dernière position de lecture d'un document dans les métadonnées du cache.
* Purge automatique du cache des documents.
* Effacement manuel du cache dans le menu Outils.
* Un fichier peut désormais être reconnu directement depuis un "dossier compressé" de l'explorateur Windows.
* Meilleure vérification des fichiers invalides.
* Meilleure compatibilité avec l'explorateur Windows en utilisant différentes alternatives de sélection de fichiers : d'abord essai avec Shell.Application dans NVDA, puis essai de Shell.Application dans PowerShell, puis à défaut passage à la navigation manuelle.
* Le moteur OCR conserve le paramètre de langue pendant tout le processus de reconnaissance, même s'il est modifié pendant une reconnaissance de plusieurs pages.
* File d'attente OCR pour reconnaître à partir de plusieurs sources.
* Le raccourci clavier PgSuiv à la dernière page d'un document va à la fin du document en indiquant le numéro de ligne.
* Le dossier temporaire de Windows est utilisé pour les outils de conversion de fichiers à la place du dossier du plugin (meilleures performances sur NVDA portable).
* Traduction roumaine et mise à jour de la traduction chinoise simplifiée.
### 2022.1.1
* Prise en charge du format de fichier DjVu.
* Prise en charge des fichiers tiff multipages.
* Correction d'un bug d'encodage PDF pour les systèmes d'exploitation en langue chinoise. sélectionné
* Mise à jour manuelle de l'extension dans le menu NVDA - Outils.
* Compatibilité à partir de NVDA 2019.3.
### 2022.1
* Mise à jour automatique de l'extension.
* Traductions espagnole et française mises à jour.
### 2021.2
* L'OCR de pdf et des images sont présentés dans une nouvelle fenêtre de texte, avec quelques raccourcis clavier pour des opérations simples.
* Prise en charge du gestionnaire de fichiers Xplorer.
* Les raccourcis Nao sont personnalisables à partir de la boîte de dialogue Gestes d'entrée de NVDA.
* Nao ne fonctionne que là où c'est possible, donc si vous êtes dans une fenêtre non prise en charge, le raccourci clavier sera ignoré par l'extension ; cela a résolu un problème important où les utilisateurs d'Excel et de Word ne pouvaient pas appuyer sur la touche NVDA-Maj-r, car elle était incorrectement interceptée par Nao.
* Un long processus OCR peut être interrompu en appuyant simplement sur le bouton « Annuler » dans la fenêtre de la barre de progression.
* Ajout de traductions en turc, russe, espagnol, chinois et français.
* Les utilisateurs peuvent faire des dons au projet.
* Correction d'un bug avec certains caractères dans le nom du fichier qui empêchait l'OCR de fonctionner correctement.
### 2021.1
* Première version publique !


[1]: https://nvda-nao.org/download
