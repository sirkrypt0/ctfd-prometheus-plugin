from sqlalchemy.sql import and_

from CTFd.models import Challenges, Teams, Solves, db
from CTFd.utils.modes import get_model
from CTFd.utils.scores import get_standings


def get_chals():
    chals = (
        Challenges.query.filter(
            and_(Challenges.state != "hidden", Challenges.state != "locked")
        )
        .order_by(Challenges.value)
        .all()
    )
    return chals


def get_challenge_solves():
    Model = get_model()

    if Model is None:
        return []

    solves_sub = (
        db.session.query(
            Solves.challenge_id, db.func.count(Solves.challenge_id).label("solves")
        )
        .join(Model, Solves.account_id == Model.id)
        .filter(Model.banned == False, Model.hidden == False)
        .group_by(Solves.challenge_id)
        .subquery()
    )

    solves = (
        db.session.query(
            solves_sub.columns.challenge_id,
            Challenges.name,
            Challenges.category,
            solves_sub.columns.solves,
        )
        .join(Challenges, solves_sub.columns.challenge_id == Challenges.id)
        .all()
    )

    has_solves = [c[0] for c in solves]
    for c in get_chals():
        if c.id not in has_solves:
            solves.append([c.id, c.name, c.category, 0])

    return solves


def get_challenge_values():
    return [(c.id, c.name, c.category, c.value) for c in get_chals()]


def get_team_count():
    Model = get_model()
    if Model is None:
        return 0
    return Model.query.count()


def get_hidden_team_count():
    Model = get_model()
    if Model is None:
        return 0
    return Model.query.filter(Model.hidden == True).count()


def get_banned_team_count():
    Model = get_model()
    if Model is None:
        return 0
    return Model.query.filter(Model.banned == True).count()


def get_teams():
    Model = get_model()
    if Model is None:
        return []
    return Model.query.all()


def get_team_scores():
    scores = []
    has_score = []
    for s in get_standings(admin=True):
        scores.append((s.account_id, s.name, s.score, s.banned, s.hidden))
        has_score.append(s.account_id)
    for t in get_teams():
        if t.id not in has_score:
            scores.append((t.id, t.name, 0, t.banned, t.hidden))
    return scores


def get_team_solves():
    Model = get_model()

    if Model is None:
        return []

    solves = (
        db.session.query(
            Solves.account_id,
            Model.name,
            db.func.count(Solves.challenge_id).label("solves"),
            Model.banned,
            Model.hidden,
        )
        .join(Model, Solves.account_id == Model.id)
        .group_by(Solves.account_id)
        .all()
    )

    has_solves = [t[0] for t in solves]
    for t in get_teams():
        if t.id not in has_solves:
            solves.append((t.id, t.name, 0, t.banned, t.hidden))

    return solves
