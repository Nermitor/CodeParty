fields_to_check = ['languages']
ok_point = 0.4


def prepare_function(field: str):
    return set(field.split(', '))


def compare_function(user, maybe_for_rec):
    if len(user & maybe_for_rec) / len(user) >= ok_point:
        return True
    return False

