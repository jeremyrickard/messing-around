#!/usr/bin/python

import subprocess, json

with open("repos.txt") as file:
    repos = [line.rstrip() for line in file]
results = open("results.json", "w")
vulnerable = []
for repo in repos:
    fullRepo = "mcr.microsoft.com/"+repo
    print(repo)
    result = subprocess.Popen(['crane', 'ls', fullRepo], bufsize=0, stdout=subprocess.PIPE)
    for line in iter(result.stdout.readline, b''):
        tag = line.decode('utf-8')[:-1]
        #tag = line
        print(tag)
        # /Users/jrrickard/.ratify/ratify
        fullTagAndRepo = fullRepo + ":"+tag
        verifyResult = subprocess.Popen(['/Users/jrickard/.ratify/ratify', 'verify', '--subject', fullTagAndRepo], bufsize=0, stdout=subprocess.PIPE)
        obj = json.load(verifyResult.stdout)
        if obj["isSuccess"] == True:
            for result in obj["verifierReports"]:
                if result["isSuccess"] is False:
                    vulnerable.append(verifyResult)
                else:
                    print("success, skipping")
                    continue
        elif obj["verifierReports"][0]["message"] == "verification failed: no referrers found for this artifact":
            print("skipping because no sbom")
            continue
json.dump(vulnerable, results, indent=4,separators=(',',': '))
results.close()
        
        
