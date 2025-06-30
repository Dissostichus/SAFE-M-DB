from __future__ import print_function
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd 
import subprocess
import os
from pyexcel_ods import save_data
from collections import OrderedDict
import glob

# Connection à une database

def connect_database():
    """Etablie la connexion avec la base de données.

    Parameters
    ----------
    user : str
        Le nom d'utilisateur utilisé pour s'authentifier auprès du serveur MySQL.
    passwd : str
        Le mot de passe permettant d'authentifier l'utilisateur auprès du serveur MySQL.
    db : str
        Le nom de la base de données à utiliser lors de la connexion au serveur MySQL.
    host : str
        Le nom d'hôte ou l'adresse IP du serveur MySQL. Par défaut : 127.0.0.1 ou localhost

    Les paramètres sont ici déjà remplis par défaut.

    Returns
    -------
    connection : 
        Objet de connexion à la base de données MySQL/MariaDB. 
    cursor : 
        Objet curseur permettant d'exécuter des requêtes SQL.
    """
    connection = mysql.connector.connect(host="localhost",
    user="root",
    passwd="L@grang1en2024",
    db="test_SAFEM_DATA")
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("select database();")
            db = cursor.fetchone()
            print("You're connected to dtabase: ", db)
    except Error as e:
        print("Error while connecting to MySQL", e)
    return connection, cursor

# Insérer des données

