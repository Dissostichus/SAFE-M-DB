# SAFE-M-DB: Intéragir avec la base de données sur l'eau à Madagascar de SAFE-M

* [Introduction](##introduction)
* [Prérequis](##support)
* [SAFEM-DATA](##MariaDB)
* [Programme python](##python)

## Introduction <a class="anchor" id="introduction"></a>

* Ce programme permet d'intéragir avec la base de données sur l'eau à Madagascar de SAFE-M, SAFEM_DATA au travers de feuille de calcul LibreOffice Calc.
* Il résulte d'un travail effectué lors d'un stage de Licence 3 à l'Institut de physique du globe de Paris.


## Prérequis <a class="anchor" id="support"></a>

Afin que l'intéraction avec la base de données SAFEM_DATA puisse fonctionner ce programme doit être depuis une machine Linux possédant les modules python3 suivant :

* mysql, datetime, numpy, pandas, subprocess, os, pyexcel_ods, collections, glob

Si ce n'est pas le cas : 
> sudo apt install python3-mysql python3-datetime python3-numpy python3-pandas python3-subprocess python3-os python3-pyexcel_ods python3-collections python3-glob

MariaDB doit être installé et configuré sur votre machine afin de charger la base de données SAFEM_DATA depuis un répertoire distant : 
https://mariadb.org/download/?t=mariadb&p=mariadb&r=11.8.2&os=Linux&cpu=x86_64&pkg=tar_gz&i=systemd&mirror=liquidtelecom

## SAFEM_DATA <a class="anchor" id="MariaDB"></a>

* Cette base de données résulte d'un travail collectif effectué par des étudiant.e.s et professeur.e.s de ...  et de l'Institut de physique du globe de Paris.

La dernière version de cette base de données est disponible sur le github de l'organisation SAFE-M : https://github.com/SAFE-M
Pour charger la base de données une fois celle-ci installée sur votre machine saisissez dans votre terminal : 
> mysql -u votre_nom_utilisateur -p votre_mot_de_passe UTF-8safem_data.sql

Pour plus d'informations sur la structure de la base de données référez-vous à la documentation de ce programme : docs/_build/html/bones.html


## Programme Python <a class="anchor" id="python-and-sql"></a>

La connexion à la base de données et l'intéraction à partir de feuille de calcul LibreOfficeCalc est effectuée au moyen d'un programme python. 

Pour des raisons de simplicité le script fonctionne en mode terminal, pas d'interface utilisateur graphique donc, et offre des choix à l'étudiant. Le programme permet

* l'Ajout de nouveaux enregistrements en saisissant manuellement les informations sur une feuille de calcul LibreOfficeCalc;
* l'Ajout de nouveaux enregistrement depuis une feuille de calcul LibreOfficeCalc déjà pré-remplie;
* la visualisation dans un feuille de calcul LibreOfficeCalc de données déjà enregistrées;
* la modification de données déjà enregistrées dans la base de données depuis une feuille de calcul LibreOfficeCalc;
* la suppression d'enregistrements déjà saisis dans la base de données depuis une feuille de calcul LibreOfficeCalc.

Les modification apportées à la base de données sont pour l'heure propre à chaque machine, la synchronisation et l'implémentation des modifications ne s'enregistre pas dans un serveur mais localement sur l'ordinateur de l'étudiant. 