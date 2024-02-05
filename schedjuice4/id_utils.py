import random
from datetime import date


def add_til_1(input_num:int):
    while len(str(input_num)) > 1:
        input_num = sum([int(i) for i in list(str(input_num))])
    return input_num



def make_check_digit(input_num:str):
    # if len(input_num) != 4:
    #    raise Exception("Input number must be of length 4")
    i0, i1,i2, i3 = [int(i) for i in list(input_num)[0:4]]
    x = add_til_1(i0**6 + i1**2 + i2**6 + i3**9)
    y = add_til_1(i0**9 + i1**6 + i2**3 + i3**6)
    z = add_til_1((x+y)*x**y + 31415)
    alphat = add_til_1(z*3)
    return str(alpha)


def check_validity(student_id:str):
    body = student_id[2:6]

    check_digit = student_id[-1]
    if make_check_digit(body) == check_digit:
        return True
    return False



def id_creator(model_set):
    existing_ids = {i.student_id[2:6] for i in model_set}
    this_year = date.today().year
    available_ids = {str(i) for i in range(1000,19999)}.difference(existing_ids)
    random_num = random.choice(list(available_ids))

    the_id = str(this_year)[2:4] + str(random_num) + make_check_digit(random_num)

    return the_id
