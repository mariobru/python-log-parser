#!/usr/bin/env python3 
import pandas as pd
import schedule
import time
import argparse

def recibeConfig():
    parser = argparse.ArgumentParser(description='This is a log parser. It receives text files with three columns separated by a blank space. The first column is a Unix timestamp, the second one is the hostname that opens the connection and the third one the hostname that receives it. You can run the range mode for a saved log or the hourly mode for live written log.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--range', action='store_true', help='Enables range mode. Given a filename with its path, an init datetime, end datetime and hostname return a list of hostnames connected to the given host during that period of time.')
    group.add_argument('-u', '--unlimited', action='store_true', help='Enables unlimited mode. You must input filename with its path, server and client and the script will output hourly a list of hostnames connected to the given server during the last hour, a list of hostnames that received connections from a given client during the last hour, the hostname that generated most connections in the last hour.')
    parser.add_argument('-f', '--filename', help='Input the filename of the log you want to parse with its absolute path.')
    parser.add_argument('-i', '--init', type=int, help='Input the init Unix timestamp.')
    parser.add_argument('-e', '--end', type=int, help='Input the end Unix timestamp.')
    parser.add_argument('-s', '--server', help='Input the hostname on which you want to know who is connected.')
    parser.add_argument('-c', '--client', help='Input the hostname you want to know where is connected.')
    args = parser.parse_args()
    return args

def rangeParser(path,init,end,hostname):
    # Load log file into a dataframe
    df = pd.read_csv('{}'.format(path), sep=' ', header=None, names=['timestamp', 'host_a', 'host_b'])
    # Select the time range we want to parse
    df_range = df[(df['timestamp'] >= init) & (df['timestamp'] <= end)]
    # Select rows with connections to the host in the time range
    df_output = df_range.loc[df_range['host_b'] == '{}'.format(hostname)]
    # Save it into a text file
    df_output.to_csv(r'./output/range_conn_to_{}_{}_{}.txt'.format(hostname,init,end), header=None, index=None, sep=' ')
    print('Check out the output folder.')

def hourParser(path,hostb,hosta):
    # Load log file into a dataframe
    df = pd.read_csv('{}'.format(path), sep=' ', header=None, names=['timestamp', 'host_a', 'host_b'])
    # Time range, in this case last hour
    last = int(time.time())
    first = last - 3600
    # Select the time range we want to parse
    df_range = df[(df['timestamp'] >= first) & (df['timestamp'] <= last)]  #Test: df_range = df[(df['timestamp'] >= 1565647204351) & (df['timestamp'] <= 1565733598341)]
    # Saving a list of hostnames connected to the given host during the last hour into a text file
    connected = df_range.loc[df_range['host_b'] == '{}'.format(hostb)]
    connected.to_csv(r'./output/connections_to_{}_{}_{}.txt'.format(hostb,first,last), header=None, index=None, sep=' ')
    # Saving a list of hostnames received connection from given host during last hour into a text file
    received = df_range.loc[df_range['host_a'] == '{}'.format(hosta)]
    received.to_csv(r'./output/connections_from_{}_{}_{}.txt'.format(hosta,first,last), header=None, index=None, sep=' ')
    # Saving the hostname that generated most connections in the last hour into a text file
    hostcount = df_range.groupby(['host_a']).count()
    max_connections = hostcount.sort_values(['timestamp'], ascending=[False])['timestamp'].head(1)
    max_connections.to_csv(r'./output/max_connections_{}_{}.txt'.format(first,last), header=False, sep=' ')
    print('Check out the output folder.')

def main():
    config = recibeConfig()
    if config.range:
        rangeParser(config.filename,config.init,config.end,config.server)
    elif config.unlimited:
        try:
            schedule.every(1).hour.do(lambda: hourParser(config.filename,config.server,config.client))
            #schedule.every(1).minutes.do(lambda: hourParser(config.filename,config.server,config.client))

            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n Script stopped.")

if __name__=='__main__':
    main()

