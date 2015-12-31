[![](https://badge.imagelayers.io/gaiaadm/jenkins-tests-processor:latest.svg)](https://imagelayers.io/?images=gaiaadm/jenkins-tests-processor:latest 'Get your own badge on imagelayers.io')

*CircleCI:* [![Circle CI](https://circleci.com/gh/gaia-adm/jenkins-tests-processor.svg?style=svg)](https://circleci.com/gh/gaia-adm/jenkins-tests-processor)

# Jenkins tests data processor

This is Jenkins test results data processor for GAIA analytics. It is based on "gaiaadm/result-processing" Docker image. It processes data format from <a href="http://{jenkins-host}:{port}/job/{jenkins-job}/{job-id}/testReport/api/json">http://{jenkins-host}:{port}/job/{jenkins-job}/{job-id}/testReport/api/json</a>

## Building

Execute:
- docker build -t gaiaadm/jenkins-tests-processor .

## Running

Execute:
- docker run -d -e AMQ_USER="admin" -e AMQ_PASSWORD="mypass" -v "/tmp:/upload" --link rabbitmq:amqserver --link mgs:metricsgw --name jenkins-tests-processor gaiaadm/jenkins-tests-processor

Note that for development it is recommended to mount a local directory containing result processor directory to /src/processors or mount the processor directory into /src/processors/{processorName}

Executing tests:
- nosetests --with-xunit
or
- python -m unittest discover -s tests -v
