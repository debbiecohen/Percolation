import random
import math
from typing import List

###############################################################################
# this is the abstract base class
# we are not concerned with making it work
class UnionFind(object):
    def __init__(self, N: int):
        pass

    # define connected in terms of find
    def connected(self, p: int, q: int) -> bool:
        return self.find(p) == self.find(q)

    def union(self, p: int, q: int) -> None:
        pass

    def find(self, p: int) -> int:
        return p
    
class QuickFind(UnionFind):
    def __init__(self, N: int):
        # allocate space for N integers
        # and assign each position to point to itself
        # can do this in one line, as follows

        # set id of each object to itself (N array accesses)
        self.id: List[int] = [i for i in range(N)]

    # do not rewrite connected(), it exists
    # and calls find.

    def find(self, p: int) -> int:
        # return the id of p (1 array access)
        return self.id[p]

    def union(self, p: int, q: int):
        pid: int = self.id[p]
        qid: int = self.id[q]

        # change all entries with id[p] to id[q]
        # (at most 2N + 2 array accesses)
        for i in range(len(self.id)):
            if self.id[i] == pid:
                self.id[i] = qid
                
class QuickUnion(UnionFind):
    def __init__(self, N: int):
        # allocate space for N integers
        # and assign each position to point to itself
        # can do this in one line, as follows

        # set id of each object to itself (N array accesses)
        self.id: List[int] = [i for i in range(N)]

    # do not rewrite connected(), it exists
    # and calls find.

    def find(self, p: int) -> int:
        # chase parent pointers until reach root
        # (depth of i array accesses)

        while p != self.id[p]:
            p = self.id[p]

        return p

    def union(self, p: int, q: int):
        # change root of p to point to root of q
        # (depth of p and q array accesses)
        i: int = self.find(p)
        j: int = self.find(q)
        self.id[i] = j
        
class WeightedQuickUnion(QuickUnion):
    def __init__(self, N: int):
        # allocate space for N integers
        # and assign each position to point to itself
        # can do this in one line, as follows

        # set id of each object to itself (N array accesses)
        self.id: List[int] = [i for i in range(N)]

        # add the sz array to maintain weights of each tree
        self.sz: List[int] = [ 1 ] * N

    # do not rewrite connected(), it exists
    # and calls find.

    # no changes to find(), but will provide anyway for complete code

    def find(self, p: int) -> int:
        # chase parent pointers until reach root
        # (depth of i array accesses)

        while p != self.id[p]:
            p = self.id[p]

        return p

    # for WeightedQuickUnion, the modification is to the union method
    def union(self, p: int, q: int):
        # change root of p to point to root of q
        # (depth of p and q array accesses)
        i: int = self.find(p)
        j: int = self.find(q)

        if i == j:
            return

        # of i and j, which is lighter?
        if self.sz[i] < self.sz[j]:
            self.id[i] = j
            self.sz[j] += self.sz[i]
        else:
            self.id[j] = i
            self.sz[i] += self.sz[j]
            
################################################################################
            
