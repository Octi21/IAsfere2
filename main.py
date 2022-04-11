import time
import copy
import itertools
import os
import sys
import math
import heapq

class parcurgeNod:
    gr = None      # ob graph

    def __init__(self, id, info, matSchimbari, sfere, parent, cost=0, h=0):
        self.id = id
        self.info = info
        self.sfere = sfere      # lista de liste de pozitii bile
        self.parent = parent
        self.g = cost
        self.h = h
        self.f = self.h + self.g

        self.info2 = copy.deepcopy(gr.matGraf)      # pt a reprezenta cu .#%@ matricea
        for poz in self.sfere:
            if poz in gr.scopuri:
                self.info2[poz[0]][poz[1]] = "%"
            else:
                self.info2[poz[0]][poz[1]] = "@"
        if id == 1:
            self.matSchimbari = gr.marModif          # pt a retine micsorarea unui turn
        else:
            self.matSchimbari = matSchimbari

        # for linie in self.matSchimbari:
        #     print(linie)



    def obtineDrum(self):
        l = [self]
        nodCurent = self
        while nodCurent.parent is not None:
            nodCurent = nodCurent.parent
            l.insert(0,nodCurent)
        return l

    def afisDrum(self):
        l = self.obtineDrum()
        sir = ""
        for nod in l:
            print(str(nod))
            sir += str(nod)
        return len(l) , sir

    def contineInDrum(self, sfereNodNou):
        nodDrum = self
        while nodDrum is not None:
            if (sfereNodNou == nodDrum.sfere):
                return True
            nodDrum = nodDrum.parent

        return False

    def __gt__(self, other):            # operatorul > pt f si daca sunt egale ret cul cu g mai mic
        if self.f == other.f:
            return self.g < other.g
        return self.f > other.f

    def __repr__(self):
        sir = ""
        sir = sir + str(self.sfere)
        return sir

    def __str__(self):              #afisare ca in exemplu
        sir = str(self.id) + ")\n"
        if self.parent != None:                 # pt a afisa schimbarile turnurilor se face rap cu parintele
            mat1 = self.matSchimbari
            mat2 = self.parent.matSchimbari
            l = len(mat1)
            for i in range(l):
                for j in range(l):
                    if mat1[i][j] != mat2[i][j]:
                        sir += "turnul (" + str(i) +","+str(j)+") " + "a scazut cu " + str(mat1[i][j] - mat2[i][j] ) + "\n"
            sir += 'afis noduri modif\n'
        sir += "cost:" +str(self.g) + "\nMat turn: \n"
        for linie in self.info:             # afis mat h turnuri
            for elem in linie:
                sir += str(elem) + " "
            sir += "\n"
        sir += "Mat sfere: \n"
        for linie in self.info2:           # afis reprezentare .@#%
            for elem in linie:
                sir += str(elem) + " "
            sir += "\n"
        return sir

    # def __gt__(self, other):
    #     if self.f == other.f:
    #         return self.g < other.g
    #     return self.f > other.f


