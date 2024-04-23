import numpy as np
import random
import sys

class ModeloDeputados:
    def __init__(self, cycles):
        self.cycles = cycles

    def output(self):
        np.set_printoptions(threshold=sys.maxsize)
        # Select columns to print
        columns_to_print = [0, 24, 48, 72, 96, 120, 144, 168, 192, 216]  # Example: columns 0, 1, and 2
        #columns_to_print = [0, 24, 48, 72, 96]  # Example: columns 0, 1, and 2

        # Print selected columns
        selected_columns = self.matrix[:, columns_to_print]
        print(f"Output: \n {selected_columns} \n Candidatos: {len(selected_columns)}")

    matrix = np.ones((70,1), dtype=int)
    
    out = []

    new_col = [[]]

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
        counter = 0    
        while(counter<self.cycles):
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
                    self.FillElections(col, 70-perdas)
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
            counter += 1