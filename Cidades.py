import json
import math
from math import radians, cos, sin, asin, sqrt


class Grafo:
    def __init__(self, vertice):
        self.v = vertice
        self.adjacentMatriz = [[0 for i in range(self.v)] for j in range(self.v)]

    def AddEdges(self, src, dest, custo):
        if src == dest:
            #print("Mesma origem e destino")
            a=0
        else:
            self.adjacentMatriz[src][dest] = custo
            self.adjacentMatriz[dest][src] = custo

    def GetNeighbours(self, src):
        lst = []
        for i in range(len(self.adjacentMatriz[src])):
            if self.adjacentMatriz[src][i] > 0:
                lst.append(i)
        return lst
    
    def DijkstraShortestPath(self,src,dest):
        dct = {}
        for i in range(len(self.adjacentMatriz)):
            temp = {}
            x = self.GetNeighbours(i)
            for j in x:
                temp[j] = self.adjacentMatriz[i][j]
            dct[i] = temp
        
        inicio = src
        fim = dest
        menor_dist = {}
        pred = {}
        nos_nao_vistos = dct
        infinito = 9999999
        path = []


        for node in nos_nao_vistos:
            menor_dist[node] = infinito
        menor_dist[inicio] = 0

        while nos_nao_vistos:
            minNode = None
            for node in nos_nao_vistos:
                if minNode is None:
                    minNode = node
                elif menor_dist[node] < menor_dist[minNode]:
                    minNode = node

            for filho, peso in dct[minNode].items():
                if peso + menor_dist[minNode] < menor_dist[filho]:
                    menor_dist[filho] = peso + menor_dist[minNode]
                    pred[filho] = minNode
            nos_nao_vistos.pop(minNode)

        no_atual = fim
        while no_atual != inicio:
            try:
                path.insert(0,no_atual)
                no_atual = pred[no_atual]
            except KeyError:
                print('Caminho nao alcançável')
                break
        path.insert(0,inicio)
        if menor_dist[fim] != infinito:
            print('Menor distancia é', str(menor_dist[fim]))
            #print('E o caminho é', str(path))
            return path

#le o json
with open('cities.json') as json_cities:
    cidades = json.load(json_cities)

list_latitude = []
list_longitude = []
list_nomes = []

for i in cidades: 
    list_latitude.append(i['latitude'])
    list_longitude.append(i['longitude'])
    list_nomes.append(i['city'])

#calcuula a distancia em km de 2 pontos na Terra
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = (sin(dlat/2)**2 + cos(lat1)) * (cos(lat2) * sin(dlon/2)**2)
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

g = Grafo(1000)

print('Digite a distância MÁXIMA entre 2 cidades para se criar uma aresta:')
in_dist = int(input())

#calcula a distancia entre as cidades e cria os grafos
for i in range(1000):
    for j in range(1000):
        dist = haversine(list_longitude[i], list_latitude[i], list_longitude[j], list_latitude[j])
        #distancia radial
        if(dist<in_dist):
            g.AddEdges(i, j, dist)

#pede a cidade de partida do usuario
print('Insira o nome da cidade de partida:')
partida = input()
while True:
    if partida in list_nomes:
        index1 = list_nomes.index(partida)
        break
    else:
        print('Cidade invalida, insira novamente:')
        partida = input()


#pede a cidade de destino do usuario 
print('Insira o nome da cidade de destino:')
destino = input()
while True:
    if destino in list_nomes:
        index2 = list_nomes.index(destino)
        break
    else:
        print('Cidade invalida, insira novamente:')
        destino = input()


caminho = g.DijkstraShortestPath(index1, index2)


#necessario para imprimir o caminho
list_teste = []
for i in range(len(caminho)):
    aux = caminho[i]
    nome = list_nomes[aux]
    list_teste.append(nome)


#printa o caminho
print('E o menor caminho é:', list_teste)
