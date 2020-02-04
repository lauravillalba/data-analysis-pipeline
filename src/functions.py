import pandas as pd
import json
import requests
import src.functions as fn
from bs4 import BeautifulSoup

#--------------------------------Import DataSet-------------------------------------
def importa(path):
    df =pd.read_csv(path)
    return df

#------------------------------Scrapping Wikipedia----------------------------------

def sunnyHours(lista):
    m = lista.find_all("td")
    return {
        "country":m[0].find("a").text.strip(),
        "city":m[1].find("a").text.strip(),
        "jan":float(m[2].text),
        "feb":float(m[3].text),
        "mar":float(m[4].text),
        "apr":float(m[5].text),
        "may":float(m[6].text),
        "jun":float(m[7].text),
        "jul":float(m[8].text),
        "ago":float(m[9].text),
        "sep":float(m[10].text),
        "oct":float(m[11].text),
        "nov":float(m[12].text),
        "dic":float(m[13].text)
     }


def dictHours(url):
    data=requests.get(url).text
    soup= BeautifulSoup(data, 'html.parser')
    
    sunnyHours_dict_global=[]
    for e in range (0,6):
        sunnyHours_table = soup.select('table.wikitable')[e]
        sunnyHours_dict = [fn.sunnyHours(fila) for fila in sunnyHours_table.find_all("tr")[1:]]
        sunnyHours_dict_global.append(sunnyHours_dict)
    return sunnyHours_dict_global

def uniFrame(sunnyHours_dict_global):
    df_africa=pd.DataFrame(sunnyHours_dict_global[0])
    df_asia=pd.DataFrame(sunnyHours_dict_global[1])
    df_europe=pd.DataFrame(sunnyHours_dict_global[2])
    df_north_central_america=pd.DataFrame(sunnyHours_dict_global[3])
    df_south_america=pd.DataFrame(sunnyHours_dict_global[4])
    df_oceania=pd.DataFrame(sunnyHours_dict_global[5])
    
    frames = [df_africa,df_asia, df_europe,df_north_central_america,df_south_america,df_oceania]
    df_global = pd.concat(frames)
    df_global.sort_values(by=['country'],inplace=True)
    df_global_index = (df_global.reset_index()).drop(['index'], axis=1)
    return df_global_index

#------------------------------------API-----------------------------------------

def capitalAPI(urlAPI):
    capital_json= requests.get(urlAPI)
    capital=capital_json.json()
    df_capital=pd.DataFrame(capital)
    df_capital.rename(columns={'name':'country'}, inplace=True)
    df_capital['country'].replace(['United States of America','United Kingdom of Great Britain and Northern Ireland',
                               'Saint Vincent and the Grenadines','Korea (Republic of)'], 
                              ['United States','United Kingdom','Saint Vincent and Grenadines',
                               'Republic of Korea'],inplace=True)
    df_capital['capital'].replace(["Saint John's","Washington, D.C.","Ottawa","Reykjavík","Jerusalem","Ulan Bator",
                                "Bern","Abu Dhabi"],["Saint Johns", "Washington,D.C.","Toronto","Reykjavik",
                                    "Tel Aviv","Ulaanbaatar","Zurich","Dubai"],inplace=True)
    return df_capital


#-------------------Merge df origen y df_capital + cleaning ---------------------

'''def nullPerColumns(frame):
    for col, numnulls in frame.isnull().sum().items():
        if numnulls > 0:
            (f"{col} {numnulls}")'''

def mergeOrigenCapital (df_origen,df_capital):
    df_mix=pd.merge(df_origen, df_capital, how='left',on='country')
    #fn.nullPerColumns(df_mix)
    # display(df_mix[(df_mix["capital"].isnull()==True)]) --> Muestra Macau con valores nulos
    df_notNulls = df_mix[df_mix.country != 'Macau']
    return df_notNulls

#----------------Merge df_notNulls y df_global_index + cleaning -------------------

def generaDefinitives(df_global_index, df_notNulls):
    df_sunnyCapital=df_global_index.rename(columns= {'city':'capital'})
    df_sunny=pd.merge(df_notNulls, df_sunnyCapital,how='left', on='capital')
    
    df_muchCleaned = df_sunny.dropna(subset=['jan'])
    df_megaCleaned=(df_muchCleaned.reset_index()).drop(['index'], axis=1)
    df_megaCleaned.rename(columns={'country_x':'country', 'capital':'city',' gdp_for_year ($) ':'gdp_for_year','gdp_per_capita ($)':'gdp_per_capita'}, inplace=True)

    df_megaCleaned['total'] = df_megaCleaned['jan']+df_megaCleaned['feb']+df_megaCleaned['mar']+df_megaCleaned['apr']+df_megaCleaned['may']+df_megaCleaned['jun']+df_megaCleaned['jul']+df_megaCleaned['ago']+df_megaCleaned['sep']+df_megaCleaned['oct']+df_megaCleaned['nov']+df_megaCleaned['dic']

    df_definitive = df_megaCleaned[['country','year','total', 'sex', 'suicides_no', 'population']]

    return df_definitive

#----------------------------------------Tablas finales -------------------------------------------

def completNoSex(df_definitive):
    #Genera df con país y total horas de luz por año:
    df_countryTotal=df_definitive[['country','total']].drop_duplicates(['country']).reset_index().drop(['index'], axis=1)

    #Genera df agrupado país, año y sumatorios:
    df_countryYear=df_definitive[['country','year','suicides_no','population']].groupby(by=['country','year']).sum().reset_index()

    #Genera df completo de los dos anteriores (país, año,horas de luz y sumatorios):
    df_countryYearTotal=pd.merge(df_countryYear, df_countryTotal,how='left', on='country')
    df_countryYearTotal['ratio']=((df_countryYearTotal['suicides_no']/df_countryYearTotal['population'])*100)*100000

    return df_countryYearTotal


def tabSex(df_definitive):
    #Genera df con país, año, sexo y sumatorios:
    df_countryYearSex=df_definitive[['country','year','sex','suicides_no','population']].groupby(by=['country','year','sex']).sum().reset_index()
    
    return  df_countryYearSex


def exportCSV (path,dataframe):
    dataframe.to_csv(path)
    

