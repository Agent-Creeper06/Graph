# stage4.py
import sys
from collections import deque

def parse_args(): #Считываение аргументов с командной строки
    args = sys.argv[1:]
    opts = {}
    i = 0
    while i < len(args):
        a = args[i]

        if a == "--test":
            opts["test"] = "true"
            i += 1
            continue

        if a.startswith("--") and i + 1 < len(args):
            opts[a[2:]] = args[i + 1]
            i += 2
            continue

        i += 1

    # Значения по умолчанию
    if "package" not in opts:
        print("Ошибка: не задан --package")
        sys.exit(2)
    if "repo" not in opts:
        print("Ошибка: не задан --repo")
        sys.exit(2)
    if "max-depth" not in opts:
        opts["max-depth"] = "5"
    if "filter" not in opts:
        opts["filter"] = ""

    return opts

def read_test_repo(path): #Чтение файла
    graph = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" not in line:
                continue
            pkg, deps = line.split(":", 1)
            pkg = pkg.strip()
            deps = deps.strip().split()
            graph[pkg] = deps
    return graph

def bfs_graph(graph, start, max_depth, substr): #Постройка графа зависимостей
    visited = set() #Массив для записи посещённых
    edges = []

    q = deque() #Очередь для прохождения дерева в ширину
    q.append((start, 0)) #Добавляем нулевой элемент
    visited.add(start) #Добавляем этот элемент в посещённые

    while q:
        cur, depth = q.popleft()
        if depth >= max_depth: #Проверка, что текущая глубина не превысила заданную
            continue

        for d in graph.get(cur, []):
            if substr and substr in d: #Если пакет содержит подстроку, то он пропускается
                continue

            edges.append((cur, d))

            if d not in visited: #Добавление посещённого пакета в список во избежании бесконечных циклов
                visited.add(d)
                q.append((d, depth + 1))

    return edges

def reverse_graph(graph): #Граф обратных зависимостей
    rev = {k: [] for k in graph} #Составление обратного графа
    for a, deps in graph.items():
        for b in deps:
            rev.setdefault(b, []).append(a)
    return rev


def reverse_deps(graph, target, max_depth, substr): #Постройка графа зависимостей
    rev = reverse_graph(graph)
    visited = set() #Массив для записи посещённых

    q = deque() #Очередь для прохождения дерева в ширину
    q.append((target, 0)) #Добавляем нулевой элемент
    visited.add(target) #Добавляем этот элемент в посещённые

    depends = []

    while q:
        cur, depth = q.popleft()
        if depth >= max_depth: #Проверка, что текущая глубина не превысила заданную
            continue

        for p in rev.get(cur, []):
            if substr and substr in p: #Если пакет содержит подстроку, то он пропускается
                continue

            if p not in visited: #Добавление посещённого пакета в список во избежании бесконечных циклов
                visited.add(p)
                depends.append(p)
                q.append((p, depth + 1))

    return depends


def main():
    #Получение параметров
    opts = parse_args()

    #Чтение параметров
    graph = read_test_repo(opts["repo"])
    max_depth = int(opts["max-depth"])
    substr = opts["filter"]
    pkg = opts["package"]

    #Получение графа
    deps = reverse_deps(graph, pkg, max_depth, substr)

    #Вывод графа
    print(f"Обратные зависимости (кто зависит от {pkg}):")
    if deps:
        for d in deps:
            print(d)
    else:
        print("(нет)")

if __name__ == "__main__":
    main()
