def is_positive_number(value):
    try:
        number_string = float(value)
    except Exception as e:
        print(e)
        return False
    return number_string > 0


print(is_positive_number('6'))
