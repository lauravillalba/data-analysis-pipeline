import pandas as pd
import src.functions as fn
import src.grafics as gr
from src.parser import parser
import src.pdfcreated as pdf

def main(country1, country2, year):

    df=fn.importa('./input/master.csv')

    print("LLAMANDO A WIKIPEDIA...")
    sunnyHours_dict_global= fn.dictHours('https://en.wikipedia.org/wiki/List_of_cities_by_sunshine_duration')
    df_global_index = fn.uniFrame(sunnyHours_dict_global)
    
    print("LLAMANDO A RESTCOUNTRIES...")
    df_capital = fn.capitalAPI("https://restcountries.eu/rest/v2/all?fields=name;capital")
    
    df_notNulls=fn.mergeOrigenCapital(df,df_capital)

    df_definitive=fn.generaDefinitives(df_global_index, df_notNulls)
    fn.exportCSV('./output/df_definitive.csv',df_definitive)

    df_countryYearTotal = fn.completNoSex(df_definitive)
    fn.exportCSV('./output/df_countryYearTotal.csv',df_countryYearTotal)

    df_countryYearSex = fn.tabSex(df_definitive)
    fn.exportCSV('./output/df_countryYearSex.csv',df_countryYearSex)
    
    print("GENERANDO GRÁFICOS...")
    
    colores1=['royalblue','lightsteelblue']
    colores2=['darkred','red']
    gr.generaGraf(country1,year,colores1)    
    gr.generaGraf(country2,year,colores2)

    gr.generaBarr(country1,country2,year)

    gr.historic(year)
    
    pdf.generaPDF(country1,country2,year)



if __name__ == "__main__":
    country1, country2, year = parser()
    
    if country1[0]==country2[0]:
        print("LOS PAISES TIENEN QUE SER DISTINTOS --> INTENTALO DE NUEVO")
        
    elif year[0]>2016 or year[0]<1985:
        print("EL AÑO DEBE ESTAR ENTRE 1985 Y 2016 --> INTENTALO DE NUEVO")
        
    else:
        main(country1[0], country2[0], year[0])
        