class Graph:

    def __init__(self,numeFisier):  #constructor cu nume fisier
        f = open(numeFisier,'r')
        primaLin = f.readline()
        l = primaLin.split()
        self.k = int(l[0])          # k de pe prima linie
        self.distMax = int(l[1])    # dist max de pe prima linie

        self.start = []
        self.matGraf = []
        self.marModif = []

        self.sfere = []
        self.scopuri = []
        rest = f.read()
        l = rest.split("sfere\n")
        l2 = l[0].strip().split("\n")   # liniile matricei din fisier
        for linie in l2:
            lMat = []
            lMat2 = []
            lMat3 = []
            for elem in linie.split():
                lMat.append(int(elem))          # gelaram liniile pt info, info2, si mat cu schimbari
                lMat2.append('.')
                lMat3.append(0)
            self.start.append(lMat)             # append la liniile generate
            self.matGraf.append(lMat2)
            self.marModif.append(lMat3)


        # print("prima lin a fis = " + str(self.k) +" " +str(self.distMax))
        # print(str(self.start))
        l = l[1].split("\niesiri\n")
        for rand in l[0].split("\n"):
            lMat = []
            for elem in rand.split():
                lMat.append(int(elem))
            self.sfere.append(lMat)                         # lista de sfere

        # print(str(self.sfere))

        for rand in l[1].strip().split("\n"):
            lMat = []
            for elem in rand.split():
                lMat.append(int(elem))
            self.scopuri.append(lMat)                   #lista de porti


        for iesire in self.scopuri:
            self.matGraf[iesire[0]][iesire[1]] = '#'
        # for rand in self.matGraf:
        #     print(rand)
        # print(self.scopuri)

    def testeazaScop(self, nodCurent):          # verif daca bilele sunt la porti
        locSfere = nodCurent.sfere
        for loc in locSfere:
            if locSfere.count(loc) > 1:
                return False
            if self.scopuri.count(loc) == 0:
                return False
        return True


    def genereazaSuccesori2(self, nodCurent, tip_euristica="euristica banala"):
        listaSuccesori = []
        pozSf = nodCurent.sfere
        lcomb = []
        for poz in pozSf:
            for i in range(poz[0] - self.distMax, poz[0] + self.distMax + 1):
                for j in range(poz[1] - self.distMax, poz[1] + self.distMax + 1):
                    if abs(i - poz[0]) + abs(j - poz[1]) <= self.distMax and [i,j] != poz and i >= 0 and \
                            i<len(self.start) and j<len(self.start) and j >=0:          # poz turnurilor pt dist manhattan
                        lcomb.append([i,j])

        lcomb = list(itertools.combinations(lcomb, math.ceil(len(pozSf) * 2 / 3)))                      # generarea de combinari

        def bilaApoape(turn,lPozsfere):                                     # fun care determina cea mai apropiata bila de un turn
            pozM = 10000
            poz = turn
            for elem in lPozsfere:
                if abs(turn[0] - elem[0]) + abs(turn[1] - elem[1]) < pozM:
                    pozM = abs(turn[0] - elem[0]) + abs(turn[1] - elem[1])
                    poz = elem
            return poz

        def genPoz(coord,maxx):                     # lista cu poz pe care poate merge o bila data sus jos st dr
            l = []
            if coord[0] - 1 >= 0:
                l.append([coord[0] - 1, coord[1]])
            if coord[1] + 1 < maxx:
                l.append([coord[0], coord[1] + 1])
            if coord[0] + 1 < maxx:
                l.append([coord[0] + 1, coord[1]])
            if coord[1] - 1 >= 0:
                l.append([coord[0], coord[1] - 1])

            return l

        # print(bilaApoape([3, 2], self.sfere))

        lPos = []                           # pentru toate bilele toate posibilitatile
        for elem in nodCurent.sfere:
            ghe = genPoz(elem,len(self.start))
            lPos.append(ghe)
        # print(lPos)


        for li in lcomb:                                                # li = toate posibilitatie de liste de modif de turnuri
            copieM = copy.deepcopy(nodCurent.info)
            copieD = copy.deepcopy(nodCurent.matSchimbari)
            ok = 1
            for elem in li:                                             # aici modif matricea si retin schimarile turnurilor elem = turnurile din li
                if elem in nodCurent.sfere:         # pentru a nu afecta marimea unui turn pe care se afla o bila
                    ok = 0
                    # print("ghe")
                    continue
                mainTurn = bilaApoape(elem,nodCurent.sfere)                  # pt a gasi turnul care a generat aceasta schimbare
                # print(mainTurn)
                distM = abs(mainTurn[0] - elem[0]) + abs(mainTurn[1] - elem[1])
                val = copieM[elem[0]][elem[1]] - copieM[mainTurn[0]][mainTurn[1]]
                if(val > 0):                        #daca turnul pe care e bila e mai mic ca turnul pe care vreau sa l modific
                    if(val + distM < self.k):
                        copieM[elem[0]][elem[1]] -= val + distM     #varianta optima de a micii un turn vecin
                        copieD[elem[0]][elem[1]] += val + distM
                        # trebuie retinuta schimbarea in cv dict pt costul unei eventuale muttari
                    else:
                        copieM[elem[0]][elem[1]] -= self.k          #scad maxim daca nu devine mai mic dupa schimbare
                        copieD[elem[0]][elem[1]] += self.k
                else:                               # daca nu e mai mic turnul pe care e bila fac doar -1 minim
                    copieM[elem[0]][elem[1]] -= 1
                    copieD[elem[0]][elem[1]] += 1
            if ok == 0:
                # print("ghe2")
                continue
            # am modif matricea aici trebuie sa aplic mutarile pt matricea schimbata
            # am retinut cu cat a fost modiif un turn in matricea modifD


            pozSfereNoi = []                        # unde vor fi sferele la finalul mutarii
            costMutari = 0                          # cat costa mutarile

            def bestAleg(poz,lPoz):                             # functie care returneaza unde se va muta bila
                maxx = 0
                retin = poz
                for elem in lPoz:
                    # if elem[0] >= 0 and elem[0] < len(self.start) and elem[1] >= 0 and elem[1] < len(self.start):
                    if copieM[elem[0]][elem[1]] < copieM[poz[0]][poz[1]] and copieM[elem[0]][elem[1]] > maxx:
                            maxx = copieM[elem[0]][elem[1]]
                            retin = elem
                return retin

            # for linie in copieM:
            #     print(linie)
            # for linie in copieD:
            #     print(linie)w


            for i in range(len(self.sfere)):                            # generez mutarea sferelor
                # print(self.sfere[i])
                # print(lPos[i])
                if nodCurent.sfere[i] not in self.scopuri:                     # mut o bila doar daca nu e deja pe poarta
                    nouaCoordBi = bestAleg(nodCurent.sfere[i],lPos[i])
                    pozSfereNoi.append(nouaCoordBi)
                    costMutari += copieD[nouaCoordBi[0]][nouaCoordBi[1]] **2
                else:
                    pozSfereNoi.append(nodCurent.sfere[i])          #nu mut bila
                    # print("O bila deja a iesit")

                # print("Noua Poz pt bila " + str(i+1) + " = " + str(nouaCoordBi))

            ok = 1                              # pentru a sari variantele in care bilele sunt pe margine si nu sunt stari fin / 2b ac turn
            for poz in pozSfereNoi:     # unde sunt bilele dupa mutari
                if pozSfereNoi.count(poz) > 1:      # sa nu fie 2 bile pe acelasi turn
                    ok = 0
                    break
                if poz not in self.scopuri:             # daca e pe marginea matricei si nu e stare finala
                    if poz[0] == 0 or poz[0] == len(self.start) or poz[1] == 0 or poz[1] == len(self.start):
                        ok = 0
                        break
            if ok == 0:
                continue

            # acm aici trebuie sa generezi ob de tip parcurgeNod  si sa adaugi in succesori

            # daca cel ptn 1 sfera s-a mutat de pe pot initiala + sa nu se repete poz sferelor in parinti pr a face bucla
            if pozSfereNoi != nodCurent.sfere and not nodCurent.contineInDrum(list(pozSfereNoi)):
                # def __init__(self, id, info, matSchimbari, sfere, parent, cost=0, h=0):
                listaSuccesori.append(parcurgeNod(nodCurent.id + 1, copieM, copieD, list(pozSfereNoi), nodCurent,
                                                  cost=nodCurent.g + costMutari, h=self.calculeaza_h(list(pozSfereNoi), copieM, tip_euristica)))

            # print("NOUL POZ SFERE = " + str(pozSfereNoi))

            # print(li)
        return listaSuccesori




    def calculeaza_h(self, pozitieSfere, matTurnuri, tip_euristica="euristica_banala"):
        if tip_euristica == "euristica_banala":
            for infoBila in pozitieSfere:
                if self.scopuri.count(infoBila):
                    return 1  # se pune costul minim pe o mutare
            return 0
        elif tip_euristica == "admisibila1":
            h = []
            for infoBila in pozitieSfere:
                min = 100000
                for poarta in self.scopuri:
                    dist = abs(poarta[0] - infoBila[0]) + abs(poarta[1] - infoBila[1])
                    if dist < min:
                        min = dist
                h.append(min)
            return max(h)
        elif tip_euristica == "admisibila2":
            h = []
            for infoBila in pozitieSfere:
                min = 100000
                cost = 0
                for poarta in self.scopuri:
                    dist = abs(poarta[0] - infoBila[0]) + abs(poarta[1] - infoBila[1])
                    cost = matTurnuri[poarta[0]][poarta[1]] - matTurnuri[infoBila[0]][infoBila[1]]
                    if cost < 0:
                        cost = 0
                    dist += cost
                    if dist < min:
                        min = dist

                h.append(min)
            return max(h)
        elif tip_euristica == "euristica_neadmisibila":
            h = 0
            for infoBila in pozitieSfere:
                min = 1000
                for poarta in self.scopuri:
                    dist = abs(poarta[0] - infoBila[0]) + abs(poarta[1] - infoBila[1])
                    if dist < min:
                        min = dist
                h += min
            return h * h * h


