import auction_dynamics

class AdUnit:
    def __init__(self,name):
        self.name = name
        self.auction_manager = auction_dynamics.AuctionManager()
    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)
    def return_winner(self):
        return self.auction_manager.top_bid
