FROM gaiaadm/result-processing:latest-python

ARG http_proxy
ARG https_proxy

# Bundle app source
COPY . /src/processors/jenkins-tests-processor

RUN cd /src/processors/jenkins-tests-processor && pip install -r requirements.txt

# generate pyc cache
RUN python -m compileall /src/processors/jenkins-tests-processor
