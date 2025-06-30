.. _modify:

Visualiser et modifier des enregistrements
==========================================

En dernier lieu ce programme vous permet d'accéder aux enregistrements contenus dans la base de données et si vous le souhaitez 
de les modifier. Dans le ``MENU PRINCIPAL`` selectionnez l'option ``3 - Visualiser/Modifier d'anciennes données``. Une fois n'est 
pas coutume vous devez ensuite spécifier le type de données auquel vous désirez accéder . Cela permet au programme de savoir dans quel
``TABLE`` de ``SAFEM_DATA`` chercher. 

Dans le menu ``SELECTION DES DONNEES`` qui s'affiche ensuite vous devez choisir la façon dont vous souhaitez accéder à vos données.
La base de données ``SAFEM_DATA`` contenant de nombreux enregistrements une premièr recoupement est nécessaire. Vous avez le choix entre utilisez
le code de nomenclature (cf. :ref:`skeleton`) ou bien la date de la prise de mesure ou de l'enregistrement de la localisation du puit. 

Selectionnez le mode de recherche puis renseignez votre code ou votre date. Le programme va alors vous dressez la liste de tout les enregistrement qui 
correspondent à l'indice de recherche que vous avez rentré::

    ===========================================================================
    SELECTION DES DONNEES
    ===========================================================================
    Comment voulez-vous accéder à vos données :
    1 - En saisissant le code de localisation (nomenclature)
    2 - En saisissant la date de la prise de la mesure
    3 - Retour au menu principal
    ===========================================================================
    
    -> 2

    Saisissez la date (format YYYY-MM-DD) : 
    
    -> 2025-06-12

    Enregistrements trouvés (4):
    rec loc_code      mdate mtype  mvalue  comment
    1397     L003 2025-06-12   Orp   256.0  modifie
    1398     L003 2025-06-12   Orp   165.0 modifié4
    1399     L003 2025-06-12   Orp   255.0     None
    1407     IPGP 2025-06-12 piezo   135.0    chaud
    Entrez le numéro 'rec' de l'enregistrement à modifier/visualiser (0 pour annuler) : 

.. note:: 

    Dans le cas où vous recherchez des enregistrement de localisation avec le code de nomenclature il est tout à fait normal de n'obtenir qu'un seul 
    enregistrement correspondant puis cette clef de recherche est unique et propre à chaque puit recenscé.

Il vous est donc possible de visualiser n'importe quelles données de la database pour peu que vous connaissiez la nomenclature ou la date de la prise de données
de l'enregistrement recherché. Il vous est, dans la suite du programme, aussi possible de modifié un enregistrement spécifique.
Le programme vous demande alors de renseignez le code d'enregistrement ``rec`` (dans le cas de données de mesures) ou le code de nomenclature ``loc_code`` 
(dans le cas de données de localisation) qui correspond à la ligne de l'enregistrement que vous souhaitez modifier. Si vous ne souhaitez pas modifier de données saisissez 
la touche ``0`` pour revenir au ``MENU PRINCIPAL``.

Une fois votre réponse validée un fichier LibreOffice
s'ouvre contenant la ligne que vous pouvez dès à présent modifier. N'oubliez d'enregistrer vos modifications avec **CTRL + S**. Une fois terminé refermez le fichier, retournez
sur le programme et appuyez sur **Entrée** pour mettre à jour la database. 

Le programme vous annonce la bonne modification de la base de données et vous redirige ensuite sur le ``MENU PRINCIPAL`` pour poursuivre votre travail::

    Entrez le numéro 'rec' de l'enregistrement à modifier/visualiser (0 pour annuler) : 
    
    -> 1398

    Fichier modify_measurements.ods généré pour modification.
    Appuyez sur Entrée après avoir enregistré vos modifications
    Enregistrement rec=1398 mis à jour avec succès!

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


