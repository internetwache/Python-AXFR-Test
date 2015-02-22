#!/usr/bin/python
import dns.resolver
import dns.query
import dns.zone
import os

from multiprocessing import Pool

DATAPATH = "zones"

def checkaxfr(domain):
  domain = domain.strip()
  try:
    ns_query = dns.resolver.query(domain,'NS')
    for ns in ns_query.rrset:
      nameserver = str(ns)[:-1]
      if nameserver is None or nameserver == "":
        continue

      if os.path.exists("." + os.sep + DATAPATH + os.sep + domain + "-" + nameserver + ".zone"):
        continue

      try:
        axfr = dns.query.xfr(nameserver, domain, lifetime=5)
        try:
          zone = dns.zone.from_xfr(axfr)
          if zone is None:
            continue
          fHandle = open("." + os.sep + DATAPATH + os.sep + domain + "-" + nameserver + ".zone", "w")
          print("Success: " + domain + " @ " + nameserver)
          for name, node in zone.nodes.items():
            rdatasets = node.rdatasets
            for rdataset in rdatasets:
              fHandle.write(str(name) + " " + str(rdataset) + "\n")
          fHandle.close()
        except Exception as e:
          continue
      except Exception as e:
        continue
  except Exception as e:
    pass
  print("Finished: " + domain)

def main():
  pool = Pool(processes=20)
  lines = open("domains.txt", "r").readlines()
  pool.map(checkaxfr, lines)
if __name__ == '__main__':
  main()
