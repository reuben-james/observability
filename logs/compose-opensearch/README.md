# Deploy Opensearch with docker-compose

## Pre-requisites

Extract from `https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/` for improved performance settings: 
```
sudo swapoff -a
```

```
# Edit the sysctl config file
sudo vi /etc/sysctl.conf

# Add a line to define the desired value
# or change the value if the key exists,
# and then save your changes.
vm.max_map_count=262144

# Reload the kernel parameters using sysctl
sudo sysctl -p

# Verify that the change was applied by checking the value
cat /proc/sys/vm/max_map_count
```

See opensearch docs for further configuration options: `https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/`

## Insecure Dev instance

### Set environment vars

```
echo OPENSEARCH_INITIAL_ADMIN_PASSWORD=<YOUR_ADMIN_PASSWORD> > .env
source .env
```

### Run the stack

```
docker compose -f docker-compose-dev.yml up -d
```

### Verify Opensearch is running

```
curl -XGET 'http://localhost:9200/_cat/allocation?v'
```

You should see output like this: 
```
shards disk.indices disk.used disk.avail disk.total disk.percent host       ip         node
     5        117kb      12gb     26.6gb     38.7gb           31 172.18.0.3 172.18.0.3 opensearch-node1
     5        114kb      12gb     26.6gb     38.7gb           31 172.18.0.4 172.18.0.4 opensearch-node2
```

## Secure Dev stack

Sometimes you need to develop against a more representative stack, with higher security configurations. 

To apply custom externally provided certificates, use the `docker-compose.yml` which is a more representative configuration of opensearch and kibana. 

### Run the stack

```
docker compose -f docker-compose.yml up -d
```