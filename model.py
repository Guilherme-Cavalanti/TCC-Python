import numpy as np
import random
import sys
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class ModeloDeputados:
    def __init__(self, cycles):
        self.cycles = cycles
        print(f"Modelo criado com {self.cycles} ciclos\n")

    def output(self):
        np.set_printoptions(threshold=sys.maxsize)
        # Select columns to print
        columns_to_print = [0, 24, 48, 72, 96, 120, 144, 168, 192, 216]  # Example: columns 0, 1, and 2
        #columns_to_print = [0, 24, 48, 72, 96]  # Example: columns 0, 1, and 2

        # Print selected columns
        selected_columns = self.matrix[:, columns_to_print]
        print(f"Output: \n {selected_columns} \n Candidatos: {len(selected_columns)}")

    def PlotMatrix(self):
        cmap_custom = mcolors.LinearSegmentedColormap.from_list("custom_binary", [(0, "white"), (0.5, "gray"), (1, "black")])

        shuffle_matrix = self.matrix.astype(float)
        np.random.shuffle(shuffle_matrix)

        for i in range (len(shuffle_matrix)):
            col = 216
            while(col>=0):
                if(shuffle_matrix[i][col]) == 1:
                    shuffle_matrix[i][col] = 0.5
                    col -=1
                else:
                    break
        plt.imshow(shuffle_matrix,cmap=cmap_custom,interpolation="nearest")
        plt.title("Matriz Deputados")
        plt.xlabel("Months")
        plt.ylabel("Deputies")
        plt.show()

    def PlotSurvivalTime(self):
        cmap_custom = mcolors.LinearSegmentedColormap.from_list("custom_binary", [(0, "white"), (0.5, "gray"), (1, "black")])
        new_matrix = self.matrix.astype(float)  

        for i in range (len(new_matrix)):
            col = 216
            while(col>=0):
                if(new_matrix[i][col]) == 1:
                    new_matrix[i][col] = 0.5
                    col -=1
                else:
                    break

        output_matrix = np.zeros((1,217),dtype=float)
        for i in range (len(new_matrix)):
            new_row =  np.zeros((1,217),dtype=float)
            count = 0
            for col in range(len(new_matrix[i])):
                if new_matrix[i][col] == 0.5:
                    new_row[0][count] = 0.5
                    count += 1
                    if col == 216:
                        output_matrix = np.vstack((output_matrix, new_row))
                elif new_matrix[i][col] == 1:
                    new_row[0][count] = 1
                    count += 1
                    if new_matrix[i][col+1] == 0:
                        output_matrix = np.vstack((output_matrix, new_row))
                        new_row =  np.zeros((1,217),dtype=float)
                        count = 0

        zero_counts = np.sum(output_matrix == 0,axis=1)

        sorted_indices = np.argsort(zero_counts)[::-1]  # Get the indices that would sort the array descendingly
        sorted_matrix = output_matrix[sorted_indices]

        plt.imshow(sorted_matrix,cmap=cmap_custom,interpolation="nearest")
        plt.title("Matriz Sobrevivência Deputados")
        plt.xlabel("Periods")
        plt.ylabel("Ranked Survival Times")
        plt.show()


    matrix = np.ones((70,1), dtype=int)

    new_col = [[]]

    def Reset(self):
        self.matrix = np.ones((70,1), dtype=int)
        self.new_col = [[]]

    def FillElections(self, col, vagas):
        atual = self.matrix[:, col]
        candidatos = []
        for i in range(len(atual)):
            if atual[i] == 0:
                candidatos.append(i)
        if len(candidatos) <= vagas:
            for candidato in candidatos:
                self.new_col[candidato] = 1
            if len(candidatos) == vagas:
                return
            resto = vagas - len(candidatos)
            for i in range(resto):
                self.new_col = np.vstack((self.new_col,[[1]]))
                line = np.zeros((1,col+1), dtype=int)
                self.matrix = np.vstack((self.matrix, line))
            return
        eleitos = random.sample(candidatos,vagas)
        for candidato in eleitos:
            self.new_col[candidato] = 1
        return
    def run(self):   
        month = 1
        while month <= 216:
            col = month-1
            self.new_col = np.zeros((len(self.matrix),1), dtype=int)
            if month == 24 or month == 72 or month == 120 or month == 168 or month == 216:
                for row in range(len(self.matrix)):
                    if self.matrix[row][col] == 1:
                        r = np.random.rand()
                        if r > 0.91:
                            self.new_col[row] = 0
                            line = np.zeros((1,month), dtype=int)
                            self.new_col = np.vstack((self.new_col,[[1]]))
                            self.matrix = np.vstack((self.matrix, line))
                            continue 
                        self.new_col[row] = 1
                self.matrix = np.hstack((self.matrix, self.new_col))
            elif month == 48 or month == 96 or month == 144 or month == 192:
                perdas = 0
                for row in range(len(self.matrix)):
                    if self.matrix[row][col] == 1:
                        r = np.random.rand()
                        if r > 0.53:
                            self.new_col[row] = 0
                            perdas += 1
                            continue 
                        self.new_col[row] = 1
                self.FillElections(col, perdas)
                self.matrix = np.hstack((self.matrix, self.new_col))
            else:
                for row in range(len(self.matrix)):
                    if self.matrix[row][col] == 1:
                        r = np.random.rand()
                        if r > 0.996:
                            self.new_col[row] = 0
                            line = np.zeros((1,month), dtype=int)
                            self.new_col = np.vstack((self.new_col,[[1]]))
                            self.matrix = np.vstack((self.matrix, line))
                            continue
                        self.new_col[row] = 1
                self.matrix = np.hstack((self.matrix, self.new_col))
            month +=1
    LoadedMatrices = []
    def RunCycles(self):
        self.LoadedMatrices = []
        counter = 0    
        while(counter<self.cycles):
            counter += 1
            self.Reset()
            self.run()
            self.LoadedMatrices.append(self.matrix)
            #self.output()
            print(f"Deputados usados no ciclo {counter}: {len(self.matrix)}")

        if len(self.LoadedMatrices) == self.cycles:
            print(f"{self.cycles} ciclos completados com sucesso!")

    SurvivalTimeData = []
    def CreateSurvivalMatrix(self):
        if len(self.LoadedMatrices) != self.cycles:
            print(f"Matrizes não carregadas, comprimento {len(self.LoadedMatrices)} para {self.cycles} ciclos")

        for m in range(len(self.LoadedMatrices)):   
            output_matrix = np.zeros((1,217),dtype=float)
            for i in range (len(self.LoadedMatrices[m])):
                new_row =  np.zeros((1,217),dtype=float)
                count = 0
                for col in range(len(self.LoadedMatrices[m][i])):
                    if self.LoadedMatrices[m][i][col] == 1:
                        new_row[0][count] = 1
                        count += 1
                        if col == 216:
                            output_matrix = np.vstack((output_matrix, new_row))
                        elif self.LoadedMatrices[m][i][col+1] == 0:
                            output_matrix = np.vstack((output_matrix, new_row))
                            new_row =  np.zeros((1,217),dtype=float)
                            count = 0
            output_matrix = output_matrix[1:]
            print(f"Linhas geradas para matriz {m+1}: {len(output_matrix)}")
            self.SurvivalTimeData.append(output_matrix)
        print(f"{len(self.SurvivalTimeData)} matrizes de tempo de sobrevivência geradas com sucesso!")   
    def GetSurvivalTimeData(self):
        if len(self.SurvivalTimeData) == self.cycles:
            return self.SurvivalTimeData
        else:
            print("Dados Não Carregados")
            return