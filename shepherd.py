#!/usr/bin/python
__author__ = 'mattdevs'
import os
import logging
import threading
from datetime import datetime

import requests
from requests import ConnectionError
from selenium import webdriver
from apscheduler.scheduler import Scheduler, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import shepherd_util


LOG_FILE = "shepherd.out"
SCREENSHOT_DIR = "screenshots"
SCREENSHOT_INTERVAL_MINS = 1


class Shepherd:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def takeScreenshot(self, siteURL):
        """ Take a screenshot of the specified site and store it. """
        logging.info("Taking a screenshot of %s" % siteURL)
        siteDir = siteURL.replace("http://", "")
        self.driver.get(siteURL)
        if not os.path.exists("%s/%s" % (SCREENSHOT_DIR, siteDir)):
            logging.info("Screenshot directory did not exist, creating %s" % siteURL)
            os.makedirs("%s/%s" % (SCREENSHOT_DIR, siteDir))
        if not self.driver.save_screenshot(
                        "%s/%s/%s.png" % (SCREENSHOT_DIR, siteDir, datetime.now().strftime("%Y-%m-%d %H.%M.%S"))):
            logging.error("Unable to take screenshot for %s" % siteURL)

    def verifySiteIsOnline(self, siteURL):
        """ Issue an HTTP request to the specified url and verify that it succeeds. """
        logging.info("Verifying that %s is online." % siteURL)
        try:
            result = requests.get(siteURL)
        except ConnectionError as conErr:
            logging.exception("Unable to reach %s: %s" % (siteURL, conErr))
            raise
        if result.status_code != 200:
            logging.error("Unable to reach %s, response code: %s" % (siteURL, result.status_code))
        logging.info("Site %s is online." % siteURL)

    def visitAndVerifySites(self):
        """ Visit all sites and verify their status. """
        siteList = shepherd_util.unpackSites()
        try:
            for site in siteList:
                self.verifySiteIsOnline(site)
                self.takeScreenshot(site)
        finally:
            logging.info("Closing all browser windows and shutting down.")
            self.driver.quit()

    def eventListener(self, event):
        """ Listener that can be attached to scheduler to monitor event execution. """
        if event.exception:
            logging.warning("Encountered exception during event processing: %s" % event.exception)


if __name__ == "__main__":
    shepherd_util.setupLogging(LOG_FILE)
    logging.info("Initializing scheduler.")
    sched = Scheduler(daemon=True)
    sched.start()
    shepherd = Shepherd()
    logging.info("Adding shepherd function to scheduler to run once per hour.")
    sched.add_listener(shepherd.eventListener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    sched.add_interval_job(shepherd.visitAndVerifySites, minutes=SCREENSHOT_INTERVAL_MINS)
    while True:
        pass
