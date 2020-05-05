import response
from format import LogSettings

class AuctionManager:
    def __init__(self):
        self.bids = []
        self.top_bid = {}
    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)
    def get_bids(self):
        return self.bids
    def get_top_bid(self):
        top_adjusted_bid_value = 0
        top_bid = []
        participating_bids = self.get_bids()
        for b in participating_bids:
            if b.adjusted_bid > top_adjusted_bid_value:
                top_adjusted_bid_value = b.adjusted_bid
                top_bid = b
        self.top_bid = top_bid
    def store_valid_bid(self,bidder,bid_value):
        self.bids.append(response.Bid(bidder,bid_value))


def hold_auctions(all_possible_auctions):
    auction_output = []
    for site in all_possible_auctions:
        for ad in site.ad_units:
            if DEBUG:
                log.message('Holding auction for ' + ad.name + ' in ' + site.domain)
            ad.auction_manager.get_top_bid()
        site.get_winning_bids_above_site_floor()
        log.announcement('We have winners! - ' + str(site.won_bids))
        auction_output.append(site.won_bids)
    return auction_output