# gr = Graph("file.txt")
# glob = parcurgeNod.gr
# glob = gr
# parcurgeNod.gr = gr         # default altfel nu marge


def verifFile(numeFile):
    f = open(numeFile,"r")
    primaLinie = f.readline()
    primaLinie = primaLinie.split()     # prima linie si pun elem intr o  lista cu split
    # print(primaLinie)

    if len(primaLinie) != 2:            #daca nu am 2 el pe prima linie
        print("Nu respecta prima linie")
        return False

    sir = f.read()

    if sir.count("sfere") == 0 or sir.count("iesiri") == 0:
        print(sir.count("sfere"))
        print(sir.count("iesiri"))
        print("nu apare separator sfere sau iesiri")
        return False

    sir = sir.split("\nsfere\n")
    # print(sir[0])
    # print(sir[1])

    matrice  = sir[0]
    matrice = matrice.split("\n")    # iau liniile matricei date (randuri pana la "sfere")
    nrL = len(matrice)          # nr de linii ale matricei
    # print(nrL)
    for linie in matrice:
        linie = linie.split()
        # print(linie)
        if len(linie) != nrL:
            print("Insuficiente elem pe linie")         # daca nr coloane de nr linii
            return False
        for elem in linie:
            if not elem.isnumeric():
                print("Nu e numar")         # daca nu am numere in matrice
                return False

    sir1 = sir[1].split("\niesiri\n")
    # print(sir1[0])
    # print(sir1[1])
    sfere  = sir1[0].split("\n")            #poz sfere
    for rand in sfere:              # pt fiecare rand de sfere
        rand = rand.split()
        if len(rand) != 2:                  # daca mai mult de 2 elem pe linie
            print("coord gresite sfere")
            return False

        for elem in rand:
            # print(elem)
            if not elem.isnumeric():                    # daca nu e nr coordonata
                print("Nu e numar")
                return False
            if elem == '0' or elem == str(nrL - 1):                 # daca bila e pe margine nu e bine !!!!!!!!
                print("e pe margine din input o bila")
                return False
            if int(elem) < 0  or int(elem) >= nrL:              # daca coord data e mai mare ca
                print("nu sunt coord reale")
                return False


    iesire = sir1[1].split("\n")                # lista de iesiri
    for rand in iesire:
        rand  = rand.split()
        if len(rand) != 2:
            print("coord gresite iesire")
            return False
        # print(rand)
        margine = 0
        for elem in rand:
            if not elem.isnumeric():
                print("Nu e numar")
                return False
            if int(elem) < 0  or int(elem) >= nrL:              # daca coord data e mai mare ca
                print("nu sunt coord reale")
                return False
            if elem == '0' or elem == str(nrL - 1):
                margine += 1
        if margine == 0:                                   # daca nu se afla pe margine iesirea rFalse
            print("poarta nu e pe marginea matricei")
            return False

    print()
    return True


