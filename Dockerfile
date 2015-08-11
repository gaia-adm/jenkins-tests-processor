FROM gaiaadm/result-processing

# Bundle app source
COPY . /src/processors/jenkins-tests-processor

# http://bugs.python.org/issue19846
ENV LANG C.UTF-8

# upgrade as needed
ENV PYTHON_VERSION 3.4.0-0ubuntu2
ENV PYTHON_PIP_VERSION 1.5.4-1ubuntu3

# setup.sh script is temporary workaround until Docker adds support for passing ENV variables
# to docker build command to allow setting up proxy
ADD setup.sh /tmp/setup.sh
RUN chmod +x /tmp/setup.sh
RUN /tmp/setup.sh

# generate pyc cache
RUN python -m compileall /src/processors/jenkins-tests-processor
