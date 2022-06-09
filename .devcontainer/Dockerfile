ARG VARIANT="20.04"
FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-${VARIANT}

# Install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        python3-pip \
        python3-dev \
        python3-distro-info=0.23ubuntu1 \
        libpq-dev \
        unattended-upgrades \
        libcairo2-dev \
        libgirepository1.0-dev \
        build-essential \
        tig

# Install python libraries
COPY requirements-dbr-10.4.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements-dbr-10.4.txt \
   && rm -rf /tmp/pip-tmp

# Install tools to be used by the VSCode python extensions
RUN pip3 --disable-pip-version-check --no-cache-dir install --force-reinstall \
    autopep8 bandit black yapf flake8 mypy pydocstyle pylint

# Install Java 8
RUN sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0xB1998361219BD9C9 \
   && curl -O https://cdn.azul.com/zulu/bin/zulu-repo_1.0.0-3_all.deb \
   && sudo apt-get install ./zulu-repo_1.0.0-3_all.deb \
   && sudo apt-get update \
   && export DEBIAN_FRONTEND=noninteractive \
   && apt-get -y install --no-install-recommends zulu8-jdk \
   && rm ./zulu-repo_1.0.0-3_all.deb

# Install Databricks tools
RUN pip3 --disable-pip-version-check --no-cache-dir install databricks-cli git+https://git@github.com/databrickslabs/dbx@8b1415be8110fcb41c0e80a52c3f8d512bb98621

ARG TARGETARCH

# Install Terraform
RUN cd /tmp \
   && wget https://releases.hashicorp.com/terraform/1.1.9/terraform_1.1.9_linux_${TARGETARCH}.zip \
   && unzip terraform*.zip \
   && mv ./terraform /usr/local/bin/terraform \
   && rm terraform*.zip

# Make python3 the default and update pip
RUN ln -s /usr/bin/python3 /usr/bin/python && /usr/bin/python3 -m pip install --upgrade pip

# ADD extension
COPY .devcontainer/databricks-notebook-0.0.1.vsix /tmp/