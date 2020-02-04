from argparse import ArgumentParser

def parser():
    parser = ArgumentParser(description="Análisis sobre la afectación de las horas de luz en el número de suicidios")

    parser.add_argument ("country1", type=str, nargs=1)
    parser.add_argument ("country2", type=str, nargs=1)
    parser.add_argument ("year", type=int, nargs=1)

    args = parser.parse_args()
    year = args.year
    country1 = args.country1
    country2 = args.country2

    return country1, country2, year