def check_time(start, limit):       #  functie care verifica sa nu fi depasit o limita de timp
    actual = time.time()
    if actual - start > limit:
        return True
    return False


sol = []
lmaxSuc = []
lmaxCoada = []
lTimpi = []
maxSuc = 0

maxCoada = 0   # nr el coada cand avem recursie


def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate, timeout, t1, euristica):
    # print("A ajuns la: ", nodCurent)
    global maxSuc, maxCoada
    if check_time(t1, timeout):
        print("depasit timp")
        return 0, "depasit timp"
    global sol
    if nodCurent.f > limita:
        return nrSolutiiCautate, nodCurent.f
    if gr.testeazaScop(nodCurent) and nodCurent.f == limita:
        # print("Solutie: ")
        nodCurent.afisDrum()
        # print(limita)
        print("\n----------------\n")
        sol.append(nodCurent)
        global lmaxSuc, lmaxCoada, lTimpi
        lmaxCoada.append(maxCoada)
        lmaxSuc.append(maxSuc)
        t2 = time.time()
        lTimpi.append(t2 - t1)

        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return 0, "gata"
    lSuccesori = gr.genereazaSuccesori2(nodCurent,tip_euristica=euristica)
    maxSuc = max(maxSuc, len(lSuccesori))
    maxCoada += len(lSuccesori)
    minim = float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate, timeout, t1,euristica)
        if rez == "gata":
            return 0, "gata"
        if rez == "depasit timp":
            return 0, "gata"

        # print("Compara ", rez, " cu ", minim)

        if rez < minim:
            minim = rez
            # print("Noul minim: ", minim)
    return nrSolutiiCautate, minim

def ida_star(gr, nrSolutiiCautate, timeout,euristica):
    t1 = time.time()
    nodStart = parcurgeNod(1,gr.start,None,gr.sfere,None,0,0)
    global sol
    sol = []
    global lmaxSuc, lmaxCoada, lTimpi, maxSuc, maxCoada
    lmaxCoada = []
    lmaxSuc = []
    lTimpi = []
    maxSuc = 0
    maxCoada = 0

    limita = nodStart.f
    while True:

        # print("Limita de pornire: ", limita)
        nrSolutiiCautate, rez = construieste_drum(gr, nodStart, limita, nrSolutiiCautate, timeout, t1,euristica)
        if rez == "gata" or rez == "depasit timp":
            break
        if rez == float('inf'):
            # print("Nu mai exista solutii!")
            break
        limita = rez
        # print(">>> Limita noua: ", limita)
    return sol





