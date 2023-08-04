"""
Fichier pour l'ouverture de base de données.

    """


import pandas as pd
import numpy as np

# On ouvre la base de donnée de teleajdu une fois pour optimiser le temps de calcul
def open_amc_db(filepath):
    db=pd.read_excel(filepath)
    # Create a new column 'New Column' with the sliced characters
    db['AMC'] = db['Code ISIN'].str[5:11]
    # Create a mapping for renaming the columns
    column_mapping = {
        'Date Courbe': 'Date Courbe',
        'Code ISIN': 'Code ISIN',
        'Maturit&eacute;': 'Maturite',
        "Date d'&eacute;mission": "Date emission",
        "Date d'&eacute;ch&eacute;ance": "Date echeance",
        'Taux Nominal %': 'Taux Nominal %',
        'Valeur Nominale': 'Valeur Nominale',
        'Encours': 'Encours',
        'Taux Issu de la Courbe %': 'Taux Issu de la Courbe %',
        'Prix Pied de Coupon %': 'Prix Pied de Coupon %',
        'Coupon Couru Unitaire': 'Coupon Couru Unitaire',
        'Prix': 'Prix',
        'Applicable': 'Applicable',
        'AMC': 'AMC'
    }

    # Rename the columns using the mapping
    db.drop(columns=[ 'Valeur Nominale ', 'Encours',
                     'Taux Issu de la Courbe %', 'Prix Pied de Coupon %',
                     'Coupon Couru Unitaire', 'Prix', 'Applicable', 'Code ISIN', 'Date Courbe'], inplace=True)
    db.rename(columns=column_mapping, inplace=True)
    return db

def open_portfolio(filepath):
    df=pd.read_excel(filepath, skiprows=9)
    # Replace "0" with 0.0 the number
    df.replace(0, np.nan, inplace=True)
    df.replace(np.nan, 0.0, inplace=True)

    return df