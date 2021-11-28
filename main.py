#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import stat
import shutil

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
import requests
import click

path = "/home/stig124/Downloads/"

def get_dl_url():
    """Scrape NVIDIA Website for the download URL for the researched driver
    :return: Scraped driver link and version
    :rtype: str
    """
    with Firefox() as driver:
        driver.get('https://www.nvidia.com/en-us/drivers/unix/')
        l = driver.find_elements(By.CSS_SELECTOR, f"#rightContent > p:nth-child(1) > a:nth-child({branch})")[0].text
        driver.find_element(By.LINK_TEXT, l).click()
        dl_conf = driver.find_element(By.ID, "lnkDwnldBtn").click()
        dl_link = driver.find_elements(By.CSS_SELECTOR, "#mainContent > table:nth-child(3) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > a:nth-child(1)")[0].get_attribute('href')
        return dl_link, l


def download(dl_link, driver_version):
    """Download the actual driver install file
    :param dl_link: Previously scraped download link
    :type dl_link: str
    :param driver_version: Downloaded driver version
    :type driver_version: str
    """
    headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"
    }
    filename = path + "NVIDIA-" + driver_version + ".run"
    with open(filename, 'wb') as f:
        with requests.get(dl_link, headers=headers, stream=True) as r:
            shutil.copyfileobj(r.raw,f)
    os.chmod(filename, 0o755)

if __name__ == '__main__':
    dl_link, driver_version = get_dl_url()
    download(dl_link, driver_version)

