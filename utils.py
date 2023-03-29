def my_sorted(iterable, *, key=lambda x: x, reverse=False):
    """
    Functie sortare
    :param iterable:lista
    :param key:lambda()
    :param reverse: (bool) True sau False
    :return:lista sortata
    """
    try:
        lst = iterable
        n = len(lst)

        if reverse is False:
            for i in range(n):
                for j in range(1, n):
                    if key(lst[j-1]) > key(lst[j]):
                        lst[j - 1], lst[j] = lst[j], lst[j - 1]

        if reverse is True:
            for i in range(n):
                for j in range(1, n):
                    if key(lst[j - 1]) < key(lst[j]):
                        lst[j - 1], lst[j] = lst[j], lst[j - 1]

        return lst
    except Exception as e:
        print(e)
