# PromptMorpher
a generator in a text file of morphed prompt for  stable-diffusion-webui-forge


PromptMorpher
Un outil interactif pour personnaliser, mélanger et transformer vos prompts de manière dynamique.

Description
PromptMorpher est un programme interactif conçu pour les créateurs et utilisateurs d'intelligence artificielle générative, comme Stable Diffusion, qui souhaitent personnaliser et ajuster leurs prompts de manière fluide. Grâce à une interface conviviale basée sur Python et Tkinter, PromptMorpher vous permet de sélectionner des mots ou expressions dans un texte, de les remplacer dynamiquement, et de créer des transitions progressives entre deux concepts.

Fonctionnalités principales
Sélection intuitive de mots ou expressions : Cliquez pour choisir un mot ou une phrase dans le texte, puis configurez des remplacements.
Keyword Blending : Mélangez deux concepts à l'aide de la syntaxe [mot1 : mot2 : facteur].
Transitions progressives : Ajustez les valeurs de début et de fin (en pourcentage) et choisissez le sens des transitions (croissant ou décroissant).
Personnalisation complète : Configurez plusieurs remplacements dans un seul texte.
Génération de fichier : Exportez automatiquement les prompts générés dans un fichier texte.

Prérequis
Python 3.7+
Bibliothèques Python nécessaires :
tkinter (inclus par défaut dans Python sur Windows)
Pillow (si nécessaire pour des extensions futures)
Veuillez regarder le fichier RunMeFirst.bat
Pour windows: cliquez sur RunMeFirst.bat pour installer si besoin automatiquement les librairies python manquante puis lance le script.
Pour Linus, Mac: veuillez installer les librairies nécessaires (ouvrez le fichier baych "RunMeFirst.bat" avec un bloc note.


Lancez le programme :
Pour windows: cliquez sur RunMeFirst.bat

Pour les autres:
python promptmorpher.py



Exemple du fichier texte généré:

-----
Prompt initial:
Un paysage de montagne avec un lac au coucher du soleil.

Prompts générés avec keyword blending:
```
Un paysage de [montagne : ville : 1.0] avec un [lac : volcan : 0.6] au [coucher du soleil : la nuit : 0.0].
Un paysage de [montagne : ville : 0.75] avec un [lac : volcan : 0.52] au [coucher du soleil : la nuit : 0.25].
Un paysage de [montagne : ville : 0.5] avec un [lac : volcan : 0.45] au [coucher du soleil : la nuit : 0.5].
Un paysage de [montagne : ville : 0.25] avec un [lac : volcan : 0.38] au [coucher du soleil : la nuit : 0.75].
Un paysage de [montagne : ville : 0.0] avec un [lac : volcan : 0.3] au [coucher du soleil : la nuit : 1.0].
```
-----


