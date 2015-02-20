AXFR-test.py
================
A tool to test if the nameservers of a domain are misconfigured and allow AXFR (dns zone transfers) to anyone.

#Requirements

- Python 3
- ```dnspython``` library

#Usage:

- Clone this repository
- Create a file called ```domains.txt``` containing the domains which should be tested
- Run ```python3 axfr-text.py```
- Vulnerable nameservers/domains will be saved to ```./zones/[DOMAIN]-[NS].zone```
