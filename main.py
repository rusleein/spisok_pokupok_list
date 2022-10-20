from prettytable import PrettyTable
import copy

vvod = None
itog = []
mis = ['-' * 30, 'Что-то пошло не так. Некорректные данные. Введите еще раз.', '-' * 30]  # шаблон вывода ОШИБКИ
mistake = '''Что-то пошло не так. Некорректные данные. Введите:
        - "Изменить", если хотите что-либо изменить в списке,
        - "Удалить",если хотите что - либо удалить из списка,
        - "Продолжить", если хотите продолжить заполнение списка, 
        - "Стоп", если хотите закончить работу со списком. '''  # Шаблон ошибки в ВЫБОРЕ ДЕЙСТВИЯ

print('-' * 120)
print('''Добро пожаловать в "Список покупок".')                                                                        |
Данная программа подсчитает список Ваших покупок и выведет на экран список и сумму покупок.                            |
При каждом шаге работе программы, Вам будет показана инструкция по использованию.                                      |
Возможности данной программы:                                                                                          |
    - Подсчет покупок;                                                                                                 |
    - Подсчет суммы по каждой позиции;                                                                                 | 
    - Подсчет итоговой суммы покупки;                                                                                  |
    - Программе не нужно объяснять, что наименование ВЕСОВОЕ, она сама это поймет, когда Вы введете НЕ ЦЕЛОЕ число;    |
    - Вы не сможете Ввести в программу в кач-ве товара некорректное значение. Т.Е. Вы не сможете ввести количество,    |
либо цену товара буквами, программа поймет это. Вы не сможете ввести наименование без количества,                      |
либо без цены, программа поймет это;                                                                                   |    
    - В случае, если Вы завершили подсчет, но потом поняли что забыли что-то внести в список, программа продолжит свою | 
работу до тех пор, пока после "Итога" не будет введено "Стоп";                                                         |
Правила использования программы:                                                                                       |
    Введите наименование товара, количество и цену через пробел.                                                       |
    Если, наименование : Банан, количество: 3 шт., цена: 24 руб., то пример ввода :Банан 3 24.                         |
    В случае, если наименовение весовое: Картошка, 3.4 кг 43 руб., то пример ввода :Картошка 3.4 43.                   |
    !!! В случае весового наименование, ВЕС ВВОДИТЬ С "." !!!                                                          |
Приятного использования!                                                                                               |
''')
print('-' * 120)


def is_number(st):  # Проверка на число
    try:
        float(st)
        return True
    except ValueError:
        return False


def is_int(s):  # Проверка на целое число
    try:
        int(s)
        return True
    except ValueError:
        return False


