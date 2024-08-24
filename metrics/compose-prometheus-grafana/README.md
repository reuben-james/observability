# Prometheus and Grafana stack in docker compose

The prometheus and grafana deployment here assumes you've already installed the node_exporter role to the docker host. See `prometheus_node_exporter/README.md` for more detail. 

## Pre-requisites

* docker & docker compose

Install docker & compose on Ubuntu
```
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```

## Prometheus config as code

### Targets

Targets are configured in `prometheus/prometheus.yml`

This project starts with config to scrape the docker host's node_exporter. 

## Grafana config as code

### Grafana Admin Creds

Set the `GF_SECURITY_ADMIN_PASSWORD` env variable so it can be passed into docker-compose.yml
```
echo GF_SECURITY_ADMIN_PASSWORD=<YOUR_GRAFANA_PASSWORD> > .env
source .env
```

### Datasources

This project provisions the prometheus datasource as well as the built-in TestData that comes with Grafana. 

If you need to add datasources, add them to `grafana/provisioning/datasources/all.yml` before bringing the stack up. 

### Dashboards

This deployment configures grafana to look in a local directory for dashboards, and provision them automatically on startup. The config file is located here `grafana/provisioning/datasources/all.yml`, and the docker-compose.yml maps the `grafana/provisioning/dashboards` folder into the container. 

You can manually develop Dashboards in the Grafana UI, then export the JSON to be saved to this folder to keep your dashboard definitions in code. 


## Run Prometheus and Grafana

```
docker compose up -d
```

Navigate to the Grafana UI `http://localhost:3000` and login with your `GF_SECURITY_ADMIN_PASSWORD` that you set earlier. 