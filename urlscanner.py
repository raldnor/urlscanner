import argparse
import requests
import re
from http.client import responses
from os import path

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep

urlcount = 0
verbose = 0
failedurls = 0
outstring = ""
firefoxpath = "c:\Program Files\Mozilla Firefox\firefox.exe"
interval = 3

def printbanner():
    banner = " ____ _____________.____\n"\
"|    |   \\______   \\    |\n"\
"|    |   /|       _/    |\n"\
"|    |  / |    |   \\    |___ \n"\
"|______/  |____|_  /_______ \\\n"\
"  ______ ____ ___\\/    ____\\/ ____   ___________\n"\
" /  ___// ___\\\\__  \\  /    \\ /    \\_/ __ \\_  __ \\\n"\
" \\___ \\\\  \\___ / __ \\|   |  \\   |  \\  ___/|  | \\/\n"\
"/____  >\\___  >____  /___|  /___|  /\\___  >__|\n"\
"     \\/     \\/     \\/     \\/     \\/     \\/\n"\
"URL scanner\r\nPeter Berends - 2021\n"
    print(banner)
    
def statuscode(url):
    try:
        response = requests.head(url)
        return response.status_code
    except Exception as err:
        if verbose:
            print("Request failed for %s (%s)." % (url, err))
        return None
        
def formaturl(url):
    if not re.match('(?:http|https)://', url):
        if verbose:
            print("Prepend https:// to line (%s)." % url)
        return 'https://{}'.format(url)
    return url
    
def checkdir(dir):
    return path.exists(dir)
    

printbanner()

parser = argparse.ArgumentParser()
parser.add_argument("--inputfile", "-i", help="specify input file with URLs per line")
parser.add_argument("--outputdir", "-d", help="specify output directory")
parser.add_argument("--outputfile", "-o", help="save results to file (CSV format)")
parser.add_argument("--verbose", "-v", help="verbose mode", action="store_true")
parser.add_argument("--append", "-a", help="append a string to the urls to check")
parser.add_argument("--firefoxpath", "-f", help="location where the executable of Firefox is found")
parser.add_argument("--screenshots", "-s", help="create screenshots of URLs", action="store_true")

args = parser.parse_args()

if not args.inputfile:
    print("No input file specified, got nothing to work with. Bye.")
    exit(1)
    
if args.screenshots == True and not args.outputdir:
    print("No output directory specified for screenshot storage. Bye.")
    exit(1)
    
if args.outputdir and not checkdir(args.outputdir):
    print("Invalid output directory specified. Bye.")
    exit(1)
    
if args.verbose:
    print("Verbose mode on")
    verbose = 1

if args.firefoxpath:
    firefoxpath = args.firefoxpath
    if verbose:
        print("Location to firefox given: %s" % args.firefoxpath)
    
if args.screenshots:
    print("Taking screenshots (will be stored in '%s')" % args.outputdir)
    if verbose:
        print("Activating Firefox as screenshot driver")
        print("Using Firefox location: %s" % firefoxpath)
    try:
        Options = Options()
        Options.headless = True
        browser = webdriver.Firefox(options=Options, firefox_binary=firefoxpath)
    except Exception as err:
        print("Could not activate screenshot driver (%s). Try setting the path to Firefox using the --firefoxpath flag." % err)
        exit(1)

print("Reading input file (%s)..." % args.inputfile)

try:
    inputfile = open(args.inputfile, 'r')
    lines = inputfile.readlines()
except:
    print("ERROR: Input file specified is invalid. Bye.")
    exit(1)

for line in lines:
    line = re.sub(r"[\n\t\s\r]*", "", line)
    line = formaturl(line)
    if args.append:
        line = line + args.append
    urlcount += 1
    if verbose:
        print("Processing: %s" % line)
    result = statuscode(line)
    if verbose:
        print("Taking screenshot of %s" % line)
    try:
        browser.get(line)
        sleep(interval)
        browser.get_screenshot_as_file(args.outputdir + '/' + line[7:] + '.png')
    except Exception as err:
        if verbose:
            print("Could not create screenshot (%s)" % err)
    if result:
        outline = str(result) + "," + responses[result] + "," + line
        outstring += outline + "\n"
        print("[%s][%s] - %s" % (result, responses[result], line))
    else:
        failedurls += 1
    
if args.outputfile:
    print("Saving results to %s" % args.outputfile)
    try:
        outfile = open(args.outputfile, 'w')
        outfile.write(outstring)
        outfile.close()
    except Exception as err:
        print("ERROR: Could not save results (%s)." % err)
    
if args.screenshots:
    browser.quit()
    
print("Done. Processed %i URLs (%i failed)." % (urlcount, failedurls))