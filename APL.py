import json

from pFactor import getPFactorData
from sheets import updateSheets


def APL():

    user = input("AniList username: ")
    sheetId = input("Google Sheets ID: ")

    p_factor_data = getPFactorData(user)

    updateSheets(sheetId, p_factor_data)
