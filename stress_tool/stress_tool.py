import argparse
import random
import string
import time

from prometheus_client import start_http_server, Summary

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_time_stress', 'Time of request stress')


@REQUEST_TIME.time()
def load_memory(a, s):
    for ss in s:
        ss.observe(random.randint(10**6, 10**7))
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
    start_http_server(int(parser.listen_address))
    # Generate some requests.
    s = []
    for i in range(int(parser.metric_count)):
        s.append(Summary('random_metric_%s' % i, 'Random value metric'))
    while True:
        a = []
        a = load_memory(a, s)
        time.sleep(float(parser.message_frequency) * 0.001)
