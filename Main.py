import sys

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


def main():
    #Получение параметров
    opts = parse_args()

    #Вывод параметров
    graph = read_test_repo(opts["repo"])
    pkg = opts["package"]

    #Вывод зависимостей
    print(f"Прямые зависимости пакета {pkg}:")
    deps = graph.get(pkg, []) #Получение зависимостей
    if not deps:
        print("(нет прямых зависимостей)")
    else:
        for d in deps:
            print(d)

if __name__ == "__main__":
    main()
