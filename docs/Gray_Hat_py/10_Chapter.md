# Fuzzing Windows Drivers

## IOCTL 
which are special gateways that allow usermode
services or applications to access kernel devices or components. As
with any means of passing information from one application to another, we
can exploit insecure implementations of IOCTL handlers to gain escalated
privileges or completely crash a target system.

on OPENBSD is used by the bio pseudo-device driver and the bioctl utility to implement RAID management in a undefined vendor-agentic interface similar to ifconfig.
