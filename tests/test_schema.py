import pandera.pandas as pa
import pytest

from src.mlops_projet.data.schema import validate_bank_data
from src.mlops_projet.data.load import load_bank_data

@pytest.fixture
def df():
    return load_bank_data()

def test_donnees_valide(df):
    validate_bank_data(df)

def test_colonne_renommee(df):
    casse=df.rename(columns={"balance":"solde"})
    with pytest.raises(pa.errors.SchemaErrors):
        validate_bank_data(casse)

def test_age_negatif(df):
    casse = df.copy()
    casse.loc[0,"age"]= -5
    with pytest.raises(pa.errors.SchemaErrors):
        validate_bank_data(casse)

def test_cible_inconue(df):
    casse = df.copy()
    casse[0,"y"] = "peut-être"
    with pytest.raises(pa.errors.SchemaErrors):
        validate_bank_data(casse)

def test_balance_aberrante(df):
    casse = df.copy()
    casse.loc[0, "balance"] = -50000
    with pytest.raises(pa.errors.SchemaErrors):
        validate_bank_data(casse)