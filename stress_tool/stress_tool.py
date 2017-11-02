import argparse
import random
import time

import prometheus_client as pclient

pc = pclient.ProcessCollector(namespace='docker',
                              pid=lambda: open('/var/run/docker.pid').read())


def load_memory(a, s):
    pc.collect()
    flag = True
    for ss in s:
        if flag:
            ss.set(random.randint(10**6, 10**7))
            flag = not flag
        else:
            ss.observe(random.randint(10**6, 10**7))
            flag = not flag
    return a


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--listen-address', default=8080)
    parser.add_argument('--metric-count', default=3)
    parser.add_argument('--message-frequency', default=15000)
    return parser


if __name__ == '__main__':
    parser = parse_args().parse_args()
    # Start up the server to expose the metrics.
    pclient.start_http_server(int(parser.listen_address))
    # Generate some requests.
    s = []
    for i in range(int(parser.metric_count)):
        s.append(pclient.Gauge('random_metric_%s' % i, 'Random value metric'))
        s.append(pclient.Histogram('random_metric_histogram_%s' % i,
                                   'Random metric histogram'))
    while True:
        a = []
        a = load_memory(a, s)
        time.sleep(float(parser.message_frequency) * 0.001)
