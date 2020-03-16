import os
import sys
from collections import defaultdict
import json


def get_cmd_arg(name):
    d = defaultdict(list)
    for cmd_args in sys.argv[1:]:
        cmd_arg = cmd_args.split('=')
        if len(cmd_arg) == 2:
            d[cmd_arg[0].lstrip('-')].append(cmd_arg[1])

    if name in d:
        return d[name][0]
    # if 'SPRING_APPLICATION_JSON' in os.environ and name in json.loads(os.environ['SPRING_APPLICATION_JSON']):
    #     return json.loads(os.environ['SPRING_APPLICATION_JSON'])[name]
    else:
        print('Unknown command line arg requested: {}'.format(name))

def get_env_var(name):
    if name in os.environ:
        return os.environ[name]
    # if 'SPRING_APPLICATION_JSON' in os.environ and name in json.loads(os.environ['SPRING_APPLICATION_JSON']):
    #     return json.loads(os.environ['SPRING_APPLICATION_JSON'])[name]
    else:
        print('Unknown environment variable requested: {}'.format(name))
            
def get_kafka_binder_brokers():
    # if 'SPRING_APPLICATION_JSON' in os.environ:
    #     return "kafka-broker:9092"
    # else:
        return get_env_var('SPRING_CLOUD_STREAM_KAFKA_BINDER_BROKERS')

def get_input_channel():
    return get_cmd_arg("spring.cloud.stream.bindings.input.destination")

def get_output_channel():
    return get_cmd_arg("spring.cloud.stream.bindings.output.destination")

def get_reverse_string():
    return get_cmd_arg("reversestring")
