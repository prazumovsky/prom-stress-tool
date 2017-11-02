import argparse
import random
import signal
import sys
import time

import prometheus_client as pclient

# strange thing
def signal_handler(signal, frame):
        print('Target stopped.')
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

pc = pclient.ProcessCollector(namespace='minion',
                              pid=lambda: open('/var/run/salt-minion.pid').read())


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
    return parser


def main():
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
        load_memory(s)
        time.sleep(float(parser.message_frequency) * 0.001)


if __name__ == '__main__':
    main()
