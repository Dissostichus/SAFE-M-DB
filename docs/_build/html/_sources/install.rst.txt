Installation
============

Charger le répertoire
---------------------

Afin d'utiliser le programme vous avez besoin de charger le répertoire dans lequel il se trouve. Ce répertoire
contient l'ensemble des codes et dossiers nécessaires à la bonne gestion de la base de donnée.

Vous pouvez cloner le répertoire en saisissant directement dans le terminal la commande::

    # git clone https://github.com/SAFE-M/SAFE-M-DB.git

.. note:: 

    Attention, avant d'importer le programme vérifiez bien que vous vous situez dans votre répertoire de travail.

Le répertoire nouvellement chargé contient dans le dossier ``src``: 

``open_sql.py``, le programme principal permettant d'intéragir avec la base de donnée via l'affichage d'un interface dans le terminal.

``lib_sql.py``, le code contenant l'ensemble des fonctions permettant le bon fonctionnement du programme principal.

``DATA``, ce dossier va être celui dans lequel l'utilisateur devra déposer les fichiers LibreOffice pour l' :ref:`import`.

Installation de la base de données
----------------------------------


Démarrage du programme
----------------------

Essayons de lancer le programme pour voir comment celui-ci fonctionne. Saisissez simplement dans votre terminal::

        # A l'intérieur du dossier src/
        python3 'open_sql.py'

La programme devrait se lancer avec un message de confirmation de connexion à la base de données ainsi qu'avec l'affichage 
du ``MENU PRINCIPAL``::

    You're connected to dtabase:  ('SAFEM_DATA',)

    ===========================================================================
    MENU PRINCIPAL
    ===========================================================================
    Que souhaitez-vous faire ?
    1 - Ajouter de nouvelles données
    2 - Ajouter à partir d'un fichier déjà remplit
    3 - Visualiser/Modifier d'anciennes données
    4 - Quitter
    ===========================================================================
    ? 

Plusieurs choix s'offrent alors à vous : 

:ref:`add`

:ref:`modify`


.. warning::

    Si le programme ne parvient pas à ce connecter à la base de données le message d'erreur suivant apparaitra::

        Error while connecting to MySQL

    Vérifiez alors si les paramètres de connexion dans la fonction ``connect_database()`` sont corrects.

