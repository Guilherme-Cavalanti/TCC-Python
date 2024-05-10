from model import ModeloDeputados
from analysis import AnaliseDeputados
 
def main():

#Quantos Ciclos irá usar
    Ciclos = 10

#Criando Modelo 
    Modelo = ModeloDeputados(Ciclos)

#Rodando Modelo uma única vez e gerando gráficos
    # Modelo.run()

    ## Ver Output
    # Modelo.output()

    ## Ver gráfico da Matriz de Output
    # Modelo.PlotMatrix()

    ## Ver gráfico com períodos de sobrevivência de cada deputado
    #Modelo.PlotSurvivalTime()

##Rodando Modelo Completo com todos os ciclos
    Modelo.RunCycles()
    Modelo.CreateSurvivalMatrix()

    #Pegar Output dos ciclos
    DadosModelo = Modelo.GetSurvivalTimeData()

##Criando Analisador após criar todos os ciclos
    Analisador = AnaliseDeputados()

##Gerando Vetores de tempo de sobrevivência a partir dos Dados do Modelo
    Analisador.GenerateSurvivalPeriodMatrix(DadosModelo)

##Gerando a Matriz com os Hazard Rates Acumulativos
    Analisador.CreateHazardMatrix()

    # Pegar média e desvio padrão dos hazard rates
    Analisador.CreateMeanAndSTD()

    # Gerar Gráfico de Hazard Rates
    Analisador.PlotHazardRateGraph()



if __name__ == "__main__":
    main()