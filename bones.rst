.. _skeleton:

Détails et structure de la base de données SAFEM_DATA
=====================================================

La base de données sur l'eau à Madagascar ``SAFEM_DATA`` contient 5 ``TABLES`` de données::

    MariaDB [SAFEM_DATA]> show tables;

    +----------------------+
    | Tables_in_SAFEM_DATA |
    +----------------------+
    | Members              |
    | courses              |
    | localisation         |
    | measurements         |
    | science              |
    +----------------------+

Le **TABLE** ``Members`` regroupe des informations sur les collaborateurs de SAFE-M.

Le **TABLE** ``courses`` contient plusieurs cours d'hydrologie ou de programmation de niveau Licence 3 et Master.

Le **TABLE** ``science`` possède plusieurs références bibliographiques.

Les deux derniers **TABLES** vont être décris plus en détails car le programme documenté ici permet d'intéragir facilement aver la base de données 
de manière interactive via ces deux **TABLES**. 

measurements
------------

ce **TABLE** possède 7 colonnes de données ::

    MariaDB [SAFEM_DATA]> select * from measurements;

    +------+----------+---------------------+------------------------+---------+-----------+-------------------------------------+
    | rec  | loc_code | mdate               | mtype                  | mvalue  | munit     | comment                             |
    +------+----------+---------------------+------------------------+---------+-----------+-------------------------------------+
    |  157 | A001     | 2022-03-14 00:00:00 | Profondeur puits       |      15 | m         | date approx                         |

``rec``, doit être un nombre entier, est un numéro d'enregistrement automatiquement attribué par la base de donnée lorsque un nouvel enregistrement est fournit.

``loc_code``, doit être une chaine de caractères, est un code qui fait office de nomenclature, ce code consensuel, unique et propre à chaque puit, source ou rivière est attribué par les utilisateurs
lors de l'enregistrement d'une nouvelle localisation. Cela permet de cataloguer, d'identifier clairement et de retrouver de manière simple un point d'enregistrement.
Chaque mesure physico-chimique d'échantillon d'eau (par exemple) ou mesure piezométrique est donc associé au puit d'où provient l'échantillon par ce code.

``mdate``, au format **YYYY-MM-DD 00:00:00**, va contenir la date à laquelle à été prise la mesure, les six derniers chiffres correspondent aux heures, minutes et secondes.

``mtype``, doit être une chaine de caractères, va correspondre au type de mesure effectuée, le plus souvent cela peut-être **pH**, **Orp**, **Od**, **Conductivité** ou **mesure piézométrique**.

``mvalue``, doit être un nombre entier ou à virgule, contient la valeur mesurée.

``munit``, doit être une chaine de caractères, contient les unités de la mesures.

``comment``, doit être une chaine de caractère, permet de rajouter quelques commentaires sur la prise de mesures et d'eventuelles informations, par exemple la hauteur de 
la margelle du puit pour une mesure piezométrique.

Saisie sur document LibreOffice
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lors de la saisie de données de mesure sur les documents **LibreOffice** qui vont permettre d'intéragir avec la base de données assurez-vous que les champs que vous remplissez
respecte bien le format attendu et décrit plus haut. 

Tout les champs peuvent ne pas être remplis en cas de manque de données et d'informations néanmoins certains sont obligatoires
pour assurer la validité de l'enregistrement et sont ajout à la base de données. Dans le cas du **TABLES** ``measurements``  seul le champs ``loc_code`` est obligatoire. 

Lors de la saisie de données sur **LibreOffice** vous remarquerez que le champs ``rec`` n'apparait pas, cette information va être automatiquement ajoutée lors de l'ajout à la database, l'utiliateur n'a pas à s'en 
préoccuper.


localisation
------------

