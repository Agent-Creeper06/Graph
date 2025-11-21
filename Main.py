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

def print_mermaid(edges): #Гравический вывод графиков
    for a, b in edges:
        print(f"{a} --> {b}")


def main():
    #Получение параметров
    opts = parse_args()

    #Чтение параметров
    graph = read_test_repo(opts["repo"])
    max_depth = int(opts["max-depth"])
    substr = opts["filter"]
    pkg = opts["package"]

    #Вывод графа на экран
    edges = bfs_graph(graph, pkg, max_depth, substr)
    print_mermaid(edges)

    #Дополнительно сохраняем в файл
    with open("graph.mmd", "w", encoding="utf-8") as f:
        f.write("graph LR\n")
        for a, b in edges:
            f.write(f"{a} --> {b}\n")

    print("Mermaid-граф записан в graph.mmd", file=sys.stderr)

if __name__ == "__main__":
    main()
