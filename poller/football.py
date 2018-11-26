import abc
from plugin import PluginBase
import requests
import logging
import xml.etree.ElementTree as ET
import os

def navigate(node, team):
    if node.tag == "g":
        game = node.attrib
        if game['hnn'] == team:
            return int(game['hs'])
        elif game['vnn'] == team:
            return int(game['vs'])
        else:
            return None
    else:
        for child in node:
            score = navigate(child, team)
            if score is not None:
                return score
        return None

class Football(object):
    __metaclass__ = abc.ABCMeta
    team = None
    score = None
    triggerURL = "https://maker.ifttt.com/trigger/%s/with/key/%s"

    def __init__(self, team):
        self.team = team

    def trigger(self):
        logging.info("Football - %s - Triggered" % self.team)
        if self.team is not None:
            requests.get(self.triggerURL % (self.team, os.environ['IFTTT_KEY']))
            return True
        return False

    def check(self):
        url = "http://www.nfl.com/liveupdate/scorestrip/ss.xml"
        r = requests.get(url)
        root = ET.fromstring(r.text)
        new_score = navigate(root, self.team)
        if self.score is None:
            self.score = new_score
            return False
        elif new_score > self.score:
            self.score = new_score
            return True
        return False