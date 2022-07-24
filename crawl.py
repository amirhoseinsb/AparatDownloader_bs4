import re
import time

import requests

from abc import ABC, abstractmethod

from config import BASE_PATH
from exceptions import QualityError


class Crawl(ABC):

    @abstractmethod
    def get_request(self, url, stream=False):
        pass


class LinkCrawl(Crawl):

    def __init__(self, url):
        self.url = url
        self.content = self.get_request(self.url)

    def get_request(self, url, stream=False):
        """
        Send get request and store data in self.content
        :param url:
        :param stream:
        :return:
        """
        uid = url.split("/")[-1]
        path = BASE_PATH + uid
        try:
            response = requests.get(path)
        except requests.exceptions.ConnectionError:
            print("Connection Error.")
            print("The request will be automatically resubmitted.")
            print("Wait a few moments...")
            time.sleep(3)
            self.get_request(url)
        else:
            json_content = response.json()
            return json_content.get("data")

    def get_all_links(self):
        """
        Parse self.content and store link in a list
        :return:
        """
        links = []

        fetch_all_links = self.content["attributes"]["file_link_all"]
        for link in fetch_all_links:
            url = link["urls"][0]
            links.append(url)

        return links

    def get_all_qualities(self):
        """
        Parse self.content and store qualities in a list
        :return:
        """
        qualities = []

        fetch_all_links = self.content["attributes"]["file_link_all"]
        for link in fetch_all_links:
            quality = re.findall(pattern=r"\d+", string=link["text"])[0]
            qualities.append(quality)

        return qualities

    def match_quality_and_link(self):
        """
        Match links and qualities in a dict
        example: {"480": "sample-link", ...}
        :return:
        """
        match = {}

        links = self.get_all_links()
        qualities = self.get_all_qualities()

        for quality, link in zip(qualities, links):
            match.setdefault(quality, link)

        return match

    def get_link(self, quality):
        """
        Return specific link
        :return:
        """
        match = self.match_quality_and_link()

        if quality not in match.keys():
            available_qualities = list(match.keys())
            raise QualityError(
                f'Sorry, this quality is not available\nAvailable qualities are {available_qualities}'
            )
        return match.get(quality)