def insert_data_localisation(connection, cursor, df):
    """Ajoute des enregistrements dans la base de données SAFE-M dans le TABLE 
    localisation de manière intéractive.

    Parameters
    ----------
    connection :
        Objet de connexion à la base de données MySQL/MariaDB. 
    cursor : 
        Objet curseur permettant d'exécuter des requêtes SQL.
    df : Dataframe pandas
        Dataframe regroupant les données du fichier LibreOffice "template_localisation.ods" 
        remplit par l'utilisateur pour ajouter les données de localisation de puits/sources/rivières.
    """

    df = df.replace({np.nan: None})
    
    required_fields = ['loc_type', 'latitude', 'longitude', 'loc_code']
    if not all(field in df.columns for field in required_fields):
        missing = [f for f in required_fields if f not in df.columns]
        raise ValueError(f"Missing required fields: {missing}")

    add_localisation = """INSERT INTO localisation 
        (loc_type, name, latitude, longitude, altitude, description, 
         contact, coord_sys, gps_used, exploitation, loc_date, 
         referentiel_z, photos_list, quartier, loc_code) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    for i, row in df.iterrows():
        data = (
            str(row['loc_type']) if row['loc_type'] is not None else None,
            str(row['name']) if row.get('name') is not None else None,
            float(row['latitude']) if row['latitude'] is not None else None,
            float(row['longitude']) if row['longitude'] is not None else None,
            float(row['altitude']) if row.get('altitude') is not None else None,
            str(row['description']) if row.get('description') is not None else None,
            str(row['contact']) if row.get('contact') is not None else None,
            str(row['coord_sys']) if row.get('coord_sys') is not None else 'WGS84',
            str(row['gps_used']) if row.get('gps_used') is not None else None,
            str(row['exploitation']) if row.get('exploitation') is not None else None,
            pd.to_datetime(row['loc_date']).strftime('%Y-%m-%d %H:%M:%S') 
                if pd.notna(row.get('loc_date')) else None,
            str(row['referentiel_z']) if row.get('referentiel_z') is not None else None,
            str(row['photos_list']) if row.get('photos_list') is not None else None,
            str(row['quartier']) if row.get('quartier') is not None else None,
            str(row['loc_code']) if row['loc_code'] is not None else None
        )
            
        cursor.execute(add_localisation, data)

    connection.commit()

def insert_data_measurements(connection, cursor, df):
    """Ajoute des enregistrements dans la base de données SAFE-M dans le TABLE 
    measurements de manière intéractive.

    Parameters
    ----------
    connection :
        Objet de connexion à la base de données MySQL/MariaDB. 
    cursor : 
        Objet curseur permettant d'exécuter des requêtes SQL.
    df : Dataframe pandas
        Dataframe regroupant les données du fichier LibreOffice "template_measurements.ods" 
        remplit par l'utilisateur pour ajouter les données de mesures physico-chimique/piezométriques.
    """

    df = df.replace({np.nan: None})
    
    required_fields = ['loc_code']
    if not all(field in df.columns for field in required_fields):
        missing = [f for f in required_fields if f not in df.columns]
        raise ValueError(f"Missing required fields: {missing}")

    add_measurements = """INSERT INTO measurements 
        (loc_code, mdate, mtype, mvalue, munit, comment) 
        VALUES (%s, %s, %s, %s, %s, %s)"""
    
    for i, row in df.iterrows():
        data_measurements = (
            str(row['loc_code']) if row['loc_code'] is not None else None,
            pd.to_datetime(row['mdate']).strftime('%Y-%m-%d %H:%M:%S') 
                if pd.notna(row.get('mdate')) else None,
            str(row['mtype']) if row.get('mtype') is not None else None,
            float(row['mvalue']) if row['mvalue'] is not None else None,
            str(row['munit']) if row.get('munit') is not None else None,
            str(row['comment']) if row.get('comment') is not None else None
        )
            
        cursor.execute(add_measurements, data_measurements)

    connection.commit()

# Modifier/Visualiser des données

def modify_database_records(connection, cursor, data_type, by_code, search_value):
    """Modifie des enregistrements dans la base de données de manière interactive.
    
    Parameters:
    -----------
    connection :
        Objet de connexion à la base de données MySQL/MariaDB. 
    cursor : 
        Objet curseur permettant d'exécuter des requêtes SQL.
    data_type : str
        'localisation' ou 'measurements' en fonction du TABLE à modifier
    by_code : booléen
        True pour accèder aux données par le loc_code, False pour accèder aux données par la date de la prise de mesure
    search_value : str
        Numéro du loc_code ou la date qui permet de cibler les données à modifier
    """
    
    table_name = 'localisation' if data_type == 'localisation' else 'measurements'
    id_column = 'loc_code'
    date_column = 'loc_date' if data_type == 'localisation' else 'mdate'
    key_columns = ['rec_code', id_column, date_column] if data_type == 'localisation' else ['rec', id_column, date_column]
    display_columns = key_columns + (['mtype', 'mvalue', 'comment'] if data_type == 'measurements' 
                                   else ['name', 'latitude', 'longitude', 'description', 'quartier'])

    if by_code:
        query = f"SELECT * FROM {table_name} WHERE {id_column} = %s"
    else:
        query = f"SELECT * FROM {table_name} WHERE DATE({date_column}) = %s"
    
    cursor.execute(query, (search_value,))
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    
    if df.empty:
        print(f"Aucun enregistrement trouvé avec ces critères.")
        return
    
    print(f"Enregistrements trouvés ({len(df)}):")
    print(df[display_columns].to_string(index=False))
    
    if data_type == 'localisation' :
        if by_code: 
            try:
                rec_to_modify = input(f"Souhaitez vous modifier/visualiser l'enregistrement {search_value} (O/N) ? ")
                if rec_to_modify in ['n','N']:
                    print("Opération annulée.")
                    return
                
                if rec_to_modify in ['o','O','y','Y']:
                    rec_to_modify = search_value

                if rec_to_modify not in df['loc_code'].values:
                    print("Code 'loc_code' invalide.")
                    return
            except ValueError:
                print("Veuillez entrer un code valide.")
                return
        else:
            try:
                rec_to_modify = input("Entrez le numéro 'loc_code' de l'enregistrement à modifier/visualiser (0 pour annuler) : ")
                if rec_to_modify == 0:
                    print("Opération annulée.")
                    return
                    
                if rec_to_modify not in df['loc_code'].values:
                    print("Code 'loc_code' invalide.")
                    return
            except ValueError:
                print("Veuillez entrer un code valide.")
                return

    else :
        try:
            rec_to_modify = int(input("Entrez le numéro 'rec' de l'enregistrement à modifier/visualiser (0 pour annuler) : "))
            if rec_to_modify == 0:
                print("Opération annulée.")
                return
                
            if rec_to_modify not in df['rec'].values:
                print("Numéro 'rec' invalide.")
                return
        except ValueError:
            print("Veuillez entrer un numéro valide.")
            return

    selected_record = df[df['loc_code'] == rec_to_modify].iloc[0] if data_type == 'localisation' else df[df['rec'] == rec_to_modify].iloc[0]
    
    def convert_value(value):
        """Convertie les valeurs pour l'export ODS"""
        if pd.isna(value) or value is None:
            return ""
        if isinstance(value, (pd.Timestamp, datetime)):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(value, (np.integer, np.floating)):
            return float(value) if isinstance(value, np.floating) else int(value)
        return str(value)
    
    filename = f"modify_{data_type}.ods" if data_type == 'localisation' else f"modify_{data_type}.ods"
    data_dict = OrderedDict()
    
    df_export = pd.DataFrame([selected_record])
    for col in df_export.columns:
        df_export[col] = df_export[col].apply(convert_value)
    
    data_dict["Feuille1"] = [df_export.columns.tolist()] + df_export.values.tolist()
    save_data(filename, data_dict)
    
    print(f"Fichier {filename} généré pour modification.")
    if os.path.exists(filename):
        subprocess.run(["xdg-open", filename])
    
    input("Appuyez sur Entrée après avoir enregistré vos modifications")
    
    try:
        df_modified = pd.read_excel(filename, sheet_name="Feuille1", header=0)
        df_modified = df_modified.replace({np.nan: None})
        
        if len(df_modified) != 1:
            print("Le fichier modifié doit contenir exactement un enregistrement")
            return
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
        return

    if data_type == 'localisation':
        update_query = f"""UPDATE {table_name} SET
            loc_type = %s, name = %s, latitude = %s, longitude = %s, 
            altitude = %s, description = %s, contact = %s, coord_sys = %s, 
            gps_used = %s, exploitation = %s, loc_date = %s, 
            referentiel_z = %s, photos_list = %s, quartier = %s
            WHERE loc_code = %s"""
        
        update_data = (
            str(df_modified.iloc[0]['loc_type']) if df_modified.iloc[0]['loc_type'] is not None else None,
            str(df_modified.iloc[0]['name']) if df_modified.iloc[0].get('name') is not None else None,
            float(df_modified.iloc[0]['latitude']) if df_modified.iloc[0]['latitude'] is not None else None,
            float(df_modified.iloc[0]['longitude']) if df_modified.iloc[0]['longitude'] is not None else None,
            float(df_modified.iloc[0]['altitude']) if df_modified.iloc[0].get('altitude') is not None else None,
            str(df_modified.iloc[0]['description']) if df_modified.iloc[0].get('description') is not None else None,
            str(df_modified.iloc[0]['contact']) if df_modified.iloc[0].get('contact') is not None else None,
            str(df_modified.iloc[0]['coord_sys']) if df_modified.iloc[0].get('coord_sys') is not None else 'WGS84',
            str(df_modified.iloc[0]['gps_used']) if df_modified.iloc[0].get('gps_used') is not None else None,
            str(df_modified.iloc[0]['exploitation']) if df_modified.iloc[0].get('exploitation') is not None else None,
            pd.to_datetime(df_modified.iloc[0]['loc_date']).strftime('%Y-%m-%d %H:%M:%S') 
                if pd.notna(df_modified.iloc[0].get('loc_date')) else None,
            str(df_modified.iloc[0]['referentiel_z']) if df_modified.iloc[0].get('referentiel_z') is not None else None,
            str(df_modified.iloc[0]['photos_list']) if df_modified.iloc[0].get('photos_list') is not None else None,
            str(df_modified.iloc[0]['quartier']) if df_modified.iloc[0].get('quartier') is not None else None,
            str(rec_to_modify)
        )
    else:
        update_query = f"""UPDATE {table_name} SET
            loc_code = %s, mdate = %s, mtype = %s, 
            mvalue = %s, munit = %s, comment = %s
            WHERE rec = %s"""
        
        update_data = (
            str(df_modified.iloc[0]['loc_code']) if df_modified.iloc[0]['loc_code'] is not None else None,
            pd.to_datetime(df_modified.iloc[0]['mdate']).strftime('%Y-%m-%d %H:%M:%S') 
                if pd.notna(df_modified.iloc[0].get('mdate')) else None,
            str(df_modified.iloc[0]['mtype']) if df_modified.iloc[0].get('mtype') is not None else None,
            float(df_modified.iloc[0]['mvalue']) if df_modified.iloc[0]['mvalue'] is not None else None,
            str(df_modified.iloc[0]['munit']) if df_modified.iloc[0].get('munit') is not None else None,
            str(df_modified.iloc[0]['comment']) if df_modified.iloc[0].get('comment') is not None else None,
            int(rec_to_modify)
        )
    
    if data_type == 'localisation' :

        try:
            cursor.execute(update_query, update_data)
            connection.commit()
            print(f"Enregistrement loc_code={rec_to_modify} mis à jour avec succès!")
        except Exception as e:
            connection.rollback()
            print(f"Erreur lors de la mise à jour : {e}")
    else :
        try:
            cursor.execute(update_query, update_data)
            connection.commit()
            print(f"Enregistrement rec={rec_to_modify} mis à jour avec succès!")
        except Exception as e:
            connection.rollback()
            print(f"Erreur lors de la mise à jour : {e}")

