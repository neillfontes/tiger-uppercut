#!/usr/bin/python
# -*- coding: utf-8 -*-

from webdriver_wrapper import WebDriverWrapper

wd = WebDriverWrapper()
wd.get_facebook()
wd.go_to_page()

# db.get_last_commented

wd.scan_posts()

wd.expand_older_posts()

wd.quit_driver()
