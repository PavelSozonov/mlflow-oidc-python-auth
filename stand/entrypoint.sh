#!/bin/bash

# Start tcpdump in the background with a file size limit of 200 MB
tcpdump -i eth0 -w /tmp/capture.pcap -U -C 200 &

# Run the original command
exec sleep infinity