def dfi(nodCurent, adancime, nrSolutiiCautate, tip_euristica, timeout, t1):
    # print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
    global maxSuc, maxCoada
    if check_time(t1, timeout):
        print("depasit timp")
        a = "depasit timp"
        return a
    if adancime == 1 and gr.testeazaScop(nodCurent):
        global sol
        global lmaxSuc, lmaxCoada, lTimpi
        # print("Solutie: ", end="")
        # nodCurent.afisDrum()
        # print("\n----------------\n")
        # input()
        sol.append(nodCurent)
        lmaxCoada.append(maxCoada)
        lmaxSuc.append(maxSuc)
        t2 = time.time()
        lTimpi.append(t2 - t1)
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
    if adancime > 1:
        lSuccesori = gr.genereazaSuccesori2(nodCurent,tip_euristica)
        maxSuc = max(maxSuc, len(lSuccesori))
        maxCoada += len(lSuccesori)
        for sc in lSuccesori:
            if nrSolutiiCautate != 0:
                nrSolutiiCautate = dfi(sc, adancime - 1, nrSolutiiCautate, tip_euristica, timeout, t1)
    return nrSolutiiCautate


def depth_first_iterativ(gr, nrSolutiiCautate, tip_euristica, timeout):
    t1 = time.time()
    global sol
    sol = []
    global lmaxSuc, lmaxCoada, lTimpi, maxSuc, maxCoada
    lmaxCoada = []
    lmaxSuc = []
    lTimpi = []
    maxSuc = 0
    maxCoada = 0
    for i in range(2000):
        dfi(parcurgeNod(1,gr.start,None,gr.sfere,None,0,0), i, nrSolutiiCautate,tip_euristica,timeout,t1)
        print(i)
        if sol != []:
            break
    return sol



def depth_first(gr, nrSolutiiCautate, tip_euristica, timeout):
    # vom simula o stiva prin relatia de parinte a nodului curent
    t1 = time.time()
    global sol
    sol = []
    global lmaxSuc, lmaxCoada, lTimpi, maxSuc,maxCoada
    lmaxCoada = []
    lmaxSuc = []
    lTimpi = []
    maxSuc = 0
    maxCoada =0
    df(parcurgeNod(1,gr.start,None,gr.sfere,None,0,0), nrSolutiiCautate,tip_euristica, timeout,t1)
    return sol



def df(nodCurent, nrSolutiiCautate,tip_euristica, timeout,t1):
    # if nrSolutiiCautate <= 0:  # testul acesta s-ar valida doar daca in apelul initial avem df(start,if nrSolutiiCautate=0)
    #     return sol
    global maxSuc , maxCoada
    if check_time(t1, timeout):
        print("depasit timp")
        a = "depasit timp"
        return a

    # print("Stiva actuala: " + "->".join(nodCurent.obtineDrum()))
    if gr.testeazaScop(nodCurent):
        global sol
        global lmaxSuc, lmaxCoada, lTimpi
        # print("Solutie: ", end="")
        # nodCurent.afisDrum()
        sol.append(nodCurent)
        lmaxCoada.append(maxCoada)
        lmaxSuc.append(maxSuc)
        t2 = time.time()
        lTimpi.append(t2 - t1)
        # print("\n----------------\n")
        # input()
        nrSolutiiCautate -= 1
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
    lSuccesori = gr.genereazaSuccesori2(nodCurent,tip_euristica)
    maxSuc = max(maxSuc,len(lSuccesori))
    maxCoada += len(lSuccesori)
    for sc in lSuccesori:
        if nrSolutiiCautate != 0:
            nrSolutiiCautate = df(sc, nrSolutiiCautate,tip_euristica, timeout,t1)

    return nrSolutiiCautate


def breadth_first(gr, nrSolutiiCautate, tip_euristica, timeout):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    t1 = time.time()
    c = [parcurgeNod(1,gr.start,None,gr.sfere,None,0,0)]
    sol = []
    global lmaxSuc, lmaxCoada, lTimpi
    lmaxCoada = []
    lmaxSuc = []
    lTimpi = []
    maxSuc = 0

    maxC = 0
    while len(c) > 0:
        if check_time(t1,timeout):
            print("depasit timp")
            a = "depasit timp"
            return a
        maxC = max(len(c), maxC)
        # print("Coada actuala: " + str(c))
        nodCurent = c.pop(0)

        if gr.testeazaScop(nodCurent):
            print("Solutie:")
            nodCurent.afisDrum()
            sol.append(nodCurent)
            lmaxCoada.append(maxC)
            lmaxSuc.append(maxSuc)
            t2 = time.time()
            lTimpi.append(t2 - t1)
            print("\n----------------\n")
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return sol
        lSuccesori = gr.genereazaSuccesori2(nodCurent,tip_euristica)
        maxSuc = max(maxSuc, len(lSuccesori))
        c.extend(lSuccesori)

