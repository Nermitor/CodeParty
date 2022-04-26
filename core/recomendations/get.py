from .config import prepare_function, compare_function, fields_to_check, ok_point


def get_recommendation(user1, user2):
    return max(compare_function(
        prepare_function(getattr(user1, i)),
        prepare_function(getattr(user2, i)))
        for i in fields_to_check
    ) >= ok_point
