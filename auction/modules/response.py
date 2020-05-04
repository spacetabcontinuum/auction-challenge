class Bid:
    def __init__(self,bidder,bid_value,adjustment_factor):
        self.bidder = bidder
        self.bid_value = bid_value
        self.adjustment_factor = adjustment_factor
        self.adjusted_bid = bid_value * (1.0000 + adjustment_factor)
    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)
