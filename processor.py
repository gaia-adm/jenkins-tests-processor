#!/usr/bin/env python3.4
import sys
import signal
import json
from datetime import datetime
from utils import get_params

def signal_handler(_signo, _stack_frame):
    sys.stderr.write('Caught ' + _signo + ', exiting')
    sys.exit(1)

signal.signal(signal.SIGTERM, signal_handler)

def get_json_parser():
    ijson = None
    try:
        # try to use yajl dll/so first (faster)
        import ijson.backends.yajl2 as ijson
    except ImportError:
        # if not yajl available, use Python JSON parser
        import ijson.backends.python as ijson
    finally:
        return ijson

def parseClassName(class_name):
    if class_name.endswith('.story'):
        # i.e stories/sanity/ci-sanity/myName.story
        index = class_name.rfind('/')
    else:
        # TODO: class name format may be language specific, this works for Java
        index = class_name.rfind('.')
    if index != -1 and (index + 1) <= len(class_name):
        return class_name[:index], class_name[index + 1:]
    else:
        return None, class_name

def create_test_execution_event(content_metadata, custom_metadata, test_execution):
    test_run_event = {'event': 'code_testrun'}
    test_run_event['time'] = datetime.utcfromtimestamp(int(custom_metadata['BUILD_TIMESTAMP']) / 1000).isoformat()
    # source
    source = {}
    source['location_uri'] = custom_metadata.get('LOCATION_URI')
    source['job_name'] = custom_metadata.get('JOB_NAME')
    source['root_job_name'] = custom_metadata.get('ROOT_JOB_NAME')
    test_run_event['source'] = source
    # tags
    tags = {}
    tags['build_uri_path'] = custom_metadata.get('BUILD_URI_PATH')
    tags['build_result'] = custom_metadata.get('BUILD_RESULT')
    custom_tags_str = custom_metadata.get('CUSTOM_TAGS')
    if custom_tags_str:
        custom_tags = custom_tags_str.split(',')
        for custom_tag in custom_tags:
            tags[custom_tag.lower()] = custom_metadata.get(custom_tag)
    test_run_event['tags'] = tags
    # id part
    id = {}
    id['method'] = test_execution['name']
    package, clazz = parseClassName(test_execution['className'])
    if package != None:
        id['package'] = package
    if clazz != None:
        id['class'] = clazz
    id['build_number'] = custom_metadata.get('BUILD_NUMBER')
    id['root_build_number'] = custom_metadata.get('ROOT_BUILD_NUMBER')
    test_run_event['id'] = id
    # result part
    result = {}
    result['status'] = test_execution['status']
    result['error_details'] = test_execution.get('errorDetails')
    result['skipped'] = test_execution.get('skipped')
    result['skipped_message'] = test_execution.get('skippedMessage')
    result['failed_since'] = test_execution.get('failedSince')
    result['age'] = test_execution.get('age')
    result['duration'] = float(test_execution.get('duration'))
    test_run_event['result'] = result
    return test_run_event

def process_test_execution(content_metadata, custom_metadata, test_execution):
    # create the test run event object
    event = create_test_execution_event(content_metadata, custom_metadata, test_execution)
    # write the object on stdout in JSON
    sys.stdout.write(json.dumps(event))

def process_tests_json(content_metadata, custom_metadata):
    sys.stdout.write('[')
    ijson = get_json_parser()
    # parser = ijson.parse(open('c:\jenkins-stories.json', mode='rb'))
    parser = ijson.parse(sys.stdin.buffer)
    count = 0
    test_execution = None
    expected_key = None
    for prefix, event, value in parser:
        # we only care about suites cases, don't care about root object or suites properties
        if prefix == 'suites.item.cases.item':
            if event == 'start_map':
                test_execution = {}
            elif event == 'end_map':
                if count > 0:
                    sys.stdout.write(',')
                process_test_execution(content_metadata, custom_metadata, test_execution)
                count = count + 1
            elif event == 'map_key':
                expected_key = value
        else:
            if expected_key != None and prefix == ('suites.item.cases.item.' + expected_key):
                test_execution[expected_key] = value
            expected_key = None
        # print(prefix + ':' + event + ':' + str(value))
    sys.stdout.write(']')

content_metadata, custom_metadata = get_params()

if len(content_metadata) > 0:
    process_tests_json(content_metadata, custom_metadata)
else:
    # no parameters, just exit
    print('[]')
    sys.exit(0)
