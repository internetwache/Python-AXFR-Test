AXFR-test.py
================
A tool to test if the nameservers of a domain are misconfigured and allow AXFR (dns zone transfers) to anyone.

#Requirements

- Python 3
- ```dnspython``` library

#Usage:

```
$> python axfr-test.py
usage: axfr-test.py [-h] [-i [INPUTFILE]] [-o [OUTPUTFILE]] [-l [LOGFILE]]
                    [-p [PROCESSES]] [-d [DOMAIN]]

Check domains' nameservers for public AXFR

optional arguments:
  -h, --help            show this help message and exit
  -i [INPUTFILE], --inputfile [INPUTFILE]
                        Inputfile to read domains from. Default: stdin
  -o [OUTPUTFILE], --outputfile [OUTPUTFILE]
                        Outputfile to write zonedata to. Default: stdout
  -l [LOGFILE], --logfile [LOGFILE]
                        Logfile to use. Default: stderr
  -p [PROCESSES], --processes [PROCESSES]
                        Processes to use. Default: 20
  -d [DOMAIN], --domain [DOMAIN]
                        Domain to check. Ignored if -i is used.
```

##Check a single domain:

```
$> python axfr-test.py -d DOMAIN
```

##Check multiple domains from a file
```
$> python axfr-test.py -i /tmp/domains.txt
```