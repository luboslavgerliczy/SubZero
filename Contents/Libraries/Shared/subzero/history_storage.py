# coding=utf-8

import datetime

mode_map = {
    "a": "auto",
    "m": "manual",
    "b": "auto-better"
}


class SubtitleHistoryItem(object):
    item_title = None
    section_title = None
    rating_key = None
    provider_name = None
    lang_name = None
    score = None
    time = None
    mode = "a"

    def __init__(self, item_title, rating_key, section_title=None, subtitle=None, mode="a", time=None):
        self.item_title = item_title
        self.section_title = section_title
        self.rating_key = str(rating_key)
        self.provider_name = subtitle.provider_name
        self.lang_name = subtitle.language.name
        self.score = subtitle.score
        self.time = time or datetime.datetime.now()
        self.mode = mode

    @property
    def title(self):
        return u"%s: %s" % (self.section_title, self.item_title)

    @property
    def mode_verbose(self):
        return mode_map.get(self.mode, "Unknown")

    def __repr__(self):
        return unicode(self)

    def __unicode__(self):
        return u"%s (Score: %s)" % (unicode(self.item_title), self.score)

    def __str__(self):
        return str(self.rating_key)

    def __hash__(self):
        return hash((self.rating_key, self.score))

    def __eq__(self, other):
        return (self.rating_key, self.score) == (other.rating_key, other.score)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)


class SubtitleHistory(object):
    size = 100
    history_items = None
    storage = None

    def __init__(self, storage, size=100):
        self.size = size
        self.storage = storage
        self.history_items = storage.LoadObject("subtitle_history") or []

    def add(self, item_title, rating_key, section_title=None, subtitle=None, mode="a", time=None):
        # create copy
        items = self.history_items
        item = SubtitleHistoryItem(item_title, rating_key, section_title=section_title, subtitle=subtitle, mode=mode, time=time)

        # insert item
        items.insert(0, item)

        # clamp item amount
        self.history_items = items[:self.size]

        # store items
        self.storage.SaveObject("subtitle_history", self.history_items)