def pokupki():  # Функция для заполнения списка и продолжения заполнения
    spisok = ''
    global itog
    summa = 0
    while spisok not in [['Итог'], ['итог']]:  # Пока введено не "ИТОГ" продолжаем работу
        spisok = input('''Введите наименование товара, количество и цену ЧЕРЕЗ ПРОБЕЛ.
Если, наименование : Банан, количество: 3 шт., цена: 24 руб., то пример ввода :Банан 3 24.
В случае, если наименовение весовое: Картошка, 3.4 кг 43 руб., то пример ввода :Картошка 3.4 43.
!!! В случае весового наименование, ВЕС ВВОДИТЬ С "." !!!
Введите "Итог" для вывода списка Ваших покупок:''').split()  # Получаем наименование, кол-во и цену
        temp = [i for j in itog
                for i in j]  # временный список со всеми товарами для поиска дубликатов

        a = [spisok.index(i) for i in spisok if ',' in i]  # если "," в spisok, получаем индекс значения с ','
        # for i in spisok:
        #   if ',' in i:
        #       a = spisok.index(i) получили индекс значения с ','
        if a:  # Если список не пустой
            spisok[a[0]] = spisok[a[0]].replace(',', '.')  # меняем ',' на '.'

        if len(spisok) == 3 and is_number(spisok[1]) and is_number(spisok[2]) or spisok in [['Итог'], ['итог']]:
            # Если длина списка 3 и (кол- во и цена - числа) или введен "ИТОГ":
            if spisok in [['Итог'], ['итог']]:  # Если введено "ИТОГ", останавливаем цикл и выводим список
                break
            if not itog:  # Если itog пустой, добавляем spisok
                itog.append(spisok)
            else:  # Если itog не пустой
                if spisok[0] in temp:  # Если наименование уже есть в списке
                    ind = [i for i, x in enumerate(itog) if spisok[0] in x]  # Находим индекс наименования
                    itog[ind[0]][1] = float(itog[ind[0]][1])
                    itog[ind[0]][1] += round(float(spisok[1]), 2)  # Добавляем количество к наименованию
                else:
                    itog.append(spisok)  # Если наименования нет в списке, то просто добавляем его
        else:  # Если введеное значение не верное, то выводим ошибку и просим ввести товар еще раз
            print(*mis, sep='\n')

    global vvod
    vvod = PrettyTable(['№', 'Наименование', 'Количество', 'Цена за шт.', 'Сумма'])

    itog_2 = copy.deepcopy(itog)  # Делаем глубокую копию основного списка покупок, чтобы не изменять его
    vvod.clear_rows()  # очищаем ввод для внесения данных после изменения

    for i in itog_2:
        i.insert(0, itog_2.index(i) + 1)  # Добавляем столбец с счетчиком строк
        i.append(round(float(i[2]) * float(i[3]), 2))  # Сумма товара (кол-во * цену)
        summa += i[4]  # Итоговая сумма
        if not is_int(i[2]):  # Если число НЕ целое, то будет КГ., если целое, то ШТ.
            i[2] = str(round(float(i[2]), 2)) + ' кг.'
        else:
            i[2] = str(i[2]) + ' шт.'
        i[3] = str(i[3]) + ' руб.'  # добавляем приписку ".руб" к итоговому списку
        i[4] = str(i[4]) + ' руб.'  # добавляем приписку ".руб" к итоговому списку
        vvod.add_row(i)  # Добавляем строку в итоговый список

    print(vvod)  # Выводим список
    print(PrettyTable(['Итого: ' + str(round(summa, 2)) + ' Руб.']))  # Выводим итоговую сумму
    global choice
    choice = input('''
            Если хотите продолжить заполнение списка, введите "Продолжить" (1)
            Если хотите что-либо изменить в списке, введите "Изменить" (2)
            Если хотите что - либо удалить из списка, введите "Удалить" (3)    
            Если хотите закончить работу со списком, введите "Стоп": ''')


def change():
    summ = 0
    print(vvod)  # Выводим список для выбора нужной строки для изменения

    s = input("Какой товар хотите изменить? Введите номер строки:")
    flag_str = False
    while not flag_str:  # Получаем номер строки
        if is_int(s) and s in [str(i) for i in range(len(itog) + 1)]:
            flag_str = True
            stroka = s  # если введено число и номер строки есть в списке, flag
        else:
            print(*mis, sep='\n')
            s = input("Какой товар хотите изменить? Введите номер строки:")

    chto_menyaem = input('''Что хотите изменить, наименование, количество или цену? 
    Если хотите изменить наименование, введите "1", кол-во - введите "2", цену - "3":''')  # Получаем номер столбца
    while chto_menyaem not in ['1', '2', '3']:  # Проверяем введеное значение
        print(*mis, sep='\n')
        chto_menyaem = input('''Что хотите изменить, наименование, количество или цену? 
            Если хотите изменить наименование, введите "1", кол-во - введите "2", цену - "3":''')

    flag_done = False  # если flag, значит значение введено верно
    while not flag_done:  # пока not flag, продолжаем проверку
        done = input('На что хотите изменить?:')  # Получаем значение на которое будем менять и проверяем его
        if ',' in done:  # меняем "," на ".", чтобы не было проблем с float
            done = done.replace(',', '.')
        if (int(chto_menyaem) == 2 and is_number(done)) or (int(chto_menyaem) == 3 and is_number(done)):
            flag_done = True  # если выбрано кол-во или цена и введено число, flag
        elif int(chto_menyaem) == 1:
            flag_done = True  # если выбрано для изменения наименование, flag
        else:
            print(*mis, sep='\n')

    itog[int(stroka) - 1][int(chto_menyaem) - 1] = done  # меняем старное значение на новое

    itogg = copy.deepcopy(itog)  # Копируем основной список покупок, чтобы не изменять его
    vvod.clear_rows()  # очищаем список для вывода нового
    for i in itogg:
        i.insert(0, itogg.index(i) + 1)  # Добавляем столбец с счетчиком строк
        i.append(round(float(i[2]) * float(i[3]), 2))  # Сумма товара (кол-во * цена)
        summ += i[4]  # Итоговая сумма

        if not is_int(i[2]):  # Если число НЕ целое, то будет КГ., если целое, то ШТ.
            i[2] = str(round(float(i[2]), 2)) + ' кг.'
        else:
            i[2] = str(i[2]) + ' шт.'
        i[3] = str(i[3]) + ' руб.'  # добавляем приписку ".руб" к итоговому списку
        i[4] = str(i[4]) + ' руб.'  # добавляем приписку ".руб" к итоговому списку
        vvod.add_row(i)
    print(vvod)
    print(PrettyTable(['Итого: ' + str(round(summ, 2)) + ' Руб.']))
    global choice
    choice = input('''
            Если хотите продолжить заполнение списка, введите "Продолжить" (1)
            Если хотите что-либо изменить в списке, введите "Изменить" (2)
            Если хотите что - либо удалить из списка, введите "Удалить" (3)    
            Если хотите закончить работу со списком, введите "Стоп": ''')


