#!/usr/bin/env python3.4
import os
import json
import unittest
from tests.test_utils import execute_processor
from testfixtures import compare

def data_file_path(file_name):
    return os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', file_name))


class TestProcessor(unittest.TestCase):
    def test_jenkins_tests1(self):
        custom_metadata = {'BUILD_TIMESTAMP': '1439781362656', 'BUILD_SERVER_URI': 'http://my-jenkins:8080',
                           'JOB_NAME': 'test-executor', 'ROOT_JOB_NAME': 'product-root',
                           'BUILD_URI_PATH': 'jobs/test-executor',
                           'BUILD_RESULT': 'UNSTABLE', 'BUILD_NUMBER': '50', 'ROOT_BUILD_NUMBER': '40',
                           'CUSTOM_TAGS': 'MYTAG1,MYTAG2', 'MYTAG1': 'MYTAG1_VALUE', 'MYTAG2': 'MYTAG2_VALUE'}
        output = execute_processor(data_file_path('jenkins-tests1.json'), custom_metadata=custom_metadata)
        output_json = json.loads(output.decode("utf-8"))
        # print(output.decode("utf-8"))

        # this is what we expect
        with open(data_file_path('result-tests1.json'), "rt") as myfile:
            expected_json = json.load(myfile)

        compare(expected_json, output_json, strict=True)

    def test_yajl2_parser(self):
        # verify that we get the yajl2 parser, not python one
        from processor import get_json_parser
        parser = get_json_parser()
        self.assertIsNotNone(parser)
        self.assertEqual('ijson.backends.yajl2', parser.__name__)

if __name__ == '__main__':
    unittest.main()
