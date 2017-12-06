from collections import defaultdict
import sys
import math

class Heap():
    def __init__(self):
        self.array = []
        self.size = 0
        self.pos = []

    def newMinHeapNode(self, v, dist):
        minHeapNode = [v, dist]
        return minHeapNode

    def swapMinHeapNode(self, a, b):
        t = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = t

    def minHeapify(self, idx):
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2

        if left < self.size and self.array[left][1] < \
                self.array[smallest][1]:
            smallest = left

        if right < self.size and self.array[right][1] < \
                self.array[smallest][1]:
            smallest = right

        # Losnodos que se van a cambiar 
        # si idx no es el mas pequeño
        if smallest != idx:
            # Swap
            self.pos[self.array[smallest][0]] = idx
            self.pos[self.array[idx][0]] = smallest

            # Swap
            self.swapMinHeapNode(smallest, idx)

            self.minHeapify(smallest)

    def extractMin(self):

        if self.isEmpty() == True:
            return

        root = self.array[0]

        lastNode = self.array[self.size - 1]
        self.array[0] = lastNode

        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1

        self.size -= 1
        self.minHeapify(0)

        return root

    def isEmpty(self):
        return True if self.size == 0 else False

    def decreaseKey(self, v, dist):

        # Tomar el indice de V en el heap

        i = self.pos[v]

        # Tomar el nodo y actualizar su valor
        self.array[i][1] = dist

        # Ir subiendo hasta que el heap este correcto (heapify)
        while i > 0 and self.array[i][1] < \
                self.array[math.floor((i - 1) / 2)][1]:
            # Swap con su padre
            self.pos[self.array[i][0]] = math.floor((i - 1) / 2)
            self.pos[self.array[math.floor((i - 1) / 2)][0]] = i
            self.swapMinHeapNode(i, math.floor((i - 1) / 2))

            # mover al indice del padre
            i = math.floor((i - 1) / 2);

    # Ver si el vertice v esta en el heap o no
    def isInMinHeap(self, v):

        if self.pos[v] < self.size:
            return True
        return False


def printArr(parent, n):
    for i in range(1, n):
        print("%d - %d" % (parent[i], i))


class Graph():
    def __init__(self, V):
        self.V = V
        self.graph = defaultdict(list)

    # Añade arista a un nodo que no tiene direccion
    def addEdge(self, src, dest, weight):

        # Añade arista de src a dest.  Un nuevo nodo es
        # añadido a la lista de adjacencia de src. El nodo
        # es añadido al ´principio. El primer elemento del nodo
        # es su destino y el segudo es su peso
        newNode = [dest, weight]
        self.graph[src].insert(0, newNode)

        # Como el grfo no es dirigido, añadir tambien arista
        # de dest a src
        newNode = [src, weight]
        self.graph[dest].insert(0, newNode)

    def PrimMST(self):
        # Numero de vertices en el grafo
        V = self.V

        # valor de key usadas para escoger el minimo peso de la arista 
        key = []

        # Aqui se guarda el spanning tree
        parent = []

        # minHeap creado representa E
        minHeap = Heap()

        #  Initializar  el minheap con todos los vertices. Valor de Key de 
        # los vertices (excepto el 0) que es infinito
        for v in range(V):
            parent.append(-1)
            key.append(sys.maxsize)
            minHeap.array.append(minHeap.newMinHeapNode(v, key[v]))
            minHeap.pos.append(v)

        # Hacer que el valor de la key del vertice 0 valga 0 para
        # que se extraiga primero
        minHeap.pos[0] = 0
        key[0] = 0
        minHeap.decreaseKey(0, key[0])

        # Al principio el tamaño del heap es igual a V
        minHeap.size = V;

        # In el loop, min heap contiene todos los nodos
        # que aun no se añaden al spanning tree.
        while minHeap.isEmpty() == False:

            # Extraer el vertice que tenga el valor mas pequeño de peso
            newHeapNode = minHeap.extractMin()
            u = newHeapNode[0]

            # Ver todos los vertices adjacentes de u   
            # (vertices extraidos) y actualizar el
            # valor de sus distancias
            for pCrawl in self.graph[u]:

                v = pCrawl[0]

                # Si la distancia mas corta a v no se ha finalizado aun
                # y la distancia a v por u es menor que 
                # la calculada previamente
                if minHeap.isInMinHeap(v) and pCrawl[1] < key[v]:
                    key[v] = pCrawl[1]
                    parent[v] = u

                    # actualizar el valor de la distancia en el heap tambien
                    minHeap.decreaseKey(v, key[v])

        printArr(parent, V)


# Testamos
graph = Graph(9)
graph.addEdge(0, 1, 1)
graph.addEdge(0, 7, 8)
graph.addEdge(1, 2, 8)
graph.addEdge(1, 7, 11)
graph.addEdge(2, 3, 7)
graph.addEdge(2, 8, 2)
graph.addEdge(2, 5, 4)
graph.addEdge(3, 4, 9)
graph.addEdge(3, 5, 14)
graph.addEdge(4, 5, 10)
graph.addEdge(5, 6, 2)
graph.addEdge(6, 7, 1)
graph.addEdge(6, 8, 6)
graph.addEdge(7, 8, 7)
graph.PrimMST()