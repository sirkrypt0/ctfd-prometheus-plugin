# CTFd Prometheus Metrics

A CTFd plugin that adds a Prometheus metrics endpoint. Authentication included!

## Install

1. Copy or clone this repository into the `CTFd/plugins` folder.
1. Install the Python requirements.
    - If you installed CTFd on your host directly, run `pip install -r requirements.txt` inside this plugin's folder.
    - If you run CTFd using the official Dockerfile, make sure to rebuild the image, as the plugins' requirements are installed during build time.

## Configuration

The following configuration options exist that can be either specified in the CTFd configuration or as an environment variable.
The value in the CTFd configuration supersedes the environment variable.

- `PROMETHEUS_ENABLED`: If set, this plugin is enabled.
- `PROMETHEUS_AUTH_TOKEN`: If this plugin is enabled, this option must be set to receive metrics. Then, the specified token must be set as a `Bearer` token in the HTTP `Authorization` header as access to the metrics is otherwise forbidden.

### Prometheus

Prometheus can be configured as follows.

```yaml
scrape_configs:
  - job_name: 'ctfd'
    authorization:
      type: Bearer
      credentials: <auth-token>
    static_configs:
      - targets: ['<https://ctfd.example.com>']
```

## Metrics

In addition to the [default metrics](https://github.com/prometheus/client_python/tree/master#process-collector) exported by the Prometheus Python client, the following CTFd-specific metrics are exported..

```prometheus
# HELP ctfd_teams_total Total number of teams
# TYPE ctfd_teams_total gauge
ctfd_teams_total{type="hidden"} 1.0
ctfd_teams_total{type="banned"} 0.0
ctfd_teams_total{type="active"} 1.0
# HELP ctfd_challenge_solves_total Solves per challenges
# TYPE ctfd_challenge_solves_total gauge
ctfd_challenge_solves_total{id="1",name="test"} 0.0
ctfd_challenge_solves_total{id="2",name="test2"} 0.0
# HELP ctfd_team_points_total Points per team
# TYPE ctfd_team_points_total gauge
ctfd_team_points_total{banned="False",hidden="True",id="1",name="Platypwnies"} 2000.0
ctfd_team_points_total{banned="False",hidden="False",id="2",name="Some Team"} 0.0
# HELP ctfd_team_solves_total Solves per team
# TYPE ctfd_team_solves_total gauge
ctfd_team_solves_total{banned="False",hidden="True",id="1",name="Platypwnies"} 2.0
ctfd_team_solves_total{banned="False",hidden="False",id="2",name="Some Team"} 0.0
```
