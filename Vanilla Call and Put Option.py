import numpy as np

class VanillaOption(object):
    def __init__(self, strike, expiry):
        self.strike = strike
        self.expiry = expiry
    
    def payoff(self):
        pass


class VanillaCallOption(VanillaOption):
    def __init__(self, strike, expiry):
        super(VanillaCallOption, self).__init__(strike, expiry)
        
    def payoff(self, spot):
        return np.maximum(spot - self.strike, 0.0)


class VanillaPutOption(VanillaOption):
    def __init__(self, strike, expiry):
        super(VanillaPutOption, self).__init__(strike, expiry)
        
    def payoff(self, spot):
        return np.maximum(self.strike - spot, 0.0)
        
the_call = VanillaCallOption(42.0, 1.0)
the_put = VanillaPutOption(38.0, 1.0)
spot1 = 45.0
spot2 = 35.0


print("The Call Payoff when the Spot price is {0:4.4f} is {1:4.4f}".format(spot1, the_call.payoff(spot1)))
print("The Put Payoff when the Spot price is {0:4.4f} is {1:4.4f}".format(spot2, the_put.payoff(spot2)))




