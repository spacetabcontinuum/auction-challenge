import adunit
from format import PrintLog as log

class Site:
    def __init__(self,domain,bidders,floor):
        self.domain = domain
        self.bidders = bidders
        self.floor = floor
        self.ad_units = []
        self.won_bids = []
    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)
    def __getitem__(self,key):
        return getattr(self,key)
    def set_ad_unit(self,name):
        self.ad_units.append(adunit.AdUnit(name))
    def get_winning_bids_above_site_floor(self):
        for a in self.ad_units:
            top_bid = a.return_winner()
            if top_bid.adjusted_bid >= self.floor:
                auction_winner = {
                'bidder': top_bid.bidder,
                'bid': top_bid.bid_value,
                'unit': a.name
                }
                self.won_bids.append(auction_winner)
            else:
                self.won_bids.append([])
                log.warning('Adjusted bid (' + str(top_bid.adjusted_bid) + ') is not above the' + self.domain + ' site floor of ' + str(self.floor) + '. No winner for ad unit ' + a.name)

class Bidder:
    def __init__(self,name,adjustment):
        self.name = name
        self.adjustment = adjustment
    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)
    def __getitem__(self,key):
        return getattr(self,key)