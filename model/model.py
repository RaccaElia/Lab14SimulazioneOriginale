import copy

from database.DAO import DAO
from model.cromosoma import Cromosoma
import networkx as nx


class Model:
    def __init__(self):
        self._cromosomi = {}
        for row in DAO.getCromosomi():
            if row[0] in self._cromosomi.keys():
                self._cromosomi[row[0]].geni.append(row[1])
            else:
                self._cromosomi[row[0]] = Cromosoma(row[0], [row[1]])
        self._grafo = nx.DiGraph()
        self._cammino = []
        self._lunghezzaMax = 0

    def creaGrafo(self):
        self._grafo.add_nodes_from(self._cromosomi.keys())
        for crom1 in self._grafo.nodes:
            for crom2 in self._grafo.nodes:
                if crom1 != crom2:
                    peso = DAO.getArco(crom1, crom2)
                    if peso != 0:
                        self._grafo.add_edge(crom1, crom2)
                        self._grafo[crom1][crom2]["weight"] = peso

    def dettagliGrafo(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getMinMaxArco(self):
        min = 999
        max = 0
        for (crom1, crom2) in self._grafo.edges:
            peso = self._grafo[crom1][crom2]["weight"]
            if peso > max:
                max = peso
            if peso < min:
                min = peso
        return min, max

    def getArchiSoglia(self, soglia):
        cntMin = 0
        cntMax = 0
        for (crom1, crom2) in self._grafo.edges:
            if self._grafo[crom1][crom2]["weight"] < soglia:
                cntMin += 1
            elif self._grafo[crom1][crom2]["weight"] > soglia:
                cntMax += 1
        return cntMin, cntMax

    def trovaCammino(self, soglia):
        self._cammino = []
        self._lunghezzaMax = 0
        for nodo in self._grafo.nodes:
            self.ricorsione([nodo], soglia)
        return self._cammino, self._lunghezzaMax


    def ricorsione(self, parziale, soglia):
        nodiVicini = self.nodiEsplorabili(parziale, soglia)
        if nodiVicini == []:
            if self.calcolaLunghezza(parziale) > self._lunghezzaMax:
                self._lunghezzaMax = self.calcolaLunghezza(parziale)
                self._cammino = copy.deepcopy(parziale)
        else:
            for nodo in nodiVicini:
                if not self.arcoConsiderato(parziale[-1], nodo, parziale):
                    parziale.append(nodo)
                    self.ricorsione(parziale, soglia)
                    parziale.pop()

    def arcoConsiderato(self, n1, n2, lista):
        for i in range(len(lista)-1):
            if (n1, n2) == (lista[i], lista[i+1]):
                return True
        return False

    def nodiEsplorabili(self, lista, soglia):
        ris = []
        for vicino in self._grafo.neighbors(lista[-1]):
            if self._grafo[lista[-1]][vicino]["weight"] > soglia:
                ris.append(vicino)
        return ris

    def calcolaLunghezza(self, lista):
        ris = 0
        for i in range(len(lista)-1):
            ris += self._grafo[lista[i]][lista[i+1]]["weight"]
        return ris