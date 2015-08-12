CircleCI build status: [![Circle CI](https://circleci.com/gh/gaia-adm/jenkins-tests-processor.svg?style=svg)](https://circleci.com/gh/gaia-adm/jenkins-tests-processor)

# Jenkins tests data processor

This is Jenkins test results data processor for GAIA analytics. It is based on "gaiaadm/result-processing" Docker image. It adds Python 3.4 and this data processor. It processes data format from <a href="http://{jenkins-host}:{port}/job/{jenkins-job}/{job-id}/testReport/api/json">http://{jenkins-host}:{port}/job/{jenkins-job}/{job-id}/testReport/api/json</a>

## Building

Execute:
- docker build -t gaiaadm/jenkins-tests-processor .

## Running

Execute:
- docker run -d -e AMQ_USER="admin" -e AMQ_PASSWORD="mypass" -v "/tmp:/upload" --link rabbitmq:amqserver --link mgs:metricsgw --name jenkins-tests-processor gaiaadm/jenkins-tests-processor

Note that for development it is recommended to mount a local directory containing result processor directory to /src/processors or mount the processor directory into /src/processors/{processorName}