# Parental Control Starter Chute

Runs a WiFi access point with content filtering and configurable blocking.

## Files

* Dockerfile: specifies the packages and files to install in the chute.
Modify this file if you add new files or need to install other
dependencies.

* chute/run.sh: is the default entry point when the chute runs.

## Getting Started

1. Fork this project to your own github account.
2. The chute is already configured for filtering web content that is
inappropriate for children.  Imagine additional functionality that would
be useful for a parental control access point.  Try implementing one of
these or an idea of your own:
  * Disable Internet access during certain hours.
  * Block access to certain websites (e.g. facebook.com) during certain hours.
You may find [iptables](http://manpages.ubuntu.com/manpages/trusty/man8/iptables.8.html)
useful for this task.
3. Launch it on your Paradrop router through paradrop.org.

When creating a version of this chute, you should configure it as shown
in the image.  The chute's functionality requires enabling a WiFi AP.
Feel free to modify the ESSID and password settings or leave the defaults.

Additionally, we recommended adding the OpenDNS address, 208.67.222.222, as a
custom DNS server.  [OpenDNS](https://www.opendns.com/home-internet-security/)
provides another layer of content filtering based on domain name resolution.

![Create version options](/images/create_version.png)

After installing the chute on your router, if everything is configured
correctly, you should be able to connect a device to the chute's WiFi AP.
Trying to navigate to a website such as "http://proxy-bypass.com" while
connected to the Parental Control AP will be rejected by DansGuardian.
The Parental Control chute will also filter adult, dangerous, and unlawful
content, but please do not test that during the workshop.
