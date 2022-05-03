from .config import comps


def get_recommendation(user1, user2):
    return any([
        cur['comp_func'](*map(cur['prepare_func'], (user1, user2)), cur['ok_point'])
        for cur in comps
    ])