# Inserer des données depuis un fichier DATA

def add_from_DATA(connection, cursor, data_type):
    """Ajoute des enregistrements à la base de données depuis un fichier LibreOffice déjà remplit.

    Parameters
    ----------
    connection :
        Objet de connexion à la base de données MySQL/MariaDB. 
    cursor : 
        Objet curseur permettant d'exécuter des requêtes SQL.
    data_type : str
        'localisation' ou 'measurements' en fonction du TABLE ou l'on souhaite 
        ajouter les enregistrements
    """

    if data_type == 'localisation' : 

        interface_notice_localisation = """
        ===========================================================================
        ATTENTION NOTICE
        ===========================================================================
        Pour ajouter des données à partir d'un fichier LibreOffice celui-ci doit respecter certaines conditions :
        - La nom du fichier doit être de la forme : donnees_localisation_***.ods
        - Les colonnes doivent commencer à la premiere case de la première ligne et dans l'ordre : 

        loc_type | name | latitude | longitude | altitude | description | contact | coord_sys | gps_used | exploitation | loc_date | referentiel_z | photos_list | quartier | loc_code 
        
        - La feuille de calcul sur laquelle sont notés les données doit s'appeler Feuille1
        ===========================================================================
        Appuyez sur Entrée une fois avoir pris connaissance de la notice.
        """
        x_notice_localisation = input(interface_notice_localisation)
    
    else :
        interface_notice_measurements = """
        ===========================================================================
        ATTENTION NOTICE
        ===========================================================================
        Pour ajouter des données à partir d'un fichier LibreOffice celui-ci doit respecter certaines conditions :
        - La nom du fichier doit être de la forme : donnees_measurements_***.ods
        - Les colonnes doivent commencer à la premiere case de la première ligne et dans l'ordre : 

        loc_code | mdate | mtype | mvalue | munit | comment 

        - La feuille de calcul sur laquelle sont notés les données doit s'appeler Feuille1
        ===========================================================================
        Appuyez sur Entrée une fois avoir pris connaissance de la notice.
        """
        x_notice_measurements = input(interface_notice_measurements)

    input('A présent vous pouvez déposer le fichier LibreOffice (.ods) dans le dossier DATA, Appuyer sur Entrée une fois le fichier déposé')

    if data_type == 'localisation':
        file_pattern = './DATA/donnees_localisation_*.ods'
        sheet_name = 'Feuille1'
    elif data_type == 'measurements':
        file_pattern = './DATA/donnees_measurements_*.ods'
        sheet_name = 'Feuille1'
    else:
        print("Type de données non reconnu. Vérifiez le titre des fichiers. Exemple : donnees_localisation_2025-06-13.ods ou donnees_measurements_2025-06-13.ods")
        return

    try:
        available_files = sorted(glob.glob(file_pattern), key=os.path.getmtime)
    except Exception as e:
        print(f"Erreur lors de la recherche des fichiers: {str(e)}")
        return

    if not available_files:
        print(f"Aucun fichier {data_type} trouvé dans le dossier DATA.")
        return

    print("\nFichiers disponibles:")
    for i, file_path in enumerate(available_files):
        print(f"{i} - {os.path.basename(file_path)}")

    try:
        choice = input("\nChoisissez votre fichier en entrant son numéro d'ordre: ")
        selected_file = available_files[int(choice)]
        
        print(f"Lecture du fichier {os.path.basename(selected_file)}")
        df = pd.read_excel(selected_file, sheet_name=sheet_name)
        
        if df.empty:
            print("Avertissement: Le fichier sélectionné ne contient aucune donnée.")
            return
            
        print(f"{len(df)} enregistrements trouvés dans le fichier.")
        
        confirm = input(f"Voulez-vous insérer {len(df)} enregistrements dans la base de données? (O/N): ")
        if confirm in ['n','N']:
            print("Opération annulée.")
            return
        
        if confirm in ['o','O','y','Y']:

            if data_type == 'localisation':
                try :
                    insert_data_localisation(connection, cursor, df)
                    print("Enregistrement terminé")
                except ValueError :
                    print("Erreur lors de l'enregistrement des données")
            else : 
                try :
                    insert_data_measurements(connection,cursor, df)
                    print("Enregistrement terminé")
                except ValueError :
                    print("Erreur lors de l'enregistrement des données")


    except ValueError:
        print("Erreur: Veuillez entrer un numéro valide.")
    except IndexError:
        print("Erreur: Le numéro sélectionné ne correspond à aucun fichier.")
    except pd.errors.EmptyDataError:
        print("Erreur: Le fichier sélectionné est vide ou corrompu.")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite: {str(e)}")