class PercolationQF(object):

    # creates n-by-n grid, with all sites initially blocked
    def __init__(self, n: int):
        if n<=0:
            raise ValueError("The size is not valid")       
        self.size: int = n
        self.topV: int  = n**2
        self.bottomV: int = n**2+1
        self.qf2 = QuickFind(self.topV + 2)                                     #Num of elems from the grid + top + bottom
        self.qf = QuickFind(self.topV + 1)                                      #Num of elems from the grid + top
        self.grid: List[bool] = [False for i in range(self.topV)]
        self.openCount: int  = 0


    # opens the site (row, col) if it is not open already
    def open(self, row: int, col: int) -> None:
        rowIdx: int = row-1                                                     #because indexing starts at 0 and row and col are from 1-N
        colIdx: int = col-1        
        if self.size-1<rowIdx<0 or self.size-1<col<0:
            raise ValueError("Arguments outside prescribed range")        
        
        idx: int = (rowIdx*self.size) + colIdx                                  
        if self.grid[idx]: return                                               #if is open already do nothing
        self.grid[idx] = True                                                   #open site
        self.openCount +=1                             
        
        left: int = (rowIdx*self.size) + (colIdx-1) if colIdx>0 else -1         #find index of left, right, top and bottom
        right: int = (rowIdx*self.size) + (colIdx+1) if colIdx<self.size-1 else -1
        top: int = ((rowIdx-1)*self.size) + (colIdx) if rowIdx>0 else -1
        bottom: int = ((rowIdx+1)*self.size) + (colIdx) if rowIdx<self.size-1 else -1
        
        if left>=0 and self.grid[left]:
            self.qf.union(idx, left)
            self.qf2.union(idx, left)
            
        if right>=0 and self.grid[right]:
            self.qf.union(idx, right)  
            self.qf2.union(idx, right)
            
        if top>=0 and self.grid[top]:
            self.qf.union(idx, top)
            self.qf2.union(idx, top)
        elif top == -1:                                                         #if is the first row, connect it to the virtual top site
            self.qf.union(self.topV, idx)
            self.qf2.union(self.topV, idx)
            
        if bottom>=0 and self.grid[bottom]:
            self.qf.union(idx, bottom) 
            self.qf2.union(idx, bottom) 
        elif bottom == -1:                                                      #if is the last row, connect it to the virtual top site
            self.qf2.union(self.bottomV, idx) 
            
            
    # is the site (row, col) open?
    def is_open(self, row: int, col: int) -> bool:
        if self.size<row<1 or self.size<col<1:
            raise ValueError("Arguments outside prescribed range")     
        rowIdx: int = row-1
        colIdx: int = col-1
        idx: int = (rowIdx*self.size) + colIdx
        return self.grid[idx]

    # is the site (row, col) full?
    def is_full(self, row: int, col: int) -> bool:
        if self.size<row<1 or self.size<col<1:
            raise ValueError("Arguments outside prescribed range")   
        rowIdx: int = row-1
        colIdx: int = col-1
        idx: int = (rowIdx*self.size) + colIdx        
        return self.is_open(row, col) and self.qf.connected(self.topV, idx)

    # returns the number of open sites
    def number_of_open_sites(self) -> int:
        return self.openCount

    # does the system percolate?
    def percolates(self) -> bool:
        return self.qf2.connected(self.topV, self.bottomV)
    
    def __str__(self) -> str:
        ans: str= ""
        for i in range(0,self.topV,self.size):
            ans+=str(self.grid[i:i+self.size])+"\n"
        return ans
    
    def animates2(self):
        ans = ""
        for i in range(1, self.size+1):
            row = []
            for j in range(1, self.size+1):
                if self.is_full(i, j):
                    row.append(0)
                else:
                    row.append(1)
            ans+=(str(row)+"\n")
        return ans    
    
    def animates(self):                                                         
        ans = ""
        for i in range(1, self.size+1):
            row = []
            for j in range(1, self.size+1):
                if self.is_full(i, j):
                    row.append(0)                                               #0 are going to be the blue sites
                elif self.is_open(i, j):
                    row.append("*")                                             #* are going to be the white sites
                else:
                    row.append(1)                                               #1 are going to be the black sites
            ans+=(str(row)+"\n")
        return ans    
    

