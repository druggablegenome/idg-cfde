#!/usr/bin/env python3

import requests
import json

RSS_API_BASE_URL = 'https://rss.ccs.miami.edu/rss-api/'
OUTDIR = '../RSS_TEST'
DEBUG = False

def run():
  target_data = get_target_data()
  assert target_data, "Error getting target data: FATAL"
  ct = 0
  pr_ct = 0
  fo_ct = 0
  rtypes = {}
  for td in target_data:
    ct += 1
    if not td['pharosReady']:
      continue
    pr_ct += 1
    if td['resourceType'] in rtypes:
      # for testing, only process one resource of each type
      continue
    if DEBUG:
      print("[DEBUG] Target data item {}: {}".format(ct, td))
    resource_data = get_resource_data(td['id'])
    if not resource_data:
      print("Error getting resource data for {}: Skipping".format(td['id']))
      continue
    if DEBUG:
      print("[DEBUG]  Resource_data:")
    for key,val in resource_data['data'][0].items():
      if DEBUG:
        print("[DEBUG]    {}: {}".format(key, val))
    # Write resource metadata to a file. Files are named <Resource_Type_Test>.json
    ofn = "{}/{}_Test.json".format(OUTDIR, td['resourceType'].replace(' ', '_'))
    print("Writing JSON file {} for resource {}...".format(ofn, td['id']))
    with open(ofn, 'w') as ofh:
      json.dump(resource_data['data'][0], ofh)
      fo_ct += 1
    rtypes[td['resourceType']] = True
  print("Processed {} RSS resources".format(ct))
  print("  Got {} Pharos-ready resources".format(pr_ct))
  print("  Wrote {} output files".format(fo_ct))

def get_target_data():
  url = RSS_API_BASE_URL + 'target'
  jsondata = None
  attempts = 0
  resp = requests.get(url, verify=False)
  if resp.status_code == 200:
    return resp.json()
  else:
    return False

def get_resource_data(idval):
  url = RSS_API_BASE_URL + 'target/id?id=%s'%idval
  jsondata = None
  attempts = 0
  resp = requests.get(url, verify=False)
  if resp.status_code == 200:
    return resp.json()
  else:
    return False


if __name__ == '__main__':
  run()