Ce **TABLE** possède 16 colonnes de données:: 

    MariaDB [SAFEM_DATA]> select * from localisation;

    +----------+------------------------------------+-------------------------------------+----------+-----------+----------+--------------------------------+-----------------------+----------------------+------------------------------------+----------------------+---------------------+------------------+-----------------+------------------------------------+----------+
    | rec_code | loc_type                           | name                                | latitude | longitude | altitude | description                    | contact               | coord_sys            | gps_used                           | exploitation         | loc_date            | referentiel_z    | photos_list     | quartier                           | loc_code |
    +----------+------------------------------------+-------------------------------------+----------+-----------+----------+--------------------------------+-----------------------+----------------------+------------------------------------+----------------------+---------------------+------------------+-----------------+------------------------------------+----------+
    |        1 | puits                              | NULL                                | -18.9103 |   47.5559 |     1289 | sec                            |                       | WGS84                | NULL                               | NULL                 | NULL                | NULL             | NULL            | NULL                               | A001     |
    |        2 | puits privé traditionnel           | NULL                                | -18.9104 |   47.5573 |     1282 |                                |                       | WGS84                | NULL                               | NULL                 | NULL                | NULL             | NULL            | NULL                               | A002     |
    |        3 | forage du campus                   | NULL                                | -18.9115 |   47.5581 |     1263 |                                |                       | WGS84                | NULL                               | NULL                 | NULL                | NULL             | NULL            | NULL                               | A003     |
    |        4 | forage privé                       | NULL                                | -18.9114 |   47.5581 |     1271 |                                |                       | WGS84                | NULL                               | NULL                 | NULL                | NULL             | NULL            | NULL                               | A004     |
    |        5 | forage piblic                      | NULL                                | -18.9097 |   47.5575 |     1271 | fermé et non fonctionnel       |                       | WGS84                | NULL                               | NULL                 | NULL                | NULL             | NULL            | NULL                               | A005     |

``rec_code``, doit être un nombre entier, est un numéro d'enregistrement automatiquement attribué par la base de donnée lorsque un nouvel enregistrement est fournit.

``loc_type``, doit être une chaine de caractères, pour indiquer qu'est ce qui a été localisé lors de l'enregistrement, une puit, une source, un forage.

``name``, doit être une chaine de caractères, permet d'indiquer le nom de le/la propriétaire du puit par exemple.

``latitude``, ``longitude``, ``altitude``, doivent être des nombres à virgule et sont obtenues par mesure GPS RTK.

``description``, doit être une chaine de caractère, permet de completer avec des informations supplémentaires.

``contact``, doit être une chaine de caractère, permet de renseigner si le/la propriétaire possède un moyen de contact, email, téléphone ou autre.

``coord_sys``, doit être une chaine de caractère, par défaut si rien n'est renseigné ce sera WGS84,  il s'agit d'un système de coordonnées géographiques mondial.

``gps_used``, doit être une chaine de caractère, permet de renseigner le modèle du GPS utilisé.

``exploitation``, doit être une chaine de caractère, permet de renseigner la type d'utilisation du puit si c'est pour un usage domestique par exemple, ou s'il n'est
plus exploité et depuis combien de temps.

``loc_date``, au format **YYYY-MM-DD 00:00:00**, contient la date à laquelle à été prise la mesure de localisation.

``referentiel_z``, doit être une chaine de caractère, permet d'indiquer d'où la mesure d'altitude est prise, s'il s'agit de la tête du puit, de la base de la margelle, etc.

``photos_list``, doit être du texte, par exemple : IMG_20221028_091535, permet d'ajouter la référence de photo du puits qui vont être enregistrés dans un dossier extérieur mais 
qu'il sera facile de retrouver grâce à cette référence. 

``quartier``, doit être une chaine de caractère, permet de renseigner le quartier dans lequel se situe la localisation.

``loc_code``, doit être une chaine de caractère, il s'agit du code qui fait office de nomenclature, ce code consensuel, unique et propre à chaque puit, source ou rivière est attribué par les utilisateurs
lors de l'enregistrement d'une nouvelle localisation. Cela permet de cataloguer, d'identifier clairement et de retrouver de manière simple un point d'enregistrement.

Saisie sur document LibreOffice
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lors de la saisie de données de localisation sur les documents **LibreOffice** qui vont permettre d'intéragir avec la base de données assurez-vous que les champs que vous remplissez
respecte bien le format attendu et décrit plus haut. 

Tout les champs peuvent ne pas être remplis en cas de manque de données et d'informations néanmoins certains sont obligatoires
pour assurer la validité de l'enregistrement et l'ajouter à la base de données. Les champs obligatoires dans le cas du **TABLES** ``localisation`` sont : ``loc_type``, ``latitude``, ``longitude`` et ``loc_code``. 

Lors de la saisie de données sur LibreOffice vous remarquerez que le champs ``rec_code`` n'apparait pas, cette information va être automatiquement ajoutée lors de l'ajout à la database, l'utiliateur n'a pas à s'en 
préoccuper.