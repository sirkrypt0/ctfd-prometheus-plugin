from prometheus_client.core import GaugeMetricFamily

from .db import (
    get_team_count,
    get_hidden_team_count,
    get_banned_team_count,
    get_challenge_solves,
    get_challenge_values,
    get_team_scores,
    get_team_solves,
)


class MetricsCollector(object):
    def __init__(self, app, logger) -> None:
        self.app = app
        self.logger = logger

    def collect(self):
        self.logger.debug("Collecting metrics")
        with self.app.app_context():
            c = GaugeMetricFamily(
                "ctfd_teams_total", "Total number of teams", labels=["type"]
            )
            hidden_team_count = get_hidden_team_count()
            c.add_metric(["hidden"], hidden_team_count)
            banned_team_count = get_banned_team_count()
            c.add_metric(["banned"], banned_team_count)
            active_team_count = get_team_count() - hidden_team_count - banned_team_count
            c.add_metric(["active"], active_team_count)
            yield c

            c = GaugeMetricFamily(
                "ctfd_challenge_solves_total",
                "Solves per challenges",
                labels=["id", "name"],
            )
            for challenge_id, name, solves in get_challenge_solves():
                c.add_metric([str(challenge_id), name], solves)
            yield c

            c = GaugeMetricFamily(
                "ctfd_challenge_value",
                "Value per challenges",
                labels=["id", "name"],
            )
            for challenge_id, name, value in get_challenge_values():
                c.add_metric([str(challenge_id), name], value)
            yield c

            c = GaugeMetricFamily(
                "ctfd_team_points_total",
                "Points per team",
                labels=["id", "name", "hidden", "banned"],
            )
            for account_id, name, score, banned, hidden in get_team_scores():
                c.add_metric([str(account_id), name, str(hidden), str(banned)], score)
            yield c

            c = GaugeMetricFamily(
                "ctfd_team_solves_total",
                "Solves per team",
                labels=["id", "name", "hidden", "banned"],
            )
            for account_id, name, solves, banned, hidden in get_team_solves():
                c.add_metric([str(account_id), name, str(hidden), str(banned)], solves)
            yield c
