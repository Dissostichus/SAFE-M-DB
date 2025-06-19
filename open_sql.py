import subprocess
import os
import pandas as pd
import numpy as np
from pyexcel_ods import save_data
from collections import OrderedDict
from datetime import datetime

from lib_sql import *

if __name__ == '__main__':

    interface ="""
    ===========================================================================
    MENU PRINCIPAL
    ===========================================================================
    Que souhaitez-vous faire ?
    1 - Ajouter de nouvelles données
    2 - Ajouter à partir d'un fichier déjà remplit
    3 - Visualiser/Modifier d'anciennes données
    4 - Quitter
    ===========================================================================
    ? """

    connection, cursor = connect_database()
    continuer = True 
    continuer_add = True
    continuer_add_DATA = True

    while continuer:

        x = input (interface)
        
        if x == '1':

            while continuer_add :

                interface_add = """
                ===========================================================================
                MENU CHOIX DES DONNEES
                ===========================================================================
                    Quelles données voulez-vous ajouter :
                    1 - Localisation de puits/sources/rivières ?
                    2 - Mesures physico-chimiques/piézométriques ?
                    3 - Quitter le menu choix des données et retourner au menu principal
                ===========================================================================
                """

                x_add = input(interface_add)
                if x_add == '1':

                    entetes = ["loc_type", "name", "latitude", "longitude", "altitude", "description", "contact", "coord_sys", "gps_used", "exploitation", "loc_date", "referentiel_z", "photos_list", "quartier", "loc_code"]

                    classeur = OrderedDict()
                    classeur.update({"Feuille1": [entetes]}) 

                    template = "template_localisation.ods"
                    save_data(template, classeur)
                    print(f"Fichier ODS '{template}' créé avec succès.")

                    template = "./template_localisation.ods"  # ou .xlsx pour Excel
                    if os.path.exists(template):
                        subprocess.run(["xdg-open", template])  # Linux (LibreOffice/Excel)
                        #subprocess.run(["start", "", fichier_excel], shell=True)  # Windows (Excel)
                    else:
                        print("Fichier non trouvé !")

                    input('Une fois le fichier LibreOffice enregistré, Appuyez sur Entrée')
                    sheet = "Feuille1" 
                    df = pd.read_excel(io=template, sheet_name=sheet)
                    insert_data_localisation(connection,cursor,df)
                    print('Database mis à jour')

                if x_add == '2':

                    entetes = ["loc_code", "mdate", "mtype", "mvalue", "munit", "comment"]

                    classeur = OrderedDict()
                    classeur.update({"Feuille1": [entetes]}) 

                    template = "template_measurements.ods"
                    save_data(template, classeur)
                    print(f"Fichier ODS '{template}' créé avec succès.")


                    template = "./template_measurements.ods"  # ou .xlsx pour Excel
                    if os.path.exists(template):
                        subprocess.run(["xdg-open", template])  # Linux (LibreOffice/Excel)
                        #subprocess.run(["start", "", fichier_excel], shell=True)  # Windows (Excel)
                    else:
                        print("Fichier non trouvé !")

                    input('Une fois le fichier LibreOffice enregistré, Appuyez sur Entrée')
                    sheet = "Feuille1" 
                    df = pd.read_excel(io=template, sheet_name=sheet)
                    insert_data_measurements(connection,cursor,df)

                    print('Database mis à jour')

                if x_add == '3':
                    continuer_add = False

        if x == '2':

            while continuer_add_DATA :

                interface_add_DATA = """
                ===========================================================================
                MENU CHOIX DES DONNEES
                ===========================================================================
                    Quelles données voulez-vous ajouter :
                    1 - Localisation de puits/sources/rivières ?
                    2 - Mesures physico-chimiques/piézométriques ?
                    3 - Quitter le menu choix des données et retourner au menu principal
                ===========================================================================
                """

                x_add_DATA = input(interface_add_DATA)
                if x_add_DATA in ['1', '2']:
                    data_type = 'localisation' if x_add_DATA == '1' else 'measurements'
                    add_from_DATA(connection, cursor,data_type)
                
                if x_add_DATA == '3':
                    continuer_add_DATA = False

        if x == '3':
            interface_update = """
            ===========================================================================
            MODIFICATION DES DONNEES
            ===========================================================================
            Quelles données voulez-vous modifier :
            1 - Localisation de puits/sources/rivières
            2 - Mesures physico-chimiques/piézométriques
            3 - Retour au menu principal
            ===========================================================================
            """
            
            x_update = input(interface_update)
            
            if x_update in ['1', '2']:
                selection_interface = """
                ===========================================================================
                SELECTION DES DONNEES
                ===========================================================================
                Comment voulez-vous accéder à vos données :
                1 - En saisissant le code de localisation (nomenclature)
                2 - En saisissant la date de la prise de la mesure
                3 - Retour au menu principal
                ===========================================================================
                """
                selection = input(selection_interface)
                
                if selection in ['1', '2']:
                    data_type = 'localisation' if x_update == '1' else 'measurements'
                    by_code = selection == '1'
                    
                    prompt = "Saisissez le code d'enregistrement : " if by_code else "Saisissez la date (format YYYY-MM-DD) : "
                    search_value = input(prompt)
                    
                    modify_database_records(connection=connection, cursor=cursor, data_type=data_type, by_code=by_code, search_value=search_value)

        if x == '4':
            continuer = False

    print('Fin du programme')

    ################################################################################
    cursor.close()
    connection.close()
    print("MySQL connection is closed")
    ################################################################################




