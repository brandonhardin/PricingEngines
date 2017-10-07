import numpy as np
from scipy.stats import binom

def CallPayOff(Spot, Strike):
    return np.maximum(Spot - Strike, 0.0)

def EuropeanBinomial(S, X, r, u, d, T):
    numSteps = 2
    numNodes = numSteps + 1
    spotT = 0.0
    callT = 0.0
    pu = (1 + r - d) / (u - d)
    pd = 1 - pu
    
    for i in range(numNodes):
        spotT = S * (u ** (numSteps - i)) * (d ** (i))
        callT += CallPayOff(spotT, X) * binom.pmf(numSteps - i, numSteps, pu)  
    callPrice = callT / ((1 + r) ** 2)
     
    return callPrice
        
def main():
    S = 41
    X = 40
    r = 0.08
    T = 1.0
    v = 0.30
    u = 1.2
    d = 0.8
    
    callPrice = EuropeanBinomial(S, X, r, u, d, T)
    print("The Two Period European Binomial Price is = %.4f" % callPrice)
                                                
main() 

