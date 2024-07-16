import heapq
import queue
import json
import time
def generare_harta(json_fisier):
    with open(json_fisier, 'r') as fisier:
        date_json = json.load(fisier)

    harta = date_json['Harta']
    return harta

def generare_distante(json_fisier):
    with open(json_fisier, 'r') as fisier:
        date_json = json.load(fisier)

    distante = date_json['Bucharest']
    return distante

def generare_input(txt_fisier):
    stare_initiala = ''
    stare_finala = ''
    with open(txt_fisier, 'r') as file:
        for line in file:
            if line.startswith("StareInitiala:"):
                stare_initiala = line.split(':')[1].strip()
            if line.startswith("StareFinala:"):
                stare_finala = line.split(':')[1].strip()
    return stare_initiala, stare_finala


class Nod:
    def __init__(self, oras, cost=0, distanta=0, parinte=None):
        self.oras = str(oras)
        self.distanta = str(distanta)
        self.cost = cost
        self.parinte = parinte if parinte is not None else self.oras

class priorityQueue:
    def __init__(self):
        self.orase = []

    def push(self, oras, cost):
        heapq.heappush(self.orase, (cost, oras))

    def pop(self):
        return heapq.heappop(self.orase)[1]
    def isEmpty(self):
        if (self.orase == []):
            return True
        else:
            return False

    def check(self):
        print(self.orase)

class ProblemaDrum:
    def __init__(self, harta, distante, stari):
        self.harta = harta
        self.stare_initiala = stari[0]
        self.stare_finala = stari[1]
        self.succesori_curenti = []
        self.distante = distante

    def initializeaza_stare(self):
        return self.stare_initiala

    def is_stare_finala(self, stare):
        return stare == self.stare_finala

    def este_stare_valida(self, stare):
        return stare in self.harta

    def aplica_tranzitii(self, stare_curenta):
        succesori_oras = []
        if self.este_stare_valida(stare_curenta):
            if stare_curenta in self.harta:
                succesori_oras = list(self.harta[stare_curenta].keys())
        return succesori_oras

    def heuristic(self, nod, valori):
        return valori[nod]

def afisare_drum(cale, stare_finala, vizitate, timp):
    drum = cale[stare_finala]

    print(f"Drumul de la {drum[0]} la {stare_finala} se realizeaza astfel: ")
    print("=======================================================")
    for i in range(len(drum) - 1):
        print(f"De la {drum[i]} la {drum[i+1]}")
    print(f"Adancimea la care s-a gasit solutia este {len(drum)-1}")
    print(f"Numarul total de noduri explorate este {vizitate}")
    print(f"Durata totala a algoritmului pentru problema abordata este de {timp}")

def afiseazaDrum(problema, cale, distance, vizitate, timp):
    finalcale = []
    i = problema.stare_finala
    while (cale.get(i) != None):
        finalcale.append(i)
        i = cale[i]
    finalcale.append(problema.stare_initiala)
    finalcale.reverse()

    print(f"Drumul de la {finalcale[0]} la {problema.stare_finala} se realizeaza astfel: ")
    print("=======================================================")
    for i in range(len(finalcale) - 1):
        print(f"De la {finalcale[i]} la {finalcale[i + 1]} cu costul de {distance[finalcale[i+1]]}")

    print(f"Adancimea la care s-a gasit solutia este {len(finalcale) - 1}")
    print(f"Numarul total de noduri explorate este {vizitate}")
    print(f"Durata totala a algoritmului pentru problema abordata este de {timp}")


