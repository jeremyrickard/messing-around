#!/usr/bin/python

import subprocess, json

with open("repos.txt") as file:
    repos = [line.rstrip() for line in file]

for repo in repos:
    fullRepo = "mcr.microsoft.com/"+repo
    print(repo)
    result = subprocess.Popen(['crane', 'ls', fullRepo], bufsize=0, stdout=subprocess.PIPE)
    #result = subprocess.run(['crane', 'ls', fullRepo],stdout=subprocess.PIPE)
    #tags = result.stdout.readline
    #for lint in iter(result.stdout.readline):
    results = open("results.txt", "w")
    
    for line in iter(result.stdout.readline, b''):
        tag = line.decode('utf-8')[:-1]
        #tag = line
        print(tag)
        # /Users/jrrickard/.ratify/ratify
        fullTagAndRepo = fullRepo + ":"+tag
        verifyResult = subprocess.Popen(['/Users/jrrickard/.ratify/ratify', 'verify', '--subject', fullTagAndRepo], bufsize=0, stdout=subprocess.PIPE)
        obj = json.load(verifyResult.stdout)
        if obj["isSuccess"] == True:
            print("success, skipping")
            continue
        for result_line in iter(verifyResult.stdout.readline, b''):
            l = result_line.decode('utf-8')[:-1]
            results.write(l)
    results.close()
        
        
