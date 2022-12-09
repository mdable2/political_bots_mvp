from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

import pickle
from urllib.parse import urljoin
import common.logging as logging
import time
import datetime
from datetime import timedelta
from typing import List, Set

class TranscriptObject():
    keywords: Set[str]
    text: str
    speaker: str

    def __init__(self, keywords, text, speaker) -> None:
        self.keywords = keywords
        self.text = text
        self.speaker = speaker

    def __repr__(self) -> str:
        return f"TranscriptObject()\nkeywords: {self.keywords}\nspeaker: {self.speaker}\ntext: {self.text}\n"
    
    def __str__(self) -> str:
        return f"keywords: {self.keywords}\nspeaker: {self.speaker}\ntext: {self.text}\n"

class TranscriptPage():
    title: str
    keywords: Set[str]
    speakers: Set[str]
    transcript_objects: List[TranscriptObject]

    def __init__(self, title, keywords, speakers, transcript_objects) -> None:
        self.title = title
        self.keywords = keywords
        self.speakers = speakers
        self.transcript_objects = transcript_objects
    
    def __repr__(self) -> str:
        return f"TranscriptPage()\ntitle: {self.title}\nkeywords: {self.keywords}\nspeakers: {self.speakers}\ntranscript_objects: {self.transcript_objects}\n"
    
    def __str__(self) -> str:
        return f"title: {self.title}\nkeywords: {self.keywords}\nspeakers: {self.speakers}\ntranscript_objects: {self.transcript_objects}\n"     


if __name__ == "__main__":
    try:
        time.sleep(5)

        options = Options()
        options.headless = True
        options.add_argument("window-size=1200x600")
        scroll_pause_time = 5

        driver = webdriver.Remote(
            "http://selenium-chrome:4444/wd/hub", options=options)

        screen_height = driver.execute_script("return window.screen.height;")
        i = 1
        df = pd.read_csv("/app/common/biden_urls.csv")
        list_of_urls = list(df["0"])
        transcript_pages = []

        for url in list_of_urls:
            try:
                kws = set()
                speakers = set()
                logging.log(f"At url: {url}")
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                title = soup.find("h1", {"class": "topic-page-header transcript-header"}).text
                results_block = soup.find('div', id="resultsblock")
                if not results_block:
                    logging.log(f"Skipping {url}")
                    continue
                transcript_objects = []
                for result in results_block.find_all("div", {"class": "media topic-media-row mediahover"}):
                    speaker = result.find("div", {"class": "speaker-label"}).text
                    text = result.find("div", {"class": "transcript-text-block"}).text
                    keywords = []
                    for kw in result.find_all("div", {"class": "tag-keyword keyword-tooltip"}):
                        keywords.append(kw.text.strip())
                    for kw in result.find_all("div", {"class": "tag-entity entity-tooltip"}):
                        keywords.append(kw.text.strip())
                    for kw in result.find_all("div", {"class": "tag-people people-tooltip"}):
                        keywords.append(kw.text.strip())
                    for kw in keywords:
                        kws.add(kw)
                    speakers.add(speaker)

                    transcript_object = TranscriptObject(set(keywords), text, speaker)
                    transcript_objects.append(transcript_object)
                transcript_pages.append(TranscriptPage(title, kws, speakers, transcript_objects))
            except Exception as e:
                logging.error(e)
                continue
        pickle.dump(transcript_pages, open("/app/common/biden_transcripts.pkl", "wb"))
        logging.log("All done!")
    except Exception as e:
        logging.error(e)
