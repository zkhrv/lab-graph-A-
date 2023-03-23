from heapq import heappush, heappop

class Graph1:
    def __init__(self, graph_dict):
        self.adj = graph_dict # Инициализация графа с помощью словаря

    def bfs(self, start): # алгоритм поиска в ширину 
        visited = {start: 0} # Создание словаря для хранения расстояний до каждой вершины
        queue = [start] # Создание очереди и добавление в нее начальной вершины
        path = {} # Создание словаря для хранения путей до каждой вершины

        while queue: # Цикл, пока очередь не пуста
            node = queue.pop(0) # Извлечение вершины из очереди
            for neighbor, weight in self.adj[node]: # Цикл по каждому соседу текущей вершины
                if neighbor not in visited: # Если соседняя вершина не посещена
                    visited[neighbor] = visited[node] + weight # Добавление расстояния до нее в словарь расстояний
                    queue.append(neighbor) # Добавление соседней вершины в очередь
                    path[neighbor] = (node, weight) # Добавление пути до соседней вершины в словарь путей

        result = [f"{start}-{node}={visited[node]}" for node in visited] # форматирование списка результатов 
        return result # возврат результата 

    def dfs(self, start): # алгоритм поиска в глубину
        visited = set() # множество посещенных вершин 
        path = [] # список вершин, образующих путь 

        def dfs_helper(node): # вложенная функция, для рекурсивного обхода графа и обновления visited и path
            visited.add(node) # добавление текущей вершины в множество visited 
            path.append(node) # добавление текущей вершины в список path
            for neighbor, _ in self.adj[node]: # обход всех соседей текущей вершины 
                if neighbor not in visited: # если соседняя вершина не посещена, вызвать dfs_helper для нее
                    dfs_helper(neighbor) 

        dfs_helper(start) # вызов вложенной функции с заданной начальной вершиной start
        result = [f"[{start}, {' '.join(path)}]"] # формирование результата в виде списка строк 
        return result # возврат результата

    def dijkstra(self, start): # алгоритм Дейкстры
        heap = [(0, start)] #инициализирует кучи с начальным весом 0 и старотовой вершиной 
        visited = set() # множество посещенных вершин 
        path = {start: None} # словар, где ключи - вершины, значения - их родители в пути  
        dist = {start: 0} # словарь, где ключи - вершины, значения - ткущее расстояние от старта

        while heap: # пока куча не пуста
            (weight, node) = heappop(heap) # получаем вершину с наименьшим расстоянием 
            if node in visited: # если вершина уже посещена, то переходим к следующей
                continue 
            visited.add(node) # добавляем вершину в множество посещенных

            for neighbor, neighbor_weight in self.adj[node]: # перебираем соседей вершины
                distance = dist[node] + neighbor_weight # вычисляем расстояние до соседа 
                if neighbor not in dist or distance < dist[neighbor]: # если расстояние меньше, чем уже известное 
                    dist[neighbor] = distance # обновляем расстояние
                    heappush(heap, (distance, neighbor)) # добавляем вершину в очередь с приоритетом
                    path[neighbor] = node # устанавливаем предка для соседа 

        result = [] # итоговый список вершин 
        end_node = "F" # конечная вершина пути 
        while end_node != start: # пока не дойдем до начальной вершины 
            result.insert(0, end_node) # добавляем вершину в начало списка
            end_node = path[end_node] # переходим к предку 
        result.insert(0, start) # добавляем начальную вершину 
        result_str = "-".join(result) # преобразуем список в строку, разделяя вершины дефисами 
        return result_str # возврат итогового пути 

    def kruskal(self): # алгоритм Крускала 
        edges = [] # создание списка ребер графа 
        for node in self.adj: # цикл по узлам графа
            for neighbor, weight in self.adj[node]: # цикл по соседним узлам и их весам 
                edges.append((weight, node, neighbor)) # добавление кортежа в список ребер 
        edges.sort() # сортировка списка ребер по возрастанию веса

        mst = {} # словрь, хранящий оставное дерево 
        parents = {} # словарь, хранящий родителей для каждого узла

        def find(node): # функция нахождения корня дерева, к которому принадлежит узел 
            if parents[node] != node: # если родительский узел не является корнем дерева
                parents[node] = find(parents[node]) # то находим для родительского узла 
            return parents[node] # возвращаем корень дерева

        def union(node1, node2): # функция объединения двух деревьев, к которым принадлежат узлы node1 и node2
            root1 = find(node1) # находим корень дерева, к которому принадлежит узел node1
            root2 = find(node2) # находим корень дерева, к которому принадлежит узел node2
            if root1 != root2: # если корни деревьев не равны
                if root1 < root2: # если корень первого дерева меньше корня второго дерева
                    parents[root2] = root1 # то устанавливаем родителя корня второго дерева равным корню первого дерева
                else: # иначе
                    parents[root1] = root2 # устанавливаем родителя корня первого дерева равным корню второго дерева


        for node in self.adj: # цикл по узлам графа
            parents[node] = node # инициализация родительского узла для каждого узла как сам узел

        for edge in edges: # цикл по списку ребер графа (в порядке возрастания веса)
            weight, node1, node2 = edge # получаем вес ребра и его два узла
            if find(node1) != find(node2): # если узлы принадлежат разным деревьям
                union(node1, node2) # объединяем деревья
                if node1 not in mst: # проверяем, есть ли node1 в словаре mst, если нет, то
                    mst[node1] = [] # добавляем пустой список для node1
                mst[node1].append((node2, weight)) # добавляем кортеж (node2, weight) в список, который соответствует node1
                if node2 not in mst: # проверяем, есть ли node2 в словаре mst, если нет, то
                    mst[node2] = [] # добавляем пустой список для node2
                mst[node2].append((node1, weight)) #  добавляем кортеж (node1, weight) в список, который соответствует node2

        result = [] # создаем список, который будет содержать результат работы алгоритма
        for node in mst: # проходимся по всем узлам MST
            result.append((node, [f"{neighbor}:{weight}" for neighbor, weight in mst[node]])) # добавляем кортеж (node, list), где list - это список кортежей (neighbor, weight) соответствующих узлу node в словаре mst

        return result #  возвращаем результат в виде списка кортежей (узел, список кортежей (сосед, вес)) 



       
