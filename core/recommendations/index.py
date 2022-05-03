from data.db_session import create_session
from data.__all_models import User, recommendations
from .get import get_recommendation


def index():
    print("Индексация начата.")
    with create_session() as db_sess:
        db_sess.query(recommendations).delete()
        max_id = max(db_sess.query(User.id).all()).id
        indexed = set()
        for i in range(1, max_id + 1):
            user1 = db_sess.query(User).get(i)
            for j in range(i, max_id + 1):
                if i != j and (i, j) not in indexed and (j, i) not in indexed:
                    user2 = db_sess.query(User).get(j)
                    if get_recommendation(user1, user2):
                        user1.recommendations.append(user2)
                    if get_recommendation(user2, user1):
                        user2.recommendations.append(user1)
                    indexed.add((i, j))
            print(f"Составлены рекомендации для пользователя {user1.nickname}")
        db_sess.commit()

