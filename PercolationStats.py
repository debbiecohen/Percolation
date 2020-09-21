import statistics
import datetime
from Percolation import *

class PercolationStatsWQU(object):

    # perform independent trials on an n-by-n grid
    def __init__(self, n: int, trials: int):
        if trials<=0 or n<=0:
            raise ValueError("Invalid num of trials")
        self.percThreshold = []
        self.trials = trials
        for i in range(trials):
            p = PercolationWQU(n)
            while not p.percolates():
                toOpenRow = random.randint(1,n)
                toOpenCol = random.randint(1,n)
                p.open(toOpenRow, toOpenCol)
            self.percThreshold.append(p.number_of_open_sites()/(n**2))
                
        
    # sample mean of percolation threshold
    def mean(self) -> float:
        return statistics.mean(self.percThreshold)

    # sample standard deviation of percolation threshold
    def stddev(self) -> float:
        return statistics.stdev(self.percThreshold)

    # low endpoint of 95% confidence interval
    def confidence_low(self) -> float:
        return self.mean()-((1.96*self.stddev())/math.sqrt(self.trials))

    # high endpoint of 95% confidence interval
    def confidence_high(self) -> float:
        return self.mean()+((1.96*self.stddev())/math.sqrt(self.trials))
    
    def __str__(self):
        return ("mean= " + str(self.mean()) + "\nstdev= " +str(self.stddev()) + "\n95% interval= [" + str(self.confidence_low()) + "," + str(self.confidence_high()) + "]")
        
        

class PercolationStatsQF(object):
    # perform independent trials on an n-by-n grid
    def __init__(self, n: int, trials: int):
        if trials<=0 or n<=0:
            raise ValueError("Invalid num of trials")
        self.percThreshold = []
        self.trials = trials
        for i in range(trials):
            p = PercolationQF(n)
            while not p.percolates():
                toOpenRow = random.randint(1,n)
                toOpenCol = random.randint(1,n)
                p.open(toOpenRow, toOpenCol)
            self.percThreshold.append(p.number_of_open_sites()/(n**2))
                
        
    # sample mean of percolation threshold
    def mean(self) -> float:
        return statistics.mean(self.percThreshold)

    # sample standard deviation of percolation threshold
    def stddev(self) -> float:
        return statistics.stdev(self.percThreshold)

    # low endpoint of 95% confidence interval
    def confidence_low(self) -> float:
        return self.mean()-((1.96*self.stddev())/math.sqrt(self.trials))

    # high endpoint of 95% confidence interval
    def confidence_high(self) -> float:
        return self.mean()+((1.96*self.stddev())/math.sqrt(self.trials))
    
    def __str__(self):
        return ("mean= " + str(self.mean()) + \
                "\nstdev= " +str(self.stddev()) + \
                "\n95% interval= [" + str(self.confidence_low()) + "," + str(self.confidence_high()) + "]")


import sys
def main() -> None:
    args = sys.argv
    a = datetime.datetime.now()
    #pWQU=PercolationStatsWQU(200,100)
    pWQU: PercolationStatsWQU =PercolationStatsWQU(int(args[1]),int(args[2]))
    print(pWQU)    
    b = datetime.datetime.now()
    c = b - a
    print("n=" + args[1] + ", T=" + args[2], (c.microseconds/1000000)+c.seconds, "pWQU")

   
    d = datetime.datetime.now()
    #pQF=PercolationStatsQF(100,100)
    pQF: PercolationStatsQF = PercolationStatsQF(int(args[1]),int(args[2]))
    print(pQF)    
    e = datetime.datetime.now()
    f = e - d
    print("n=" + args[1] + ", T=" + args[2], (f.microseconds/1000000)+f.seconds, "pQF")
    

    
   


if __name__ == '__main__':
    main()