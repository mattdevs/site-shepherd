#!/usr/bin/python
import os
import logging
import requests

from datetime import datetime
from requests import ConnectionError
from selenium import webdriver
from apscheduler.scheduler import Scheduler
from apscheduler.scheduler import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

SITES_FILE = "sites.txt"
LOG_FILE = "shepherd.log"
SCREENSHOT_DIR = "screenshots"

def takeScreenshot(driver, siteURL):
	""" Take a screenshot of the specified site and store it. """
	logging.info("Taking a screenshot of %s" % siteURL)
	siteDir = siteURL.replace("http://", "")
	driver.get(siteURL)
	if not os.path.exists("%s/%s" % (SCREENSHOT_DIR, siteDir)):
		logging.info("Screenshot directory did not exist, creating %s" % siteURL)
		os.makedirs("%s/%s" % (SCREENSHOT_DIR, siteDir))
	if not driver.save_screenshot("%s/%s/%s.png" % (SCREENSHOT_DIR, siteDir, datetime.now().strftime("%Y-%m-%d %H.%M.%S"))):
		logging.info("Unable to take screenshot for %s" % siteURL)
		raise Exception("Unable to take screenshot for %s" % siteURL)

def verifySiteIsOnline(siteURL):
	""" Issue an HTTP request to the specified url and verify that it succeeds. """
	logging.info("Verifying that %s is online." % siteURL)
	try:
		result = requests.get(siteURL)
	except ConnectionError as conErr:
		logging.warning("Unable to reach %s: %s" % (siteURL, conErr))
		raise Exception("Unable to reach %s" % siteURL)
	if result.status_code != 200:
		logging.warning("Unable to reach %s, response code: %s" % (siteURL, result.status_code))
		raise Exception("Unable to reach %s" % siteURL)
	logging.info("Site %s is online." % siteURL)

def setupSelenium():
	""" Set up and return selenium web driver. """
	driver = webdriver.Chrome()
	logging.info("Initialized web driver %s" % driver.name)
	return driver

def unpackSites():
	""" Unpack all sites defined in the site list. """
	logging.info("Unpacking site list from %s" % SITES_FILE)
	siteList = []
	with open(SITES_FILE, 'r') as sitesFile:
		for siteEntry in sitesFile.readlines():
			siteList.append(siteEntry.replace('\n', ''))
	logging.info("Sites retrieved from file: %s" % siteList)
	return siteList

def setupLogging():
	""" Set up a basic logger that will log to a file and stdout. """
	logging.basicConfig(filename=LOG_FILE, format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
	logging.getLogger().addHandler(logging.StreamHandler())
	logging.info("Finished log setup.")

def visitAndVerifySites():
	""" Visit all sites and verify their status. """
	siteList = unpackSites()
	driver = setupSelenium()
	try:
		for site in siteList:
			verifySiteIsOnline(site)
			takeScreenshot(driver, site)
	finally:
		logging.info("Closing all browser windows and shutting down.")
		driver.quit()

def eventListener(event):
	""" Listener that can be attached to scheduler to monitor event execution. """
	if event.exception:
		logging.warning("Encountered exception during event processesing: %s" % event.exception)

if __name__ == "__main__":
	setupLogging()
	logging.info("Initializing scheduler.")
	sched = Scheduler(daemon=True, max_runs=1)
	sched.start()
	logging.info("Adding shepherd function to scheduler to run once per hour.")
	sched.add_listener(eventListener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
	sched.add_interval_job(visitAndVerifySites, minutes=5)
	while True:
		pass


	
		

