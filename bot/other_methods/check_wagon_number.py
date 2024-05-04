import math


def check_wagon_number(number):
    pre_control_sum = 0
    count = 0
    number_list = []
    prod_control_number_list = []
    weight_factor = [2, 1, 2, 1, 2, 1, 2]
    for item in number:
        number_list.append(int(item))
    control_number_list = number_list[:-1]
    check_control_sum = int(number_list[-1])
    while count < len(control_number_list):
        prod_control_number_list.append(weight_factor[count] * control_number_list[count])
        count += 1
    for item in prod_control_number_list:
        while item > 0:
            pre_control_sum += item % 10
            item //= 10
    control_sum = math.ceil(pre_control_sum / 10) * 10 - pre_control_sum
    if control_sum == check_control_sum:
        return True
    else:
        return False


def get_wagon_type(number):
    number_type = {2: 'крытые вагоны', 3: 'прочие(специализированные) вагоны', 4: 'платформы', 6: 'полувагоны', 7: 'цистерны', 8: 'изотермические вагоны', 9: 'прочие(специализированные) вагоны'}
    return number_type.get(int(number[1]))