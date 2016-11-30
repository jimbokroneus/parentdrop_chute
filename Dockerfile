# Parental Control
#
# Runs a WiFi access point with content filtering and configurable blocking.

# Specify the base image.
FROM paradrop/workshop

# Install dependencies.  You can add additional packages here following the example.
RUN apt-get update && apt-get install -y \
#   <package> \
    iptables \
    privoxy \
    dansguardian

# Install files required by the chute.
#
# ADD <path_inside_repository> <path_inside_container>
#
ADD chute/privoxy_config /etc/privoxy/config
ADD chute/dansguardian.conf /etc/dansguardian/dansguardian.conf
ADD chute/run.sh /usr/local/bin/run.sh
ADD chute/parser /user/local/bin/parser

# This is the command that will be run inside the container.  It can be a bash
# script that runs other commands, a python script, a compiled binary, etc.
CMD ["bash", "/usr/local/bin/run.sh"]
#CMD ["python", "/usr/local/bin/parser/parser.py"]

