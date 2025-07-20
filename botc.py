import re
from typing import no_type_check
import urllib.request as req
from bs4 import BeautifulSoup, Tag


def clean(s: str):
    return re.sub("[-' ]", "", s.lower())


def URLify(s: str):
    return re.sub(" ", "_", s)


def retrieveImageURL(imageLink: str):
    try:
        imageResponse = req.urlopen(imageLink).read().decode('utf-8')
    except Exception:
        print("can't load")
        return ""

    src = re.search('<a href="(/images/.+\\.png)">', imageResponse)
    if src is None:
        print("no link provided")
        return ""
    src = re.search('/images/.+\\.png', src.group())
    if src is None:
        return ""

    return f"https://wiki.bloodontheclocktower.com{src.group()}"


def title(s: str):
    s1: list[str] = s.split(' ')
    s2: list[str] = []
    for i in s1:
        s3: list[str] = []
        for j in i.split('-'):
            s3.append(j.capitalize())
        s2.append('-'.join(s3))
    return ' '.join(s2)


def getDescription(link: str):
    data = ""
    try:
        with req.urlopen(link) as response:
            data = response.read().decode('utf-8')
    except Exception:
        print("WOOWOOWOO - Link doesn't work, check the script")
        return ["", "", ""]

    parsed_html = BeautifulSoup(data, features='lxml')
    summary = parsed_html.find('span', id='Summary')
    if summary is None or summary.parent is None or summary.parent.parent is None or summary.parent.parent.p is None:
        return ["", "", ""]

    returnedValues = []

    for p in summary.parent.parent.find_all('p'):
        returnedValues.append(p.text)
    returnedValues.append("")
    for li in summary.parent.parent.find_all('li'):
        returnedValues[2] += "* " + li.text + "\n"
    returnedValues[2] = returnedValues[2].strip()
    if len(returnedValues) != 3:
        return ["", "", ""]
    return returnedValues


def getJinxes(link: str):
    data = ""
    try:
        with req.urlopen(link) as response:
            data = response.read().decode('utf-8')
    except Exception:
        print("WOOWOOWOO - Link doesn't work, check the script")
        return []

    parsed_html = BeautifulSoup(data, features='lxml')
    summary = parsed_html.find('div', id='jinxes')
    if summary is None or not isinstance(summary,
                                         Tag) or summary.table is None:
        return []

    returnedValues = []

    for row in summary.table.find_all('tr'):
        character = row.find_all('td')[1].find_all('p')[0].text #type: ignore
        jinx = row.find_all('td')[1].find_all('p')[1].text #type: ignore
        returnedValues.append((character, jinx)) #type: ignore

    return returnedValues
