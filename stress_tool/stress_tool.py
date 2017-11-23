import random
import re
import requests
import signal
import sys
import time

import argparse

import prometheus_client as pclient


# strange thing
def signal_handler(signal, frame):
        print('Target stopped.')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


pc = pclient.ProcessCollector(namespace='docker',
                              pid=lambda: open('/var/run/docker.pid').read())


def load_memory(s):
    pc.collect()
    flag = True
    for ss in s:
        if flag:
            ss.set(random.randint(10**6, 10**7))
            flag = not flag
        else:
            ss.observe(random.randint(0, 100) / 100)
            flag = not flag


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-P', '--listen-address', default=8080)
    parser.add_argument('-n', '--metric-count', default=3)
    parser.add_argument('-s', '--message-frequency', default=15000)

    parser.add_argument('-r', '--readmode', default=False, action='store_true',
                        help='Tool read mode.')
    parser.add_argument('-l', '--prometheus-url', help='Prometheus URL to '
                                                       'connect and query.')
    parser.add_argument('-j', '--job-name', help='Prometheus job name'
                                                 'to read metrics. '
                                                 'Required -r.')
    parser.add_argument('-i', '--instance-name', help='Single instance to '
                                                      'read metrics from. '
                                                      'Required -r.')
    parser.add_argument('-rp', '--read-period', default=15000)
    return parser


def read_mode(parser):
    prom_url = parser.prometheus_url
    job = parser.job_name
    if job is None:
        job = ''
    elif not job.startswith('~'):
        job = '"%s"' % job
    instance = parser.instance_name
    if instance is None:
        instance = ''
    elif not instance.startswith('~'):
        instance = '"%s"' % instance

    if not instance and not job:
        raise ValueError('Incorrect job and instance names. Aborting..')

    query_string = ('{' + ('instance=%s' % instance if instance else '') +
                    (', job=%s' % job if job else '') + '}')
    while True:
        r = requests.get('http://%s/api/v1/query' % prom_url,
                         params={'query': query_string})
        match = re.search('\"status\":\s*\"success\"', r.text)
        if not match:
            print('Unsuccessful response: %s' % r.text)
        time.sleep(float(parser.read_period) * 0.001)


def write_mode(parser):
    # Start up the server to expose the metrics.
    pclient.start_http_server(int(parser.listen_address))
    # Generate some requests.
    s = []
    for i in range(int(parser.metric_count)):
        s.append(pclient.Gauge('random_metric_%s' % i, 'Random value metric'))
        s.append(pclient.Histogram('random_metric_histogram_%s' % i,
                                   'Random metric histogram'))
    while True:
        load_memory(s)
        time.sleep(float(parser.message_frequency) * 0.001)


def main():
    parser = parse_args().parse_args()
    if parser.readmode:
        read_mode(parser)
    else:
        write_mode(parser)


if __name__ == '__main__':
    main()
