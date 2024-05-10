import numpy as np
import matplotlib.pyplot as plt

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
        sum = np.sum(self.SurvivalPeriodMatrix[row])
        h = self.SurvivalPeriodMatrix[row][col]/sum
        return h
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
        print(f"\n Matriz com Hazard Rates Acumulativos criada com \n{len(self.HazardRateMatrix)} linhas")
    MeanArray = []
    STDArray = []
    def CreateMeanAndSTD(self):
        column_means = np.mean(self.HazardRateMatrix, axis=0)
        column_std = np.std(self.HazardRateMatrix, axis=0)
        self.MeanArray = column_means
        self.STDArray = column_std
    def PlotHazardRateGraph(self):
        plt.errorbar(x=np.arange(218),y=self.MeanArray,yerr=self.STDArray ,color="black", ecolor="gray")
        plt.title("Hazard Rates Acumulativos")
        plt.xlabel("Months")
        plt.ylabel("Probabilidade")
        plt.show()