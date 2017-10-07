import abc
import numpy as np
from scipy.stats import binom

class Option(object, metaclass=abc.ABCMeta):
    """An option.

    The doc string.
    """

    @property
    @abc.abstractmethod
    def expiry(self):
        """Get the expiry date."""
        pass

    @expiry.setter
    @abc.abstractmethod
    def expiry(self, newExpiry):
        """Set the expiry date."""
        pass
    
    @abc.abstractmethod
    def payoff(self):
        """Get the option's payoff value."""
        pass


class VanillaOption(Option):
    def __init__(self, expiry, strike, payoff):
        self.__expiry = expiry
        self.__strike = strike
        self.__payoff = payoff
        
    @property
    def expiry(self):
        return self.__expiry

    @expiry.setter
    def expiry(self, new_expiry):
        self.__expiry = new_expiry
    
    @property 
    def strike(self):
        return self.__strike
    
    @strike.setter
    def strike(self, new_strike):
        self.__strike = new_strike

    def payoff(self, spot):
        return self.__payoff(self, spot)

    
def call_payoff(option, spot):
    return np.maximum(spot - option.strike, 0.0)

def put_payoff(option, spot):
    return np.maximum(option.strike - spot, 0.0)


class PricingEngine(object, metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def calculate(self):
        """A method to implement a pricing model.

           The pricing method may be either an analytic model (i.e.
           Black-Scholes), a PDF solver such as the finite difference method,
           or a Monte Carlo pricing algorithm.
        """
        pass
        
class BinomialPricingEngine(PricingEngine):
    def __init__(self, steps, pricer):
        self.__steps = steps
        self.__pricer = pricer

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, new_steps):
        self.__steps = new_steps
    
    def calculate(self, option, data):
        return self.__pricer(self, option, data)

    
def EuropeanBinomialPricer(pricing_engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    steps = pricing_engine.steps
    nodes = steps + 1
    dt = expiry / steps 
    u = np.exp((rate * dt) + volatility * np.sqrt(dt)) 
    d = np.exp((rate * dt) - volatility * np.sqrt(dt))
    pu = (np.exp(rate * dt) - d) / (u - d)
    pd = 1 - pu
    disc = np.exp(-rate * expiry)
    spotT = 0.0
    payoffT = 0.0
    
    for i in range(nodes):
        spotT = spot * (u ** (steps - i)) * (d ** (i))
        payoffT += option.payoff(spotT)  * binom.pmf(steps - i, steps, pu)  
    price = disc * payoffT 
     
    return price 
   
def AmericanBinomialPricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    spot, rate, volatility, dividend = data.get_data()
    steps = engine.steps
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

    for i in range(nodes):
        St[i] = spot * (u ** (steps-i)) * (d ** i)
        Ct[i] = option.payoff(St[i])

    for i in range((steps - 1), -1, -1):
        for j in range(i+1):
            Ct[j] = dpu * Ct[j] + dpd * Ct[j+1]
            St[j] = St[j] / u
            Ct[j] = np.maximum(Ct[j], option.payoff(St[j]))

    price = Ct[0]
    return(price)


class MarketData(object):
    """A class to encapsulate market data variables.

       Especially to be passed to pricing engines.
    """

    def __init__(self, rate, spot, volatility, dividend):
        self.__rate = rate
        self.__spot = spot
        self.__volatility = volatility
        self.__dividend = dividend

    @property
    def rate(self):
        return self.__rate

    @rate.setter
    def rate(self, new_rate):
        self.__rate = new_rate

    @property
    def spot(self):
        return self.__spot

    @spot.setter
    def spot(self, new_spot):
        self.__spot = new_spot

    @property
    def volatility(self):
        return self.__volatility

    @volatility.setter
    def volatility(self, new_volatility):
        self.__volatility = new_olatility

    @property
    def dividend(self):
        return self.__dividend

    @dividend.setter
    def dividend(self, new_yield):
        self.__dividend = new_yield
        
    def get_data(self):
        return (self.__spot, self.__rate, self.__volatility, self.__dividend)
    

class OptionFacade(object):
    """Facade Class to price an option"""

    def __init__(self, option, engine, data):
        self.option = option
        self.engine = engine
        self.data = data

    def price(self):
        return self.engine.calculate(self.option, self.data)
    

def main():
    strike = 40.0
    expiry = 1.0
    spot = 41.0
    rate = 0.08
    volatility = 0.30
    dividend = 0.0
    call = VanillaOption(expiry, strike, call_payoff)
    data = MarketData(rate, spot, volatility, dividend)
    
    nodes = 3
    binom_engine = BinomialPricingEngine(nodes, EuropeanBinomialPricer)
    the_option = OptionFacade(call, binom_engine, data)
    price = the_option.price()
    print("The Call Price with {0} nodes is: {1:.3f}".format(nodes, price))

    
if __name__ == "__main__":
    main()
