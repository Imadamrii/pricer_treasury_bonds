import pandas as pd
from datetime import datetime, date



def get_duree_dernier_coupon(date_valeur, date_emission):
# Convertir les dates en objets datetime
    if not isinstance(date_valeur, datetime):
        date_valeur = datetime.combine(date_valeur, datetime.min.time())

    if not isinstance(date_emission, datetime):
        date_emission = datetime.strptime(date_emission, "%d/%m/%Y")

        
        
    # Vérification de la date du dernier coupon
    if date_emission.month < date_valeur.month:
        date_dernier_coupon = date_emission.replace(year=date_valeur.year)
    elif date_emission.month == date_valeur.month:
        if date_emission.day <= date_valeur.day:
            date_dernier_coupon = date_emission.replace(year=date_valeur.year)
        else:
            date_dernier_coupon = date_emission.replace(year=date_valeur.year - 1)
    else:
        date_dernier_coupon = date_emission.replace(year=date_valeur.year - 1)
    print("date dernier coupon :",date_dernier_coupon)
    # Calcul de la durée écoulée en jours depuis le dernier paiement
    duree_ecoule = (date_valeur - date_dernier_coupon).days
    duree_ecoule_years = duree_ecoule / 365
    return duree_ecoule_years
    
def present_value(taux_nominal, taux_courbe, maturite_residuelle, nominal):
    # Règle le problème de maturité non entière. On calcule ici la valeur nette actuelle
    # en revenant à la date du dernier coupon : la maturité devient entière !
   
    if not isinstance(taux_nominal, float):
        taux_nominal= float(taux_nominal.replace(',', '.'))
    taux_courbe=float(taux_courbe)

    
    # Si la maturité est décimale, on arrondit à l'entier supérieur pour le calcul.
    if int(maturite_residuelle) != maturite_residuelle:
        new_maturity = int(maturite_residuelle) + 1
    else:
        new_maturity = int(maturite_residuelle)

    # On calcule le coupon.
    coupon = taux_nominal * nominal

    # Création de la liste des coefficients d'actualisation pour chaque période.
    liste_coef = [1 / ((1 + taux_courbe) ** i) for i in range(1, new_maturity + 1)]
    
    # Calcul de la valeur actuelle du principal à maturité.
    present_value_principal = nominal / ((1 + taux_courbe) ** new_maturity)

    # Calcul de la valeur actuelle de chaque coupon.
    liste_coupon = [coupon * coef for coef in liste_coef]
    
    # Liste des flux de paiement, comprenant les coupons et le principal à maturité.
    liste_paiement = liste_coupon + [present_value_principal]

    # Somme des flux de paiement pour obtenir la valeur nette actuelle.
    return sum(liste_paiement)
    
def dirty_price(taux_nominal, taux_courbe, maturite_residuelle, nominal,date_valeur,date_emission):
    """
    Calcule le prix sale (dirty price) d'une obligation en tenant compte de la maturité résiduelle et des dates
    de valeur et d'émission.

    Arguments :
        taux_nominal (float) : Taux nominal de l'obligation (exprimé en pourcentage, par exemple 5.15 pour 5.15%)
        taux_courbe (float) : Taux issu de la courbe des taux (Yield to Maturity - YTM) utilisé pour actualiser les flux futurs
        maturite_residuelle (float) : Durée restante jusqu'à la maturité de l'obligation en années
        nominal (float) : Valeur nominale de l'obligation
        date_valeur (str) : Date de valeur de l'obligation au format "jj/mm/aaaa"
        date_emission (str) : Date d'émission de l'obligation au format "jj/mm/aaaa"

    Returns :
        dirty_price (float) : Le prix sale (dirty price) de l'obligation
    """
    # Calcul de la valeur nette actuelle de l'obligation
    PV = present_value(taux_nominal, taux_courbe, maturite_residuelle, nominal)

    # Vérifie si la maturité résiduelle est décimale
    if maturite_residuelle != int(maturite_residuelle):
        print("date_valeur",date_valeur,"date_emission",date_emission)
        duree_ecoule_years=get_duree_dernier_coupon(date_valeur,date_emission)

        # Calcul du dirty price en utilisant la partie décimale de la maturité résiduelle
        dirty_price = PV * ((1 + taux_courbe) ** duree_ecoule_years)
        return dirty_price
    else:
        # Si la maturité résiduelle est entière, le dirty price est égal à la valeur nette actuelle
        return PV

    


def clean_price(taux_nominal, taux_courbe, maturite_residuelle, nominal,date_valeur,date_emission):
    # Calcul du dirty price en appelant la fonction dirty_price
    dirty = dirty_price(taux_nominal, taux_courbe, maturite_residuelle, nominal,date_valeur,date_emission)

    # Vérifie si la maturité résiduelle est décimale 
    if maturite_residuelle != int(maturite_residuelle):
        # Calcul du coupon
        coupon = nominal * taux_nominal

        duree_depuis_dernier_coupon=get_duree_dernier_coupon(date_valeur,date_emission)
        
        # Calcul des intérêts courus (pieds de coupon) en utilisant la partie décimale de la maturité résiduelle
        pieds_coupon = coupon * duree_depuis_dernier_coupon
        # Calcul du clean price en soustrayant les intérêts courus du dirty price
        clean_price_ = dirty - pieds_coupon

        return clean_price_
    else:
        # Si la maturité résiduelle est entière, le clean price est égal au dirty price
        return dirty



