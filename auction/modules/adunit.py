import auction_dynamics

class AdUnit:
    def __init__(self,name):
        self.name = name
        self.auction_manager = auction_dynamics.AuctionManager()
