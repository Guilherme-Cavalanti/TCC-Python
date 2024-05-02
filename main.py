from model import ModeloDeputados
 
def main():
    Modelo = ModeloDeputados(1)
    Modelo.run()
    Modelo.output()
    # Modelo.PlotMatrix()
    Modelo.PlotSurvivalTime()

if __name__ == "__main__":
    main()