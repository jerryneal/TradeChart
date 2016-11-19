from time import time
from math import exp, sqrt, log
from random import gauss, seed

if __name__ == '__main__':

    seed(20000)
    t0 = time()

    # Parameters
    S0 = 100. #Initial Value
    K = 105. # strike price
    T = 1.0 # Maturity
    r = 0.05 # riskless short rate
    sigma = 0.2  # volatility
    M = 50
    dt = T / M
    I = 250000

    # Simulating I paths with M time stamps
    S = []
    for i in range(I):
        path = []
        for t in range(M + 1):
            if t == 0:
                path.append(S0)
            else:
                z = gauss(0.0,1.0)
                St = path[t - 1] * exp((r - 0.5 * sigma ** 2) * dt + sigma * sqrt(dt) * z)
                path.append(St)
        S.append(path)

    # Calculating the Actual Simulation
    C0 = exp(-r * T) * sum([max(path[-1] - K,0) for path in S]) / I

    # Results output
    tpy = time() - t0

    print "European Option value %7.3f" % C0
    print "Duration in Seconds   %7.3f" % tpy