GRADES = ['Primaire', '6ème', '5ème', '4ème', '3ème',
          'Seconde', 'Première', 'Terminale', 'Supérieur']


def check_field_validity(f, f_list, attr):
    for item in f_list:
        if f == item.attr:
            return False
    return True


def get_grade_from_range(g_from, g_to):
    i = GRADES.index(g_from)
    j = GRADES.index(g_to)
    grades = GRADES[i:j+1]
    return grades


def check_tuple_in_list(t, test_elem, list_tuples):
    res = [item for item in list_tuples
           if item[0] == test_elem[0] and (item[1] >= test_elem[1] or item[2] >= test_elem[2])]
    return res, t




