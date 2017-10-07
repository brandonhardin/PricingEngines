import numpy as np

def callTPayoff(spot, strike):
    return np.maximum(spot - strike, 0.0)

spot = 100.0
strike = 100.0
expiry = 1.0
rate = 0.08
vol = 0.01 * 0.01
div = 0.0

kappa = 2.0
theta = 0.01
sigma = 0.1

M = 1000 # number of replications
N = 252  # number of steps

dt = expiry / N

path = np.zeros(N)
var = np.zeros(N)
callT = np.zeros(M)
z1 = np.random.normal(size=(M,N))
z2 = np.random.normal(size=(M,N))

for i in range(M):
    var[0] = theta
    path[0] = spot
    
    for j in range(1, N):
        #simulate variance equation first
        var[j] = var[j-1] + kappa * (theta - var[j-1]) * dt + sigma * np.sqrt(var[j-1] * dt) * z1[i,j]
        
        # use truncation method
        if var[j] <= 0.0:
            var[j] = np.maximum(var[j], 0.0)
            
        # simulation of price path
        path[j] = path[j-1] * np.exp((rate - div - 0.5 * var[j]) * dt + np.sqrt(var[j] * dt) * z2[i,j])
        
    callT[i] = callTPayoff(path[-1], strike)

result = callT.mean() * np.exp(-rate * expiry)
fmt = "The value of the callT option is: {0:0.3f}"
print(fmt.format(result))