def a_star(gr2, nrSolutiiCautate, tip_euristica, timeout):
    # in coada vom avea doar noduri de tip NodParcurgere (nodurile din arborele de parcurgere)
    c = [parcurgeNod(1,gr2.start,None,gr2.sfere,None,0,0)]
    sol = []
    t1 = time.time()
    global maxSuc , lmaxSuc , lmaxCoada, lTimpi
    lmaxCoada = []
    lmaxSuc = []
    lTimpi = []
    maxSuc = 0
    maxC = 0
    while len(c) > 0:
        if check_time(t1,timeout):
            print("depasit timp")
            a = "depasit timp"
            return a
        maxC = max(len(c),maxC)
        # print("DIMENSIUNEA COZII = " + str(len(c)))
        # print(str(c))
        nodCurent = c.pop(0)
        if gr2.testeazaScop(nodCurent):
            t2 = time.time()
            print("Solutie: ")
            sol.append(nodCurent)
            lmaxCoada.append(maxC)
            lmaxSuc.append(maxSuc)
            lTimpi.append(t2 - t1)
            nodCurent.afisDrum()
            print("\n----------------\n")
            # input()
            nrSolutiiCautate -= 1
            if nrSolutiiCautate == 0:
                return sol
        lSuccesori = gr2.genereazaSuccesori2(nodCurent, tip_euristica=tip_euristica)
        maxSuc = max(maxSuc,len(lSuccesori))
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa f
                if c[i].f >= s.f:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def a_star_optim(gr, tip_euristica, timeout):
    l_open = [parcurgeNod(1,gr.start,None,gr.sfere,None,0,0)]
    heapq.heapify(l_open)

    global lmaxSuc, lmaxCoada, lTimpi
    lmaxCoada = []
    lmaxSuc = []
    lTimpi = []
    maxSuc = 0
    maxC = 0
    t1 = time.time()
    # l_open contine nodurile candidate pentru expandare (este echivalentul lui c din A* varianta neoptimizata)

    # l_closed contine nodurile expandate
    l_closed = []
    while len(l_open) > 0:
        if check_time(t1,timeout):
            print("depasit timp")
            a = "depasit timp"
            return a
        maxC = max(len(l_open), maxC)
        # print("DIMENSIUNEA COZII = " + str(len(c)))
        # print(str(c))
        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)

        if gr.testeazaScop(nodCurent):
            print("Solutie: ", end="")
            nodCurent.afisDrum()
            lmaxCoada.append(maxC)
            lmaxSuc.append(maxSuc)
            t2 = time.time()
            lTimpi.append(t2 - t1)
            print("\n----------------\n")
            return nodCurent
        lSuccesori = gr.genereazaSuccesori2(nodCurent, tip_euristica=tip_euristica)
        maxSuc = max(maxSuc, len(lSuccesori))
        for s in lSuccesori:
            gasitC = False
            for nodC in l_open:
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        lSuccesori.remove(s)
                    else:  # s.f<nodC.f
                        l_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            lSuccesori.remove(s)
                        else:  # s.f<nodC.f
                            l_closed.remove(nodC)
                        break
        for elem in lSuccesori:
            heapq.heappush(l_open,elem)




# for i in range(len(sys.argv)):
#     print("Argumentul {} are valoarea {} si tipul de date {}".format(i, sys.argv[i], type(sys.argv[i])))
listaFisiereInput = os.listdir(sys.argv[1])
listaFisiereOutput = os.listdir(sys.argv[2])
nrSol = int(sys.argv[3])
timeout = int(sys.argv[4])
# print(listaFisiereInput)
# print(listaFisiereOutput)
# print(nrSol)
# print(timeout)

if not os.path.exists("folder_output"):                         #daca folder ul de output nu exista il creez
    os.mkdir("folder_output")
for numeFisier in listaFisiereInput:                        # adaug in acest folder cate un file pentru fiecare file de input unul de output
    numeFisierOutput = "output_" + numeFisier
    f = open("folder_output\\" + numeFisierOutput, "w")
    f.write("")
    f.close()

