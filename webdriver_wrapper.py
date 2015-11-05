#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import pickle
import os.path
import sys

from configparser import PropertyReader

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class WebDriverWrapper:

    driver = None

    fb_user = None
    fb_password = None

    posts = []

    page_address = "https://www.facebook.com/Globoesportecom/"

    fb_login_email = "//input[@id='email']"
    fb_login_password = "//input[@id='pass']"
    fb_login_button = "//label[@id='loginbutton']/input"
    fb_logged_in = "//a[contains(@href, \"https://www.facebook.com/?ref=logo\")]"

    fb_common_post_div = "//div[@class = \"_1dwg\"]"
    fb_common_post_div_url = ""

    def __init__(self):

        self.setup_logger()
        self.read_config()

        logging.info('Hello, let\'s reveal some Facebook posts for the world to see...')
        self.driver = webdriver.Firefox()

    def get_facebook(self):

        logging.info('Trying to load Facebook cookies')

        logged_in = False

        if os.path.lexists("./cookies/cookies.pkl"):
            logging.info('Cookies exist, trying to add to session')
            self.driver.get("http://www.facebook.com")
            cookies = pickle.load(open("./cookies/cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            logging.info('Cookies added to the Driver, refreshing')
            self.driver.get("http://www.facebook.com")

            login_success = self.driver.find_element(By.XPATH, self.fb_logged_in)
            if login_success is not None:
                logging.info('Logged in')
                logged_in = True

        else:
            self.logger.warning('Cookies do not exist. Damn. Manual login')
            self.driver.get("http://www.facebook.com")
            logging.info('Typing user')
            self.driver.find_element(By.XPATH, self.fb_login_email).send_keys(self.fb_user)
            logging.info('Typing password')
            self.driver.find_element(By.XPATH, self.fb_login_password).send_keys(self.fb_password)
            logging.info('Submitting')
            self.driver.find_element(By.XPATH, self.fb_login_button).click()

            login_success = self.driver.find_element(By.XPATH, self.fb_logged_in)
            if login_success is not None:
                logging.info('Logged in')
                if os.path.lexists("./cookies/cookies.pkl"):
                    logging.info('Deleting existing Cookie file')
                    os.remove("./cookies/cookies.pkl")
                logging.info('Dumping new Cookie file')
                pickle.dump(self.driver.get_cookies(), open("./cookies/cookies.pkl", "wb"))
                logged_in = True

        if not logged_in:
            sys.exit('Issues with logging in, aborting...')

    def go_to_page(self):
        logging.info('Loading target page')
        self.driver.get(self.page_address)
        logging.info('Loaded target page')

    def scan_posts(self, up_to_post = None):
        # Otherwise we will scan forever
        scan_post_limit = 10

        self.fb_common_post_div


    # def get_post_urls(self):


    # This is just to get more posts in the feed in case it doesn't run
    # or multiple posts are done in a short . It is an ugly solution for
    # now.
    # def expand_older_posts(self):
    #     body = self.driver.find_element(By.XPATH, '//body')
    #     body.send_keys(Keys.END)
    #     time.sleep(2)

    def quit_driver(self):
        self.driver.quit()

    def setup_logger(self):
        logging.basicConfig(level=logging.DEBUG, filename='pastepost.log', format='%(asctime)s %(message)s')
        logging.getLogger().addHandler(logging.StreamHandler())
        logging.info("Setting up logger")

    def read_config(self):
        logging.info("Reading configuration")
        if os.path.lexists("./cfg/config.properties"):
            logging.debug("Configuration file exists")
            props = PropertyReader.read_properties_file('./cfg/config.properties')
            self.fb_login_email = props['email']
            self.fb_login_password = props['password']
            logging.debug("Email={0}, Password={1}".format(self.fb_login_email, self.fb_login_password))
        else:
            sys.exit("Configuration file does not exist. Please create it under cfg/config.properties. Aborting...")



