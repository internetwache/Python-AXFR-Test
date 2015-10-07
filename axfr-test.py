#!/usr/bin/python
import argparse
import dns.resolver
import dns.query
import dns.zone
import os
import sys

from multiprocessing import Pool

INPUTFILE = sys.stdin
OUTPUTFILE = sys.stdout
LOGFILE = sys.stderr
PROCESSES = 20

def checkaxfr(domain):
  domain = domain.strip()
  try:
    ns_query = dns.resolver.query(domain,'NS')
    for ns in ns_query.rrset:
      nameserver = str(ns)[:-1]
      if nameserver is None or nameserver == "":
        continue

      try:
        axfr = dns.query.xfr(nameserver, domain, lifetime=5)
        try:
          zone = dns.zone.from_xfr(axfr)
          if zone is None:
            continue
          LOGFILE.write("Success: " + domain + " @ " + nameserver + "\n")
          LOGFILE.flush()
          OUTPUTFILE.write("Success: " + domain + " @ " + nameserver + "\n")
          OUTPUTFILE.flush()
          for name, node in zone.nodes.items():
            rdatasets = node.rdatasets
            for rdataset in rdatasets:
              OUTPUTFILE.write(str(name) + " " + str(rdataset) + "\n")
              OUTPUTFILE.flush()
        except Exception as e:
          continue
      except Exception as e:
        continue
  except Exception as e:
    pass
  LOGFILE.write("Finished: " + domain + "\n")
  LOGFILE.flush()

def main():
  global PROCESSES, LOGFILE, OUTPUTFILE, INPUTFILE

  parser = argparse.ArgumentParser(description='Check domains\' nameservers for public AXFR')
  parser.add_argument('-i', '--inputfile', type=str, nargs="?", default=sys.stdin, help='Inputfile to read domains from. Default: stdin')
  parser.add_argument('-o', '--outputfile', type=str, nargs="?", default=sys.stdout, help='Outputfile to write zonedata to. Default: stdout')
  parser.add_argument('-l', '--logfile', type=str, nargs="?", default=sys.stderr, help="Logfile to use. Default: stderr")
  parser.add_argument('-p', '--processes', type=int, nargs="?", default=20, help='Processes to use. Default: 20')
  parser.add_argument('-d', '--domain', type=str, nargs="?", help="Domain to check. Ignored if -i is used.")
  args = parser.parse_args()

  if args.processes <=0:
    print("Number of processes must be greater than zero.")
    sys.exit(1)

  PROCESSES = args.processes

  if not str(type(args.inputfile)) == "<class '_io.TextIOWrapper'>":
    if not os.path.isfile(args.inputfile):
      print("Inputfile does not exist.")
      sys.exit(1)
    domains = open(args.inputfile, "r").readlines()
  else:
    if not args.domain is None:
      domains = [args.domain]
    else:
      domains = args.inputfile.readlines()

  if not str(type(args.outputfile)) == "<class '_io.TextIOWrapper'>":
    try:
      OUTPUTFILE = open(args.outputfile, "w")
    except:
      print("Outputfile cannot be created.")
      sys.exit(1)
  else:
    OUTPUTFILE = args.outputfile

  if not str(type(args.logfile)) == "<class '_io.TextIOWrapper'>":
    try:
      LOGFILE = open(args.logfile, "w")
    except:
      print("Logfile cannot be created.")
      sys.exit(1)
  else:
    LOGFILE = args.logfile


  pool = Pool(processes=PROCESSES)

  pool.map(checkaxfr, domains)

if __name__ == '__main__':
  main()
