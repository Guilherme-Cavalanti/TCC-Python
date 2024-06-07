import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class AnaliseDeputados:
    def __init__(self):
        print("\nAnalisador criado\n")

    SurvivalPeriodMatrix = []
    def GenerateSurvivalPeriodMatrix(self, SurvivalTimeData):
        for m in range(len(SurvivalTimeData)):
            newLine = np.zeros(218, dtype=int) 
            for row in range(len(SurvivalTimeData[m])):
                num_ones = np.count_nonzero(SurvivalTimeData[m][row] == 1)
                newLine[num_ones] += 1  
            self.SurvivalPeriodMatrix.append(newLine)
        print(f"Matriz com {len(self.SurvivalPeriodMatrix)} vetores criada.")
    def HazardRate(self, row, col):
        sum = np.sum(self.SurvivalPeriodMatrix[row][col:])
        if sum > 0:
            h = self.SurvivalPeriodMatrix[row][col]/sum
            return h 
        return 0
    def CumulativeHazardRate(self, row,col):
        if(col==0):
            return 0
        sum = 0
        for i in range(col):
            sum += self.HazardRate(row, i)
        H = sum+self.HazardRate(row,col)
        return H
    HazardRateMatrix = []
    def CreateHazardMatrix(self):
        for row in range(len(self.SurvivalPeriodMatrix)):
            newLine = np.zeros(218, dtype=float)
            teste = np.zeros(218, dtype=float)
            for col in range(len(self.SurvivalPeriodMatrix[row])):
                newLine[col] = self.CumulativeHazardRate(row,col)  
                teste[col] = self.HazardRate(row,col) 
            self.HazardRateMatrix.append(newLine)
        print(f"\nMatriz com Hazard Rates Acumulativos criada com {len(self.HazardRateMatrix)} linhas")
    MeanArray = []
    STDArray = []
    def CreateMeanAndSTD(self):
        column_means = np.mean(self.HazardRateMatrix, axis=0)
        column_std = np.std(self.HazardRateMatrix, axis=0)
        self.MeanArray = column_means
        print(f"\nMédia calculada para {len(self.MeanArray)} elementos")
        self.STDArray = column_std
        print(f"Desvio Padrão calculado para {len(self.STDArray)} elementos")
    ConfidenceIntervalErrors = []
    def CreateConfidenceIntervals(self):
        self.MeanArray[0] = 0.0000001
        self.STDArray[0] = 0.0000001
        n = len(self.MeanArray)
        confidence_level = 0.95

        lower_bounds = np.zeros_like(self.MeanArray)
        upper_bounds = np.zeros_like(self.MeanArray)
        for i in range(n):
            #CI = stats.norm.interval(confidence_level, loc=self.MeanArray[i], scale=self.STDArray[i] / np.sqrt(n))
            CI = stats.norm.interval(confidence_level, loc=self.MeanArray[i], scale=self.STDArray[i])
            lower_bounds[i], upper_bounds[i] = CI
        self.ConfidenceIntervalErrors = (upper_bounds - lower_bounds) / 2
        print(f"Gerados {len(self.ConfidenceIntervalErrors)} intervalos de confiança com sucesso\n")
    def PlotHazardRateGraph(self):
        plt.errorbar(x=np.arange(218),y=self.MeanArray,yerr=self.ConfidenceIntervalErrors ,color="black", ecolor="gray")
        plt.title("Hazard Rates Acumulativos")
        plt.xlabel("Months")
        plt.ylabel("Probabilidade")
        plt.show()
    
    def KaplanMeier(self,row,col):
        if(col==0):
            return 0
        S = 1
        for i in range(col):
            S*= 1 - self.HazardRate(row,i) 
        S *= 1 - self.HazardRate(row,col)   

        #Retornar função de sobrevivência 
        #return S
        #Retornar função de sobrevivência ao contrário
        return 1-S

    def GreenWoodError(self,row,col):
         # Inicializa a probabilidade de sobrevivência
        S = 1
        var_sum = 0
        for i in range(col + 1):
            hazard_rate = self.HazardRate(row, i)
            S *= 1- hazard_rate  # Multiplica pelo complemento da taxa de risco
            remaining_in_risk = sum(self.SurvivalPeriodMatrix[row][i:])
            num_exits = self.SurvivalPeriodMatrix[row][i]
            if remaining_in_risk > 0:
                var_sum += num_exits / (remaining_in_risk * (remaining_in_risk - num_exits))
        
        var = (S)**2 * var_sum
        se = np.sqrt(var)
        return se

    ProductMatrix = []
    GreenWoodMatrix = []

    def CreateProductMatrix (self):
        for row in range(len(self.SurvivalPeriodMatrix)):
            newLine = np.zeros(218, dtype=float)
            newLineGreenWood = np.zeros(218, dtype=float)
            for col in range(len(self.SurvivalPeriodMatrix[row])):
                newLine[col] = self.KaplanMeier(row,col)  
                newLineGreenWood[col] = self.GreenWoodError(row,col) 
            self.ProductMatrix.append(newLine)
            self.GreenWoodMatrix.append(newLineGreenWood)
        print(f"\nMatriz com Hazard Rates Acumulativos criada com {len(self.HazardRateMatrix)} linhas")

    MeanProductArray = []
    GreenWoodErrorArray = []

    def CreateProductMeanAndSTD (self):
        column_means = np.mean(self.ProductMatrix, axis=0)
        greenwood_means = np.mean(self.GreenWoodMatrix, axis=0)
        self.MeanProductArray = column_means
        print(f"\nMédia de produto limite calculada para {len(self.MeanProductArray)} elementos")
        self.GreenWoodErrorArray = greenwood_means
        print(f"Erro Greenwood médio calculado para {len(self.GreenWoodErrorArray)} elementos")

    def PlotSurvivorFunction (self):
        plt.errorbar(x=np.arange(218),y=self.MeanProductArray,yerr=self.GreenWoodErrorArray ,color="black", ecolor="gray")
        plt.title("Função de Sobrevivência")
        plt.xlabel("Months")
        plt.ylabel("Probabilidade")
        plt.show()