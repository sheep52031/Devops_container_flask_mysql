#Dockerfile-ubuntu-22.04
FROM ubuntu:22.04 as base

# Install Python 3 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get install -y mysql-client

# Copy your Flask application and HTML template
COPY ./flask_app /flask_app

# Set the working directory
WORKDIR /flask_app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Ensure scripts are available for use in next command
COPY ./container/root/scripts/* /scripts/
COPY ./container/root/usr/local/bin/* /usr/local/bin/

# - Symlink variant-specific scripts to default location
# - Upgrade base security packages, then clean packaging leftover
# - Add S6 for zombie reaping, boot-time coordination, signal transformation/distribution: @see https://github.com/just-containers/s6-overlay#known-issues-and-workarounds
# - Add goss for local, serverspec-like testing
RUN /bin/bash -e /scripts/ubuntu_apt_config.sh && \
    /bin/bash -e /scripts/ubuntu_apt_cleanmode.sh && \
    ln -s /scripts/clean_ubuntu.sh /clean.sh && \
    ln -s /scripts/security_updates_ubuntu.sh /security_updates.sh && \
    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    /bin/bash -e /security_updates.sh && \
    apt-get install -yqq \
      curl \
      gpg \
      apt-transport-https \
    && \
    /bin/bash -e /scripts/install_s6.sh && \
    /bin/bash -e /scripts/install_goss.sh && \
    apt-get remove --purge -yq \
        curl \
        gpg \
    && \
    /bin/bash -e /clean.sh

# Overlay the root filesystem from this repo
COPY ./container/root /

# Copy the init.sh script and make it executable
COPY ./container/root/run.d/init.sh /etc/cont-init.d/init.sh
RUN chmod +x /etc/cont-init.d/init.sh


### Stage 2 --- collapse layers ###

FROM scratch
COPY --from=base / .

# Use in multi-phase builds, when an init process requests for the container to gracefully exit, so that it may be committed
# Used with alternative CMD (worker.sh), leverages supervisor to maintain long-running processes
ENV SIGNAL_BUILD_STOP=99 \
    S6_BEHAVIOUR_IF_STAGE2_FAILS=2 \
    S6_KILL_FINISH_MAXTIME=5000 \
    S6_KILL_GRACETIME=3000

RUN goss -g goss.base.yaml validate

# NOTE: intentionally NOT using s6 init as the entrypoint
# This would prevent container debugging if any of those service crash
CMD ["/bin/bash", "/run.sh"]