def delete():
    global itog
    global vvod
    print(vvod)
    del_vvod = input('''
    Введите "1" если хотите удалить строку,
    Введите "2" если хотите очистить список. 
    Обратите внимание, список удалить !!!БЕЗВОЗВРАТНО!!!: ''')
    while del_vvod not in ['1', '2']:  # Проверяем введеное значение
        print(*mis, sep='\n')
        del_vvod = input('''
        Введите "1" если хотите удалить строку,
        Введите "2" если хотите очистить список: ''')
    if del_vvod == '2':
        vvod.clear_rows()
        itog = []  # очищаем список для того, чтобы после удаления он был пуст
        print(vvod)
    if del_vvod == '1':
        print(vvod)
        num_str = input('Введите номер строки, которую хотели бы удалить:')
        flag_del_str = False
        while not flag_del_str:  # Получаем номер строки
            if is_int(num_str) and num_str in [str(i) for i in range(len(itog) + 1)]:
                flag_del_str = True
                num_del_str = int(num_str)  # если введено число и номер строки есть в списке, flag
            else:
                print(*mis, sep='\n')
                num_str = input('Введите номер строки, которую хотели бы удалить:')
        itog.pop(num_del_str - 1)  # удаляем строку из списка
        vvod.del_row(num_del_str - 1)  # удаляем строку из итогового
        print(vvod)

    global choice
    choice = input('''
        Если хотите продолжить заполнение списка, введите "Продолжить" (1)
        Если хотите что-либо изменить в списке, введите "Изменить" (2)
        Если хотите что - либо удалить из списка, введите "Удалить" (3)    
        Если хотите закончить работу со списком, введите "Стоп": ''')


pokupki()

while choice.lower() not in ['стоп']:
    if choice.lower() in ['изменить', '2']:
        if itog:
            change()
        else:
            print('- ' * 30)
            print('Список покупок пуст, сначала заполните его, затем переходите к изменению.')
            print('- ' * 30)
            choice = input('''
                    Если хотите продолжить заполнение списка, введите "Продолжить" (1)
                    Если хотите что-либо изменить в списке, введите "Изменить" (2)
                    Если хотите что - либо удалить из списка, введите "Удалить" (3)    
                    Если хотите закончить работу со списком, введите "Стоп": ''')
    if choice.lower() in ['продолжить', '1']:
        pokupki()
    elif choice.lower() in ['удалить', '3']:
        if itog:
            delete()
        else:
            print('- ' * 30)
            print('Список покупок пуст, сначала заполните его, затем переходите к удалению элементов.')
            print('- ' * 30)
            choice = input('''
                    Если хотите продолжить заполнение списка, введите "Продолжить" (1)
                    Если хотите что-либо изменить в списке, введите "Изменить" (2)
                    Если хотите что - либо удалить из списка, введите "Удалить" (3)    
                    Если хотите закончить работу со списком, введите "Стоп": ''')
    else:
        print('- ' * 30)
        choice = input(mistake)
        print('- ' * 30)

else:
    print('- ' * 30)
    print('Спасибо за использование. Хорошего дня!')
    print('- ' * 30)


#  Добавить удаление и изменение(+) +
#  Убрать "что-то не так" после "ИТОГ"  +
#  Изменение:  +
#  Добавить фильтр на вводимую информацю в CHANGE()  +
#  Убрать дублирование запроса CHOICE во время второго выбора  +
#
#

