import re
import subprocess
import time
from prometheus_client import start_http_server, Gauge

# create Prometheus metrics
ping_time_ipv4 = Gauge('ping_time_ipv4', 'Response time for IPv4 ping', ['target'])
ping_time_ipv6 = Gauge('ping_time_ipv6', 'Response time for IPv6 ping', ['target'])

# the list of the hosts to execute ping
targets = ['www.amazon.co.jp', 'www.google.com']

def ping(target, version):
    """
    Execute ping command to specified host and retrieve response time
    version: 4 (IPv4) or 6 (IPv6)
    """
    ping_command = ['ping', '-c', '1', '-W', '1']  # Timeout 1 sec
    if version == 4:
        ping_command.extend(['-4'])  # IPv4
    else:
        ping_command.extend(['-6'])  # IPv6
    ping_command.append(target)

    try:
        output = subprocess.check_output(ping_command, universal_newlines=True)
        match = re.search(r'time=(\d+\.\d+) ms', output)
        if match:
            response_time = float(match.group(1))
            return response_time
    except subprocess.CalledProcessError:
        pass

    return float('nan')  # If ping fails, recrod nan

if __name__ == '__main__':
    # Start exporter
    start_http_server(8406)

    # Update metrics periodically
    while True:
        for target in targets:
            ping_time_ipv4.labels(target=target).set(ping(target, 4))
            ping_time_ipv6.labels(target=target).set(ping(target, 6))
        time.sleep(10)  # Update every 10 secs
