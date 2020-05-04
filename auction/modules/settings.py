import adunit
from format import LogSettings

log = LogSettings()
log.debug_enabled()

class Entity:
    def __init__(self):
        self.collection = []
    def get_valid_entities(self,source,params,class_name):
        for s in source:
            attr = []
            for p in params:
                a = 's[\'' + p + '\']'
                a = eval(a)
                attr.append(a)
            e = class_name(*attr)
            self.collection.append(e)
    def sort_collection(self,key):
        return sorted(self.collection, key=lambda k: k[key])

class Site:
    def __init__(self,domain,bidders,floor):
        self.domain = domain
        self.bidders = bidders
        self.floor = floor
        self.ad_units = []
        self.winning_bids = []
        log.message('Loaded config for ' + self.domain + '. Site floor = ' + str(self.floor))
    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)
    def __getitem__(self,key):
        return getattr(self,key)
    def set_ad_unit(self,name):
        self.ad_units.append(adunit.AdUnit(name))
    def get_winning_bids_above_site_floor(self):
        for ad in self.ad_units:
            top_bid = ad.return_winner()
            if top_bid.adjusted_bid >= self.floor:
                auction_winner = {
                'bidder': top_bid.bidder,
                'bid': top_bid.bid_value,
                'unit': ad.name
                }
                self.winning_bids.append(auction_winner)
            else:
                self.winning_bids.append([])
                log.warning('Adjusted bid (' + str(top_bid.adjusted_bid) + ') is not above the' + self.domain + ' site floor of ' + str(self.floor) + '. No winner for ad unit ' + ad.name)

class Bidder:
    def __init__(self,name,adjustment):
        self.name = name
        self.adjustment = adjustment
        log.message('Loaded bidder settings for ' + self.name)
    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)
    def __getitem__(self,key):
        return getattr(self,key)
