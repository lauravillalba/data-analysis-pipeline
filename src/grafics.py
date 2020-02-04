import pandas as pd
import src.grafics as gr
import src.functions as fn
import matplotlib.pyplot as plt
from matplotlib import colors

def generaGraf(country,year,colores):
    #Genera estadística de los dos países según sexo el año indicado:
    df_countryYearSex=fn.importa('./output/df_countryYearSex.csv')
    
    df_yearSex=df_countryYearSex.loc[df_countryYearSex['year'] == year]
    df_yearcountry=df_yearSex.loc[df_yearSex['country']== country]
    
    s=df_yearcountry.groupby('sex').agg ({'suicides_no':'sum'
                                    }).sort_values(by=['suicides_no'])
    
    print(F'\n\nSUICIDES PER SEX {year} in {country}:\n {s}')
    sex=['male','female']
    num_suicides=[s['suicides_no']['male'],s['suicides_no']['female']]

    explode=[0,0.3]
    
    plt.figure()
    plt.pie(num_suicides,labels=sex,explode=explode, autopct="%0.1f %%", colors=colores)  
    #plt.title(f'SUICIDES PER SEX {year} in {country}')
    plt.savefig(f'output/SUICIDES_SEX_{year}_{country}.png')


def generaBarr(country1,country2,year):
    df_countryYearTotal=fn.importa('./output/df_countryYearTotal.csv')
    
    df_yearCountry=df_countryYearTotal.loc[df_countryYearTotal['year'] == year]

    df_yearCountry1=df_yearCountry.loc[df_yearCountry['country']== country1]
    df_yearCountry2=df_yearCountry.loc[df_yearCountry['country']== country2]

    concat=pd.concat([df_yearCountry1,df_yearCountry2])
    
    q=concat.groupby('country').agg ({'total':'sum',
                                    'ratio':'sum'
                                    }).sort_values(by=['total'])
    print(f'\n\nTOTAL HORAS DE LUZ VS RATIO EN {year}\n {q} ')
    plt.figure()
    q.plot.bar()
    #plt.title(f'TOTAL HORAS DE LUZ VS RATIO EN {year} ')
    plt.savefig(f'output/TOTAL_HORAS_RATIO_{year}.png')


def historic(year):
    df_countryYearTotal=fn.importa('./output/df_countryYearTotal.csv')

    h =(df_countryYearTotal.groupby("country").agg({
                                                    "total":"sum", 
                                                    "ratio":"sum"
                                            }).sort_values(by=['ratio']))
    print(f'\n\nRESUMEN TODOS LOS PAISES EN {year} \n{h}')
    plt.figure()
    h.plot.bar()
    #plt.title(f'TOTAL DE HORAS DE LUZ EN VS RATIO {year} \n TODOS LOS PAISES ')
    plt.savefig(f'output/HISTORICO_{year}.png')

'''def historic(country):
    df_countryYearTotal=fn.importa('./output/df_countryYearTotal.csv')
    
    df_histoCountry=df_countryYearTotal.loc[df_countryYearTotal['country']== country]
    print('Aquí!!\n',df_histoCountry)
    h =(df_histoCountry.groupby("year").agg({
                                            "suicides_no":"sum"
                                            }).sort_values(by=['year']))
    print(f'\n\HISTORICO DE {country} \n{h}')
    plt.figure()
    h.plot.bar()
    #plt.title(f'HISTORICI DE {country} \n')
    plt.savefig(f'output/HISTORICO_{country}.png')'''
    
