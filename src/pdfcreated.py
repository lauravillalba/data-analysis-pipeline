from fpdf import FPDF 
import pandas as pd 
import data

def generaPDF(country1,country2,year):

    pdf = FPDF('L','mm','A4')
    pdf.add_page()

    pdf.set_font('Courier', 'B', 20)

    pdf.cell(270, 15, '¿INFLUYE EL NÚMERO DE HORAS DE LUZ EN EL ÍNDICE DE SUIDICIOS?',1,1,'C')

    pdf.set_font("Courier",'',14)
    pdf.cell(90,10, f'{country1}_{year}',1,0,'C')
    pdf.set_font("Courier",'',14)
    pdf.cell(90,10, f'Horas de luz vs ratio en {year}',1,0,'C')
    pdf.set_font("Courier",'',14)
    pdf.cell(90,10, f'{country2}_{year}',1,1,'C')


    #pdf.set_text_color(198,21,21)
    pdf.cell(90,65,'',1,0,'C')
    pdf.image(f'output/SUICIDES_SEX_{year}_{country1}.png', 14, 40,h=55)

    #pdf.set_text_color(198,21,21)
    pdf.cell(90,65,'',1,0,'C')
    pdf.image(f'output/TOTAL_HORAS_RATIO_{year}.png', 108, 40,h=55)


    #pdf.set_text_color(198,21,21)
    pdf.cell(90,65,'',1,1,'C')
    pdf.image(f'output/SUICIDES_SEX_{year}_{country2}.png', 195, 40,h=55)


    pdf.set_font("Courier",'',14)
    pdf.cell(270,10, f'Todos los países - {year}',1,1,'C')
    pdf.set_text_color(198,21,21)
    pdf.cell(270,70,'',1,1,'C')
    pdf.image(f'output/HISTORICO_{year}.png', 50, 120,w=200,h=55)


    return pdf.output(f'output/informe_{country1}_{country2}_{year}.pdf','F')