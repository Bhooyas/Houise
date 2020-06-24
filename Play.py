from random import choice

def claim(tickect,prise,remaing_numbers):
    if prise in [0,1]:
        for row in tickect:
            for i in row:
                if i in remaing_numbers:
                    return False
        return True
    elif prise == 2:
        not_num = 0
        for row in tickect:
            for i in row:
                if i not in remaing_numbers and i!=0:
                    not_num += 1
        if not_num >= 5:
            return True
        else:
            return False
    elif prise == 3:
        row = tickect[0]
        for i in row:
            if i in remaing_numbers:
                return False
        return True
    elif prise == 4:
        row = tickect[1]
        for i in row:
            if i in remaing_numbers:
                return False
        return True
    elif prise ==  5:
        row = tickect[2]
        for i in row:
            if i in remaing_numbers:
                return False
        return True
    elif prise == 6:
        for row in tickect:
            for i in row:
                if i <=50:
                    if i in remaing_numbers:
                        return False
        return True
    elif prise == 7:
        for row in tickect:
            for i in row:
                if i>=50:
                    if i in remaing_numbers:
                        return False
        return True
    else:
        return False


def generate_num(remaing_numbers=None):
    if remaing_numbers == None:
        remaing_numbers = list(range(1,91))
    color = choice(['255, 38, 139','3, 138, 34','3, 68, 173','230, 38, 255','255, 128, 38'])
    number = choice(remaing_numbers)
    remaing_numbers.remove(number)
    return number,remaing_numbers,color
