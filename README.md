# python-log-parser

## Introduction:
This is a log parser. It receives text files with three columns separated by a blank space. The first column is a Unix timestamp, the second one is the hostname that opens the connection and the third one the hostname that receives it.

## Configuration:
Fork and/or clone this repo into your computer:

`git clone https://github.com/mariobru/python-log-parser.git` 

Give execution permissions to logparser.py if needed:

`sudo chmod 744 logparser.py`

## How to use it:
This scripts can be run in two modes:

* **Range mode**: Given a filename with its path, an init datetime, end datetime and hostname return a list of hostnames connected to the given host during that period of time. Example:

    `./logparser.py -r -f ./input/input-file-10000.txt -i 1565647204351 -e 1565733598341 -s Natausha`
* **Unlimited hourly mode**: You must input filename with its path, server and client and the script will output hourly a list of hostnames connected to the given server during the last hour, a list of hostnames that received connections from a given client during the last hour and the hostname that generated most connections in the last hour. Example: 

    `./logparser.py -u -f ./input/input-file-10000.txt -s Natausha -c Dristen`                       

* You will find the parsed logs in the **output** folder.
* Run `./logparser.py -h` to read the help information in your terminal:  

```
usage: logparser.py [-h] [-r | -u] [-f FILENAME] [-i INIT] [-e END]
                    [-s SERVER] [-c CLIENT]

This is a log parser. It receives text files with three columns separated by a
blank space. The first column is a Unix timestamp, the second one is the
hostname that opens the connection and the third one the hostname that
receives it. You can run the range mode for a saved log or the hourly mode for
live written log.

optional arguments:
  -h, --help            show this help message and exit
  -r, --range           Enables range mode. Given a filename, an init
                        datetime, end datetime and hostname return a list of
                        hostnames connected to the given host during that
                        period of time.
  -u, --unlimited       Enables unlimited mode. You must input filename,
                        server and client and the script will output hourly a
                        list of hostnames connected to the given server during
                        the last hour, a list of hostnames that received
                        connections from a given client during the last hour,
                        the hostname that generated most connections in the
                        last hour.
  -f FILENAME, --filename FILENAME
                        Input the filename of the log you want to parse with
                        its absolute path.
  -i INIT, --init INIT  Input the init Unix timestamp.
  -e END, --end END     Input the end Unix timestamp.
  -s SERVER, --server SERVER
                        Input the hostname on which you want to know who is
                        connected.
  -c CLIENT, --client CLIENT
                        Input the hostname you want to know where is
                        connected.
```