class PercolationWQU(object):

    # creates n-by-n grid, with all sites initially blocked
    def __init__(self, n: int):
        if n<=0:
            raise ValueError("The size is not valid")       
        self.size: int = n
        self.topV: int = n**2
        self.bottomV: int = n**2+1
        self.wqu2 = WeightedQuickUnion(self.topV + 2)                           #Num of elems from the grid + top + bottom
        self.wqu = WeightedQuickUnion(self.topV + 1)                            #Num of elems from the grid + top
        self.grid: List[bool] = [False for i in range(self.topV)]
        self.openCount: int = 0


    # opens the site (row, col) if it is not open already
    def open(self, row: int, col: int) -> None:
        rowIdx: int = row-1                                                     #because indexing starts at 0 and row and col are from 1-N
        colIdx: int = col-1        
        if self.size-1<rowIdx<0 or self.size-1<col<0:
            raise ValueError("Arguments outside prescribed range")        
        
        idx: int = (rowIdx*self.size) + colIdx                                  #if is open already
        if self.grid[idx]: return
        self.grid[idx] = True                                                   #open site
        self.openCount +=1                             
        
        left: int = (rowIdx*self.size) + (colIdx-1) if colIdx>0 else -1         #find index of left, right, top and bottom
        right: int = (rowIdx*self.size) + (colIdx+1) if colIdx<self.size-1 else -1
        top: int = ((rowIdx-1)*self.size) + (colIdx) if rowIdx>0 else -1
        bottom: int = ((rowIdx+1)*self.size) + (colIdx) if rowIdx<self.size-1 else -1
        
        if left>=0 and self.grid[left]:
            self.wqu.union(idx, left)
            self.wqu2.union(idx, left)
            
        if right>=0 and self.grid[right]:
            self.wqu.union(idx, right)
            self.wqu2.union(idx, right)  
            
        if top>=0 and self.grid[top]:
            self.wqu.union(idx, top)  
            self.wqu2.union(idx, top)
        elif top == -1:                                                         #if is the first row, connect it to the virtual top site
            self.wqu.union(self.topV, idx)
            self.wqu2.union(self.topV, idx)
        
        if bottom>=0 and self.grid[bottom]:
            self.wqu.union(idx, bottom) 
            self.wqu2.union(idx, bottom)
        elif bottom == -1:                                                      #if is the last row, connect it to the virtual top site
            self.wqu2.union(self.bottomV, idx) 
            
            
    # is the site (row, col) open?
    def is_open(self, row: int, col: int) -> bool:
        if self.size<row<1 or self.size<col<1:
            raise ValueError("Arguments outside prescribed range")     
        rowIdx: int = row-1
        colIdx: int = col-1
        idx: int = (rowIdx*self.size) + colIdx
        return self.grid[idx]

    # is the site (row, col) full?
    def is_full(self, row: int, col: int) -> bool:                              
        if self.size<row<1 or self.size<col<1:
            raise ValueError("Arguments outside prescribed range")   
        rowIdx: int = row-1
        colIdx: int = col-1
        idx: int = (rowIdx*self.size) + colIdx        
        return self.is_open(row, col) and self.wqu.connected(idx,self.topV)     #the current site is connected to the virtual top site
    
    # returns the number of open sites
    def number_of_open_sites(self) -> int:
        return self.openCount                                                   #everytime I open a site I increment the count

    # does the system percolate?
    def percolates(self) -> bool:
        return self.wqu2.connected(self.topV, self.bottomV)
    
    def __str__(self) -> str:
        ans: str = ""
        for i in range(0,self.topV,self.size):
            ans+=str(self.grid[i:i+self.size])+"\n"
        return ans
    
    def animates(self):                                                         
        ans = ""
        for i in range(1, self.size+1):
            row = []
            for j in range(1, self.size+1):
                if self.is_full(i, j):
                    row.append(0)                                               #0 are going to be the blue sites
                elif self.is_open(i, j):
                    row.append("*")                                             #* are going to be the white sites
                else:
                    row.append(1)                                               #1 are going to be the black sites
            ans+=(str(row)+"\n")
        return ans    
                    
    


   
import sys
def main() -> None:
    #Monte Carlo simulation
    print("Monte Carlo with quickfind")
    p = PercolationQF(4)
    while not p.percolates():
        randX = random.randint(1,p.size)
        randY = random.randint(1,p.size)
        p.open(randX, randY)
    print(p.number_of_open_sites()/(p.size**2))
    print(p)
    print(p.animates())
    
    print("Monte Carlo with weigthed quick union")
    q = PercolationWQU(4)
    while not q.percolates():
        randX = random.randint(1,q.size)
        randY = random.randint(1,q.size)
        q.open(randX, randY)
    print(q.number_of_open_sites()/(q.size**2))
    print(q)
    print(q.animates())    
        
    

if __name__ == '__main__':
    main()