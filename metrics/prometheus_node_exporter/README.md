# A simple ansible playbook to install the Prometheus Linux Node Exporter

## Pre-requisites

* python3
* ansible

Installed using pipenv 
```
pipenv install ansible
```

## Quickstart

Install the prometheus collection
```
ansible-galaxy collection install -r requirements.yml -p collections/
```

OR: Install just the node_exporter role
```
ansible-galaxy install -r requirements.yml -p roles/
```

Apply the collection role to localhost
```
ansible-playbook -i hosts all playbook-node-exporter-collection.yml
```

OR: Apply the standalone role to localhost
```
ansible-playbook -i hosts all playbook-node-exporter-role.yml
```

After you've successfully run the ansible playbook, test the metrics endpoint
```
curl http://localhost:9100/metrics
```
