from prettytable import PrettyTable # импортируем класс PrettyTable из библиотеки prettytable

class Graph2:

    def __init__(self, graph_dict=None): # метод инициализации класса
        if graph_dict is None: # если граф не передан, то создаем пустой словарь
            graph_dict = {}
        self.graph_dict = graph_dict # сохраняем словарь графа в атрибут класса

    def vertices(self): # метод для получения списка вершин графа
        return list(self.graph_dict.keys())

    def edges(self): # метод для получения списка ребер графа
        edges = []
        for vertex in self.graph_dict: # перебираем вершины графа
            for neighbour in self.graph_dict[vertex]: # перебираем соседей каждой вершины
                if {neighbour, vertex} not in edges: # если ребро еще не было добавлено в список ребер, то добавляем его
                    edges.append({vertex, neighbour})
        return edges # возвращаем список ребер

    def add_vertex(self, vertex): # метод для добавления новой вершины в граф
        if vertex not in self.graph_dict: # если вершина еще не была добавлена в граф, то добавляем ее
            self.graph_dict[vertex] = []

    def add_edge(self, edge): # метод для добавления нового ребра в граф
        edge = set(edge) # преобразуем ребро в множество
        (vertex1, vertex2) = tuple(edge) # извлекаем вершины из множества ребра
        if vertex1 in self.graph_dict: # если первая вершина уже есть в графе, то добавляем вторую вершину как соседа первой вершины
            self.graph_dict[vertex1].append((vertex2, 0))
        else: # иначе создаем новую вершину и добавляем вторую вершину как соседа первой вершины
            self.graph_dict[vertex1] = [(vertex2, 0)]

    def prim(self): # Алгоритм Прима
        visited = set()  # создание множества для посещенных вершин
        unvisited = set(self.graph_dict.keys())  # создание множества для непосещенных вершин
        start_vertex = list(unvisited)[0]  # выбор первой вершины в множестве непосещенных вершин
        visited.add(start_vertex)  # добавление первой вершины в множество посещенных вершин
        unvisited.remove(start_vertex)  # удаление первой вершины из множества непосещенных вершин
        result = {}  # создание словаря для хранения ребер и их весов
        while unvisited:  # цикл продолжается пока все вершины не будут посещены
            edges = []  # создание списка ребер
            for visited_vertex in visited:  # цикл по всем посещенным вершинам
                for neighbour, weight in self.graph_dict[visited_vertex]:  # цикл по всем соседям текущей вершины
                    if neighbour in unvisited:  # если сосед еще не посещен
                        edges.append((visited_vertex, neighbour, weight))  # добавление ребра в список ребер
            min_edge = min(edges, key=lambda x: x[2])  # поиск ребра с минимальным весом
            result[min_edge[0]] = "{}: {}".format(min_edge[1], min_edge[2])  # добавление ребра в словарь результата
            visited.add(min_edge[1])  # добавление вершины в множество посещенных вершин
            unvisited.remove(min_edge[1])  # удаление вершины из множества непосещенных вершин
        return result # возвращаем результат работы алгоритма


    def floyd_warshall(self): # Алгоритм Флойда-Уоршелла
        distance = {} # Создание пустого словаря для хранения расстояний между вершинами графа
        vertices = sorted(self.vertices()) # Получение списка вершин графа и их сортировка
        for vertex in vertices: # Цикл по каждой вершине графа
            distance[vertex] = {} # Добавление нового пустого словаря для текущей вершины
            for neighbour in vertices: # Цикл по каждому соседу текущей вершины
                if neighbour == vertex: # Если текущая вершина совпадает с ее соседом, то расстояние до него равно 0
                    distance[vertex][neighbour] = 0
                else: # Иначе расстояние равно бесконечности
                    distance[vertex][neighbour] = float('inf')
            for neighbour, weight in self.graph_dict[vertex]: # Цикл по каждому соседу текущей вершины и его весу
                distance[vertex][neighbour] = weight # Установка расстояния от текущей вершины до соседа, равного его весу
        for k in vertices: # Цикл по каждой вершине графа
            for i in vertices: # Цикл по каждой вершине графа
                for j in vertices: # Цикл по каждой вершине графа
                    if distance[i][j] > distance[i][k] + distance[k][j]: # Если текущее расстояние между вершинами больше, чем сумма расстояний до вершины k
                        distance[i][j] = distance[i][k] + distance[k][j] # от вершины i и до вершины k от вершины j, то установка нового расстояния
        return distance # Возврат словаря расстояний между вершинами графа

    def print_floyd_warshall(self): # красивый вывод результата работы алгоритма Флойда-Уоршелла в виде матрици достижимости 
        distance = self.floyd_warshall() # Вызов метода floyd_warshall для получения словаря расстояний между вершинами графа
        vertices = sorted(self.vertices()) # Получение списка вершин графа и их сортировка
        table = PrettyTable([''] + vertices) # Создание таблицы с помощью библиотеки PrettyTable
        for vertex in vertices: # Цикл по каждой вершине графа
            row = [vertex] # Создание новой строки для текущей вершины
            for neighbour in vertices: # Цикл по каждому соседу текущей вершины
                if distance[vertex][neighbour] == float('inf'): # Если расстояние от текущей вершины до соседа равно бесконечности, то в таблице проставляется "-"
                    row.append('-')
                else: # Иначе - расстояние записывается в ячейку таблицы
                    row.append(distance[vertex][neighbour])
            table.add_row(row) # Добавление созданной строки в таблицу
        return table # Возврат готовой таблицы
    