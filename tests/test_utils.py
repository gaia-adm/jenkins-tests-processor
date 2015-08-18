import json
import os
import subprocess


def execute_processor(input_file, processor_descriptor_file=None, content_metadata=None, data_type=None,
                      custom_metadata=None):
    """
    Executes a data processor identified by given processor descriptor path on file system. This very simple
    processor executor is only meant to be used in tests.

    Returns result from data processor STDOUT in the form of bytes. If the processor exited with non 0 code,
    CalledProcessError will be raised. TimeoutExpired will be raised if timeout occurs during processor execution.

    :param processor_descriptor_file: path on file system to processor-descriptor.json file. If not provided parent directory
           and current working directory are checked.
    :param input_file: path of file with input to pass to data processor on STDIN
    :param content_metadata: optional, dictionary with content metadata. Keys passed to processor are case insensitive.
           If not provided default content metadata will be provided (for JSON content).
    :param data_type: optional, allows to specify data type of content. This will be something like 'jenkins/test'.
           If the processor descriptor defines only one dataType, its value will be used.
    :param custom_metadata: optional, dictionary with custom metadata.
    """
    # read processor descriptor JSON
    if processor_descriptor_file is None:
        # try parent dir of this file
        processor_descriptor_file = os.path.join(
            os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)),
            'processor-descriptor.json')
        # try current working directory
        if not os.path.isfile(processor_descriptor_file):
            processor_descriptor_file = os.path.join(os.getcwd(), 'processor-descriptor.json')
        # try parent of working directory
        if not os.path.isfile(processor_descriptor_file):
            processor_descriptor_file = os.path.abspath(
                os.path.join(os.getcwd(), os.pardir, 'processor-descriptor.json'))
        if not os.path.isfile(processor_descriptor_file):
            raise Exception('Unable to find processor-descriptor.json')

    with open(processor_descriptor_file, "rt") as myfile:
        processor_descriptor = json.load(myfile)

    # prepare content_metadata & custom_metadata
    if content_metadata is None:
        content_metadata = {'contentType': 'application/json;charset=utf-8', 'mimeType': 'application/json',
                            'charset': 'utf-8'}
    if data_type:
        content_metadata['dataType'] = data_type
    if 'dataType' not in content_metadata:
        consumes_arr = processor_descriptor['consumes']
        if len(consumes_arr) == 1:
            d_data_type = consumes_arr[0].get('dataType')
            if d_data_type:
                content_metadata['dataType'] = d_data_type
    if custom_metadata is None:
        custom_metadata = {}

    # add prefix to content_metadata
    content_metadata = {'P_' + key.upper(): content_metadata[key] for key in content_metadata}
    # add prefix to custom_metadata
    custom_metadata = {'P_C_' + key.upper(): custom_metadata[key] for key in custom_metadata}

    # perform processor execution
    command = processor_descriptor['command']
    cwd = os.path.dirname(processor_descriptor_file)
    env = os.environ.copy()
    env.update(content_metadata)
    env.update(custom_metadata)
    with open(input_file, mode='rb') as input_file_obj:
        output = subprocess.check_output(command, cwd=cwd, env=env, stdin=input_file_obj, shell=True, timeout=5)
    return output