ok = True
while ok:
    listaEur = ["euristica_banala", "admisibila1", "admisibila2", "euristica_neadmisibila"]
    optioune = input("optiuni:\n1 : ruleaza a_star  \n2 : releaza a_starOPtim\n3 : ruleaza bfs\n4 : ruleaza dfs\n"
                     "5 : ruleaza dfi\n6 : ruleaza ida_star\n7 : iesi \n")

    if optioune == "1":
        print(listaFisiereInput)
        valInput = input("alegegi fisier de intrare = ")

        if valInput in listaFisiereInput:
            valInput2 = "folder_input\\" + valInput

            if verifFile(valInput2):
                gr = Graph(valInput2)
                parcurgeNod.gr = gr

                print(listaEur)
                euristica = input("alege euristica = ")
                # euristica_banala
                # admisibila1
                # euristica_neadmisibila

                if euristica in listaEur:
                    t0 = time.time()
                    sol = a_star(gr, nrSolutiiCautate=nrSol, tip_euristica=euristica,timeout = timeout)
                    t1 = time.time()
                    print("Alg a durat = " + str(t1 - t0))

                    f = open("folder_output\\output_" +  valInput, "w")
                    if sol == "depasit timp":
                        f.write(sol)
                    else:
                        try:
                            i = 0
                            for elem in sol:

                                f.write(elem.afisDrum()[1])
                                f.write("\nMax de succesori generati =  " +str(lmaxSuc[i]) +"\n")
                                f.write("Nr de el dinlista =  " + str(lmaxCoada[i]) + "\n")
                                f.write("Timp gasire =  " + str(lTimpi[i]) + "\n")
                                f.write("\n----------------\n\n")
                                i+=1
                        except:
                            print("nu ex sol")
                            f.write("nu ex sol")
                else:
                    print("Euristica gresita")
            else:
                print("nu ex sol")
                f = open("folder_output\\output_" +  valInput, "w")
                f.write("nu ex sol")
        else:
            print("file invalid")

    elif optioune =="2":
        print(listaFisiereInput)
        valInput = input("alegegi fisier de intrare = ")

        if valInput in listaFisiereInput:
            valInput2 = "folder_input\\" + valInput

            if verifFile(valInput2):
                gr = Graph(valInput2)
                parcurgeNod.gr = gr

                print(listaEur)
                euristica = input("alege euristica = ")
                # euristica_banala
                # admisibila1
                # euristica_neadmisibila

                if euristica in listaEur:
                    t0 = time.time()
                    sol = a_star_optim(gr, tip_euristica=euristica, timeout=timeout)
                    t1 = time.time()
                    print("Alg a durat = " + str(t1 - t0))

                    f = open("folder_output\\output_" + valInput, "w")
                    if sol == "depasit timp":
                        f.write(sol)
                    else:
                        try:
                            f.write(sol.afisDrum()[1])
                            f.write("\nMax de succesori generati =  " + str(lmaxSuc[0]) + "\n")
                            f.write("Nr de el dinlista =  " + str(lmaxCoada[0]) + "\n")
                            f.write("Timp gasire =  " + str(lTimpi[0]) + "\n")
                        except:
                            print("Nu ex sol")
                            f.write("Nu ex sol")
                else:
                    print("Euristica gresita")
            else:
                print("nu ex sol")
                f = open("folder_output\\output_" +  valInput, "w")
                f.write("nu ex sol")
        else:
            print("file invalid")

    if optioune == "3":
        print(listaFisiereInput)
        valInput = input("alegegi fisier de intrare = ")

        if valInput in listaFisiereInput:
            valInput2 = "folder_input\\" + valInput

            if verifFile(valInput2):
                gr = Graph(valInput2)
                parcurgeNod.gr = gr

                # print(listaEur)
                # euristica = input("alege euristica = ")
                # euristica_banala
                # admisibila1
                # euristica_neadmisibila


                t0 = time.time()
                sol = breadth_first(gr, nrSolutiiCautate=nrSol, tip_euristica="euristica_banala",timeout = timeout)
                t1 = time.time()
                print("Alg a durat = " + str(t1 - t0))

                f = open("folder_output\\output_" + valInput, "w")
                if sol == "depasit timp":
                    f.write(sol)
                else:
                    try:
                        i = 0
                        for elem in sol:
                            f.write(elem.afisDrum()[1])
                            f.write("\nMax de succesori generati =  " + str(lmaxSuc[i]) + "\n")
                            f.write("Nr de el dinlista =  " + str(lmaxCoada[i]) + "\n")
                            f.write("Timp gasire =  " + str(lTimpi[i]) + "\n")
                            f.write("\n----------------\n\n")
                            i+=1
                    except:
                        print("Nu ex sol")
                        f.write("Ne ex sol")
            else:
                print("nu ex sol")
                f = open("folder_output\\output_" +  valInput, "w")
                f.write("nu ex sol")
        else:
            print("file invalid")
    if optioune == "4":
        print(listaFisiereInput)
        valInput = input("alegegi fisier de intrare = ")

        if valInput in listaFisiereInput:
            valInput2 = "folder_input\\" + valInput

            if verifFile(valInput2):
                gr = Graph(valInput2)
                parcurgeNod.gr = gr

                # print(listaEur)
                # euristica = input("alege euristica = ")
                # euristica_banala
                # admisibila1
                # euristica_neadmisibila


                t0 = time.time()
                sol = depth_first(gr, nrSolutiiCautate=nrSol, tip_euristica="euristica_banala",timeout = timeout)
                t1 = time.time()
                print("Alg a durat = " + str(t1 - t0))

                f = open("folder_output\\output_" + valInput, "w")
                if sol == []:
                    f.write("Limata timp depasita")
                else:
                    try:
                        i = 0
                        for elem in sol:
                            f.write(elem.afisDrum()[1])
                            f.write("\nMax de succesori generati =  " + str(lmaxSuc[i]) + "\n")
                            f.write("Nr de el dinlista =  " + str(lmaxCoada[i]) + "\n")
                            f.write("Timp gasire =  " + str(lTimpi[i]) + "\n")
                            f.write("\n----------------\n\n")
                            i += 1
                    except:
                        print("Nu ex sol")
                        f.write("Ne ex sol")
            else:
                print("nu ex sol")
                f = open("folder_output\\output_" +  valInput, "w")
                f.write("nu ex sol")
        else:
            print("file invalid")
    if optioune == "5":
        print(listaFisiereInput)
        valInput = input("alegegi fisier de intrare = ")

        if valInput in listaFisiereInput:
            valInput2 = "folder_input\\" + valInput

            if verifFile(valInput2):
                gr = Graph(valInput2)
                parcurgeNod.gr = gr

                # print(listaEur)
                # euristica = input("alege euristica = ")
                # euristica_banala
                # admisibila1
                # euristica_neadmisibila


                t0 = time.time()
                sol = depth_first_iterativ(gr, nrSolutiiCautate=nrSol, tip_euristica="euristica_banala",timeout = timeout)
                t1 = time.time()
                print("Alg a durat = " + str(t1 - t0))

                f = open("folder_output\\output_" + valInput, "w")
                if sol == []:
                    f.write("Limata timp depasita")
                else:
                    try:
                        i = 0
                        for elem in sol:
                            f.write(elem.afisDrum()[1])
                            f.write("\nMax de succesori generati =  " + str(lmaxSuc[i]) + "\n")
                            f.write("Nr de el dinlista =  " + str(lmaxCoada[i]) + "\n")
                            f.write("Timp gasire =  " + str(lTimpi[i]) + "\n")
                            f.write("\n----------------\n\n")
                            i += 1
                    except:
                        print("Nu ex sol")
                        f.write("Ne ex sol")
            else:
                print("nu ex sol")
                f = open("folder_output\\output_" +  valInput, "w")
                f.write("nu ex sol")
        else:
            print("file invalid")
    if optioune == "6":
        print(listaFisiereInput)
        valInput = input("alegegi fisier de intrare = ")

        if valInput in listaFisiereInput:
            valInput2 = "folder_input\\" + valInput

            if verifFile(valInput2):
                gr = Graph(valInput2)
                parcurgeNod.gr = gr

                print(listaEur)
                euristica = input("alege euristica = ")
                # print(listaEur)
                # euristica = input("alege euristica = ")
                # euristica_banala
                # admisibila1
                # euristica_neadmisibila
                if euristica in listaEur:
                    t0 = time.time()
                    sol = ida_star(gr, nrSolutiiCautate = nrSol, timeout = timeout,euristica = euristica)
                    t1 = time.time()
                    print("Alg a durat = " + str(t1 - t0))

                    f = open("folder_output\\output_" + valInput, "w")
                    if sol == []:
                        f.write("Limata timp depasita")
                    else:
                        try:
                            i = 0
                            for elem in sol:
                                f.write(elem.afisDrum()[1])
                                f.write("\nMax de succesori generati =  " + str(lmaxSuc[i]) + "\n")
                                f.write("Nr de el dinlista =  " + str(lmaxCoada[i]) + "\n")
                                f.write("Timp gasire =  " + str(lTimpi[i]) + "\n")
                                f.write("\n----------------\n\n")
                                i += 1
                        except:
                            print("Problema fisier")
                            f.write("Problema fisier")
                else:
                    print("ne ex eur")
            else:
                print("nu ex sol")
                f = open("folder_output\\output_" +  valInput, "w")
                f.write("nu ex sol")
        else:
            print("file invalid")
    elif optioune == "7":
        print("ati terminat")
        ok = False


# python main.py folder_input folder_output 2 10







