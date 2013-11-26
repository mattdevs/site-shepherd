#!/usr/bin/python
__author__ = 'mattdevs'

import logging

SITES_FILE = "sites.txt"

def setupLogging(logFileName):
    """ Set up a basic logger that will log to a file and stdout. """
    logging.basicConfig(filename=logFileName, format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.info("Logger initialized.")

def unpackSites():
    """ Unpack all sites defined in the site list. """
    logging.info("Unpacking site list from %s" % SITES_FILE)
    siteList = []
    with open(SITES_FILE, 'r') as sitesFile:
        for siteEntry in sitesFile.readlines():
            siteList.append(siteEntry.replace('\n', ''))
    logging.info("Sites retrieved from file: %s" % siteList)
    return siteList