def CautareBFS(problema, stare_initiala):
    start_time = time.time()
    nod_stare_init = Nod(stare_initiala)
    frontiera = [nod_stare_init]
    vizitate = []
    cale = {nod_stare_init.oras: [nod_stare_init.oras]}  # Dict

    while frontiera:
        stare_curenta = frontiera.pop(0)
        vizitate.append(stare_curenta.oras)

        if problema.is_stare_finala(stare_curenta.oras):
            afisare_drum(cale, problema.stare_finala, len(vizitate), time.time()-start_time)
            print("SUCCES")
            return

        succesori = problema.aplica_tranzitii(stare_curenta.oras)
        for s in succesori:
            if s not in [node.oras for node in frontiera] and s not in vizitate:
                new_node = Nod(s, 0, 0, stare_curenta)
                # print(new_node.parinte.oras, new_node.oras)
                frontiera.append(new_node)
                cale[new_node.oras] = cale[new_node.parinte.oras] + [new_node.oras]

    print("EȘEC")


def astar(problema, stare_initiala):
    start_time = time.time()
    frontiera = priorityQueue()
    frontiera.push(stare_initiala, 0)
    vizitate = []
    cale = {}
    distante = {}
    distante[stare_initiala] = 0
    cale[stare_initiala] = None
    while not frontiera.isEmpty():
        stareCurenta = frontiera.pop()
        vizitate.append(stareCurenta)
        if problema.is_stare_finala(stareCurenta):
            # afisare_drum(cale, problema.stare_finala, len(vizitate), time.time()-start_time)
            afiseazaDrum(problema, cale, distante, len(vizitate), time.time()-start_time)
            print("SUCCES")
            return

        succesori = problema.aplica_tranzitii(stareCurenta)
        for s in succesori:
            g_cost = distante[stareCurenta] + int(problema.harta[stareCurenta][s])
            # print(s, int(problema.harta[stareCurenta][s]), "now : " + str(distante[stareCurenta]), g_cost)

            if (s not in distante or g_cost < distante[s]):

                f_cost = g_cost + problema.heuristic(s, problema.distante)
                distante[s] = g_cost
                frontiera.push(s, f_cost)
                cale[s] = stareCurenta
    print("ESEC")
def astar(problema, stare_initiala):
    start_time = time.time()
    frontiera = priorityQueue()
    frontiera.push(stare_initiala, 0)
    vizitate = []
    cale = {}
    distante = {}
    distante[stare_initiala] = 0
    cale[stare_initiala] = None
    while not frontiera.isEmpty():
        stareCurenta = frontiera.pop()
        vizitate.append(stareCurenta)
        if problema.is_stare_finala(stareCurenta):
            # afisare_drum(cale, problema.stare_finala, len(vizitate), time.time()-start_time)
            afiseazaDrum(problema, cale, distante, len(vizitate), time.time()-start_time)
            print("SUCCES")
            return

        succesori = problema.aplica_tranzitii(stareCurenta)
        for s in succesori:
            g_cost = distante[stareCurenta] + int(problema.harta[stareCurenta][s])
            # print(s, int(problema.harta[stareCurenta][s]), "now : " + str(distante[stareCurenta]), g_cost)

            if (s not in distante or g_cost < distante[s]):

                f_cost = g_cost + problema.heuristic(s, problema.distante)
                distante[s] = g_cost
                frontiera.push(s, f_cost)
                cale[s] = stareCurenta
    print("ESEC")

def main():
    harta = generare_harta('harta.json')
    distante = generare_distante('distanteBucuresti.json')

    #input usor
    # problema = ProblemaDrum(harta, distante, generare_input('input_1'))
    # stare_initiala = problema.initializeaza_stare()
    # CautareBFS(problema, stare_initiala)
    # astar(problema, stare_initiala)

    #input imposibil
    # problema = ProblemaDrum(harta, distante, generare_input('input_2'))
    # stare_initiala = problema.initializeaza_stare()
    # CautareBFS(problema, stare_initiala)
    # astar(problema, stare_initiala)

    #input greu
    problema = ProblemaDrum(harta, distante, generare_input('input_3'))
    stare_initiala = problema.initializeaza_stare()
    CautareBFS(problema, stare_initiala)
    astar(problema, stare_initiala)

if __name__ == "__main__":
    main()