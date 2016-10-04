# Parental Control Starter Chute

Runs a WiFi access point with content filtering and configurable blocking.

## Files

* Dockerfile: specifies the packages and files to install in the chute.
Modify this file if you add new files or need to install other
dependencies.

* chute/run.sh: is the default entry point when the chute runs.

## Getting Started

1. Fork this project to your own github account.
2. TODO
3. Launch it on your Paradrop router through paradrop.org.

When creating a version of this chute, you should configure it as shown
in the image.  The chute requires configuring a WiFi AP.  Feel free to
modify the ESSID and password settings or leave the defaults.

Additionally, we recommended adding the OpenDNS address, 208.67.222.222, as an
alternative DNS server.  [OpenDNS](https://www.opendns.com/home-internet-security/)
provides another layer of content filtering.

![Create version options](/images/create_version.png)

After installing the chute on your router, if everything is configured
correctly, you should be able to connect a device to the chute's WiFi
AP.
