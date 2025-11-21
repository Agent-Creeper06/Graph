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

    #Значения по умолчанию
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


def main(): #Запуск функции
    #Получение параметров
    opts = parse_args()
    #Вывод параметров
    print("Параметры (ключ=значение):")
    for k, v in opts.items():
        print(f"{k}={v}")

if __name__ == "__main__":
    main()
