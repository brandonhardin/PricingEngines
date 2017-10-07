import numpy as np

class VanillaOption(object):
    def __init__(self, strike, expiry, payoff):
        self.__strike = strike
        self.__expiry = expiry
        self.__payoff = payoff
        
    @property
    def strike(self):
        return self.__strike
    
    @property
    def expiry(self):
        return self.__expiry
    
    def payoff(self, spot):
        return self.__payoff(self, spot)

def call_payoff(option, spot):
    return np.maximum(spot - option.strike, 0.0)

def put_payoff(option, spot):
    return np.maximum(option.strike - spot, 0.0)

spot = 41.0
strike = 40.0
expiry = 1.0
rate = 0.08
volatility = 0.30
dividend = 0.0
steps = 3
nodes = steps + 1

dt = expiry / steps
u = np.exp((rate * dt) + volatility * np.sqrt(dt))
d = np.exp((rate * dt) - volatility * np.sqrt(dt)) 
pu = (np.exp(rate * dt) - d) / (u - d)
pd = 1 - pu
disc = np.exp(-rate * dt)
dpu = disc * pu
dpd = disc * pd

Ct = np.zeros((nodes, ))
St = np.zeros((nodes, ))
option = VanillaOption(strike, expiry, call_payoff)

for i in range(nodes):
    St[i] = spot * (u ** (steps-i)) * (d ** i)
    Ct[i] = option.payoff(St[i])

for i in range((steps - 1), -1, -1):
    for j in range(i+1):
        Ct[j] = dpu * Ct[j] + dpd * Ct[j+1]
        St[j] = St[j] / u
        Ct[j] = np.maximum(Ct[j], option.payoff(St[j]))

price = Ct[0]
print("The Option Price is: ${0:.3f}".format(price))
