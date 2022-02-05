import ast
import sys
import time


def get_a(log_a):
    """Get generator from log_a file."""
    while True:
        a = log_a.readline().strip()
        if not a:
            break
        yield ast.literal_eval(a)


def get_b(log_b):
    """Get generator from log_b file."""
    while True:
        b = log_b.readline().strip()
        if not b:
            break
        yield ast.literal_eval(b)


def iterate(income):
    """Try to get next item from generators, return False in case of exception"""
    try:
        outcome = next(income)
    except StopIteration:
        outcome = False
    return outcome


if __name__ == '__main__':
    # открытие сразу трех файлов, чтобы не держать в памяти данные, будем их считывать и сразу писать в log_c файл
    start = time.time()
    with open(sys.argv[1]) as log_a:
        with open(sys.argv[2]) as log_b:
            with open(sys.argv[4], 'w') as log_c:
                # создание генераторов и получение первых значений из них
                a, b = get_a(log_a), get_b(log_b)
                aa, bb = iterate(a), iterate(b)
                while True:
                    # если строки в log_a закончились, то пишем остаток файла log_b в файл log_c
                    if not aa:
                        while bb:
                            bbb = str(bb).replace("'", '"')
                            log_c.write(f'{bbb}\n')
                            bb = iterate(b)
                        break
                    if not bb:
                        # если строки в log_a закончились, то пишем остаток файла log_b в файл log_c
                        while aa:
                            aaa = str(aa).replace("'", '"')
                            log_c.write(f'{aaa}\n')
                            aa = iterate(a)
                        break
                    # сравнение таймштампов и в соответствии с этим запись значения в log_c
                    if aa['timestamp'] == bb['timestamp']:
                        bbb = str(bb).replace("'", '"')
                        log_c.write(f'{bbb}\n')
                        aaa = str(aa).replace("'", '"')
                        log_c.write(f'{aaa}\n')
                        bb = iterate(b)
                        aa = iterate(a)
                    elif aa['timestamp'] > bb['timestamp']:
                        bbb = str(bb).replace("'", '"')
                        log_c.write(f'{bbb}\n')
                        bb = iterate(b)
                    else:
                        aaa = str(aa).replace("'", '"')
                        log_c.write(f'{aaa}\n')
                        aa = iterate(a)
    print(f"Finished in {time.time() - start:0f} sec")

# P.S. в случае необходимости можно еще добавить сортировку в случае одинакового таймштампа
# по другому полю, например по log_level и это бы практически не усложнило код
# еще не стал делать проверку аргументов, т.к. в тестовом задании дан шаблон команды для
# запуска скрипта, если нужно, могу прикрутить проверку.

# Спасибо вам за такое интересное задание! Очень бы хотел попасть на тех. собеседование и
# получить фидбек как можно было бы сделать код эффективнее.
