#!/usr/bin/env python3

import argparse
from opensearchpy import OpenSearch
from faker import Faker
import json
import time
import socket
from datetime import datetime

# Configure OpenSearch client
client = OpenSearch(
    hosts=[{'host': 'localhost', 'port': 9200, 'scheme': 'http'}]
)
hostname = socket.gethostname()
current_date = datetime.now().strftime("%Y-%m-%d")
base_index_name = "syslog"

# Initialize Faker instance
faker = Faker()

def generate_log():
    """Generate a fake log entry."""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'syslog_level': faker.random_element(elements=('INFO', 'ERROR', 'WARNING', 'DEBUG')),
        'message': faker.sentence(),
        'service': faker.random_element(elements=('auth', 'payment', 'orders', 'users')),
        'user_id': faker.uuid4(),
        'ip_address': faker.ipv4(),
        'response_time_ms': faker.random_int(min=20, max=500),
        'host': hostname
    }
    return log_entry

def send_log_to_opensearch(index_name, log_entry):
    """Send a log entry to OpenSearch."""
    response = client.index(index=index_name, body=log_entry)
    return response

def generate_and_send_logs(index_name, interval, max_messages):
    """Generate and send log entries to OpenSearch on a schedule, stopping after max_messages."""
    count = 0
    while count < max_messages:
        log_entry = generate_log()
        response = send_log_to_opensearch(index_name, log_entry)
        print(f"Log sent to OpenSearch: {json.dumps(log_entry)}")
        count += 1
        time.sleep(interval)  # wait for the specified interval before sending the next log
    print(f"Sent {max_messages} log entries. Stopping.")

if __name__ == "__main__":
    # Argument parser with usage description
    parser = argparse.ArgumentParser(
        description="Generate and send log entries to OpenSearch.",
        usage="%(prog)s [options]"
    )
    
    parser.add_argument('-i', '--interval_seconds', type=int, default=5, 
                        help='Time interval between logs in seconds (default: 5 seconds)')
    parser.add_argument('-m', '--max_messages', type=int, default=10, 
                        help='Maximum number of log entries to send (default: 10 messages)')
    
    args = parser.parse_args()

    index_name = f"{base_index_name}-{current_date}"

    generate_and_send_logs(index_name, args.interval_seconds, args.max_messages)
