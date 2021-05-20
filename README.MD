# URL Scanner

This is simple utility that gets a list of urls from a textfile (one url per line), queries each url and returns the web server status code.
Optionally screenshots can be made during this process of the pages being queries (this requires Firefox to be installed).

### Usage
```
usage: urlscanner.py [-h] [--inputfile INPUTFILE] [--outputdir OUTPUTDIR]
                     [--outputfile OUTPUTFILE] [--verbose] [--append APPEND]
                     [--firefoxpath FIREFOXPATH] [--screenshots]
```

#### Options:
```-h``` or ```--help``` - Show command lines options and a brief help description per option.  
```-i``` or ```--inputfile``` - Input text file to read urls from. Basically a text file with one url per line.  
```-d``` or ```--outputdir``` - Directory to store screenshots in. This directory has to exist before it can be specified.  
```-a``` or ```--append``` - Append a string to the urls to be checked (e.g. 'index.html' or '?action=something').  
```-f``` or ```--firefoxpath``` - Location where the firefox executable is found (required when creating screenshots).  
```-s``` or ```--screenshots``` - Create .png screenshots of urls.  
```-v``` or ```--verbose``` - More output while the utility is running.

### Examples:
Let's assume we have a textfile called _urls.txt_ containing the following lines:
```
www.google.com
https://www.reddit.com
http://github.com
```
When no http:// or https:// prefix is specified the script will assume https:// needs to be prepended. When specifically http:// needs to be queried make sure it is specified in the text file.

#### 1. Simple status code query with only console output
Command:  
``` 
$ python3 ./urlscanner.py -i urls.txt 
 ____ _____________.____
|    |   \______   \    |
|    |   /|       _/    |
|    |  / |    |   \    |___ 
|______/  |____|_  /_______ \
  ______ ____ ___\/    ____\/ ____   ___________
 /  ___// ___\\__  \  /    \ /    \_/ __ \_  __ \
 \___ \\  \___ / __ \|   |  \   |  \  ___/|  | \/
/____  >\___  >____  /___|  /___|  /\___  >__|
     \/     \/     \/     \/     \/     \/
URL scanner
Peter Berends - 2021

Reading input file (urls.txt)...
[200][OK] - https://www.google.com
[200][OK] - https://www.reddit.com
[301][Moved Permanently] - http://github.com
Done. Processed 3 URLs (0 failed).
```

#### 2. Output results to CVS file:
```
$ python3 ./urlscanner.py -i urls.txt -o out.txt
 ____ _____________.____
|    |   \______   \    |
|    |   /|       _/    |
|    |  / |    |   \    |___ 
|______/  |____|_  /_______ \
  ______ ____ ___\/    ____\/ ____   ___________
 /  ___// ___\\__  \  /    \ /    \_/ __ \_  __ \
 \___ \\  \___ / __ \|   |  \   |  \  ___/|  | \/
/____  >\___  >____  /___|  /___|  /\___  >__|
     \/     \/     \/     \/     \/     \/
URL scanner
Peter Berends - 2021

Reading input file (urls.txt)...
[200][OK] - https://www.google.com
[200][OK] - https://www.reddit.com
[301][Moved Permanently] - http://github.com
Saving results to out.txt
Done. Processed 3 URLs (0 failed).

$ cat out.txt
200,OK,https://www.google.com
200,OK,https://www.reddit.com
301,Moved Permanently,http://github.com
```

#### 3. Create screenshots in verbose mode
```
$ mkdir shots
$ python3 ./urlscanner.py -i urls.txt -s -f /opt/firefox/firefox -d shots -v
 ____ _____________.____
|    |   \______   \    |
|    |   /|       _/    |
|    |  / |    |   \    |___ 
|______/  |____|_  /_______ \
  ______ ____ ___\/    ____\/ ____   ___________
 /  ___// ___\\__  \  /    \ /    \_/ __ \_  __ \
 \___ \\  \___ / __ \|   |  \   |  \  ___/|  | \/
/____  >\___  >____  /___|  /___|  /\___  >__|
     \/     \/     \/     \/     \/     \/
URL scanner
Peter Berends - 2021

Verbose mode on
Location to firefox given: /opt/firefox/firefox
Taking screenshots (will be stored in 'shots')
Activating Firefox as screenshot driver
Using Firefox location: /opt/firefox/firefox
Reading input file (urls.txt)...
Prepend https:// to line (www.google.com).
Processing: https://www.google.com
Taking screenshot of https://www.google.com
[200][OK] - https://www.google.com
Processing: https://www.reddit.com
Taking screenshot of https://www.reddit.com
[200][OK] - https://www.reddit.com
Processing: http://github.com
Taking screenshot of http://github.com
[301][Moved Permanently] - http://github.com
Done. Processed 3 URLs (0 failed).

$ ls -a shots
.  ..  github.com.png  www.google.com.png  www.reddit.com.png
```
