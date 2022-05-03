def prepare_function(user):
    return set(user.languages.split(', '))


def to_language_comp(user, maybe_for_rec, ok_point):
    if len(user & maybe_for_rec) / len(user) >= ok_point:
        return True
    return False


def follows_comp(user, maybe_for_rec, ok_point):
    g = user.common_follows(maybe_for_rec).count() >= ok_point
    return g


def followed_comp(user, maybe_for_rec, ok_point):
    c = 0
    for u1 in user.follows.all():
        if u1.is_following(maybe_for_rec):
            c += 1
    return c >= ok_point


comps = [
    {
        "prepare_func": prepare_function,
        "comp_func": to_language_comp,
        "ok_point": 0.6
    },
    {
        "prepare_func": lambda x: x,
        "comp_func": follows_comp,
        "ok_point": 1
    },
    {
        "prepare_func": lambda x: x,
        "comp_func": followed_comp,
        "ok_point": 2
    }
]