import numpy_financial as npf
from datetime import datetime

def get_date_dernier_coupon(date_valeur, date_emission):
    # Convertir les dates en objets datetime
    if not isinstance(date_valeur, datetime):
        date_valeur = datetime.combine(date_valeur, datetime.min.time())

    if not isinstance(date_emission, datetime):
        date_emission = datetime.strptime(date_emission, "%d/%m/%Y")

    # Vérification de la date du dernier coupon
    if date_emission.month < date_valeur.month:
        date_dernier_coupon = date_emission.replace(year=date_valeur.year)
    elif date_emission.month == date_valeur.month:
        if date_emission.day <= date_valeur.day:
            date_dernier_coupon = date_emission.replace(year=date_valeur.year)
        else:
            date_dernier_coupon = date_emission.replace(year=date_valeur.year - 1)
    else:
        date_dernier_coupon = date_emission.replace(year=date_valeur.year - 1)
        print("date_dernier_coupon", date_dernier_coupon)
    # Calculate the fraction of the year that has passed since the last payment
    days_since_last_payment = (date_valeur - date_dernier_coupon).days
    fraction_of_year = days_since_last_payment / 365.0
    
    return date_dernier_coupon, fraction_of_year

def calculate_bond_prices(date_valeur, date_emission, date_maturite, taux_nominal, yield_to_maturity):
    # Calculate time to maturit

    # Calculate the date of the last coupon payment and the fraction of the year since then
    date_dernier_coupon, fraction_of_year = get_date_dernier_coupon(date_valeur, date_emission)
    # Calculate the number of coupon payments that have occurred before date_valeur
    num_coupons_payed = (date_dernier_coupon.year - date_emission.year)
    num_coupons_total= (date_maturite.year - date_emission.year)
    num_coupons_left= num_coupons_total-num_coupons_payed
    # Create cash flows for bond
    cash_flows = [taux_nominal * 100000] * num_coupons_left
    cash_flows[-1] += 100000  # Face value at maturity

    # Calculate bond prices using numpy_financial
    present_value_ = npf.npv(rate=yield_to_maturity, values=cash_flows)
    clean_price_ = present_value_/((1+yield_to_maturity)^(1-fraction_of_year))
    gross_price_ = clean_price_ + (cash_flows[0] * fraction_of_year)

    return clean_price_, gross_price_



# Sample input
date_valeur = datetime.strptime("2023-08-04", "%Y-%m-%d")
date_emission = datetime.strptime("2004-04-05", "%Y-%m-%d")
date_maturite = datetime.strptime("2024-04-05", "%Y-%m-%d")
taux_nominal = 0.05  # 5%
yield_to_maturity = 0.04  # 4%


import QuantLib as ql

def calculate_bond_prices(issue_date, maturity_date, current_date, coupon_rate, yield_to_maturity, face_value=100000.0):
    calendar = ql.NullCalendar()
    day_count = ql.ActualActual(ql.ActualActual.ISMA)
    business_convention = ql.Unadjusted
    
    # Create QuantLib dates
    ql_issue_date = ql.Date(issue_date.day, issue_date.month, issue_date.year)
    ql_maturity_date = ql.Date(maturity_date.day, maturity_date.month, maturity_date.year)
    ql_current_date = ql.Date(current_date.day, current_date.month, current_date.year)

    # Create the fixed-rate bond
    schedule = ql.Schedule(ql_issue_date, ql_maturity_date, ql.Period(ql.Annual), calendar, business_convention, business_convention, ql.DateGeneration.Backward, False)
    bond = ql.FixedRateBond(0, calendar, face_value, ql_issue_date, ql_maturity_date, ql.Period(ql.Annual), [coupon_rate], day_count, business_convention, business_convention)

    # Set market convention and yield to maturity
    yield_curve = ql.FlatForward(ql_current_date, ql.QuoteHandle(ql.SimpleQuote(yield_to_maturity)), day_count, ql.Compounded, ql.Annual)
    bond.setPricingEngine(ql.DiscountingBondEngine(ql.YieldTermStructureHandle(yield_curve)))

    # Calculate prices
    accrued_interest = bond.accruedAmount(ql_current_date)
    clean_price_ = bond.cleanPrice()
    dirty_price_ = clean_price_ + accrued_interest

    return accrued_interest, clean_price_, dirty_price_

# # Example usage
# issue_date = ql.Date(1, 1, 2020)
# maturity_date = ql.Date(1, 1, 2030)
# current_date = ql.Date(4, 8, 2023)
# coupon_rate = 0.05
# yield_to_maturity = 0.04

# prices = calculate_bond_prices(issue_date, maturity_date, current_date, coupon_rate, yield_to_maturity)
# for key, value in prices.items():
#     print(key + ":", value)

