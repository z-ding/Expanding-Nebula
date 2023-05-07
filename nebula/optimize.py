import numpy as np
def solution(g):
    m = len(g)
    n = len(g[0])
    #create an 2d array of m+1, n+1
    matrix= np.full((m, n,2),[0,0]) # 4 possible value remaining
    for i in range(0,m):
        for j in range(0,n):
            if g[i][j] == True:
                matrix[i][j] = [1,4] #one 1 only in the 2*2 square start from i,j
            else:
                matrix[i][j] = [0,4]
    #print(matrix)
    #start from cells with value 1, we know there can be one and only one 1 in the 2*2 grid
    #to increase efficiency we should use bitmask to memorize what combinations we have already checked
    #cell [r,c] will be r*width + c th number from [0, width*height-1], while i th number from [0,width*height-1] will have index [i / height,i%width] in the matrix
    #the bitmask status will record on which positions we have -1, 0 and 1. use 3 binary numbers to record the position where we have -1, 0 and 1 respectively
    grid = np.full((m+1, n+1),-1) # fill the grid
    memo = np.empty((m+2, n+2), dtype=object)
    for i in range(m+2):
        for j in range(n+2):
            memo[i][j] = dict()
    def isValid(r,c, modified):
        #print("updating " + str(r) + "," + str(c))
        if r<0 or c<0 or r== m or c == n:
            return True # out of boundary, no need to check
        matrix[r][c][1] -=1
        modified.append([r,c])
        #print(matrix)       
        #check whether the 2*2 grid from [i,j] is valid
        cntOne = 0
        if grid[r+1][c] == 1: cntOne +=1
        if grid[r][c] == 1: cntOne +=1
        if grid[r+1][c+1] == 1: cntOne +=1
        if grid[r][c+1] == 1: cntOne +=1
        if matrix[r][c][0] == 1 and cntOne >1:
            return False
        if matrix[r][c][1] ==0:
            if matrix[r][c][0] == 1 and cntOne!= 1:
                return False
            if matrix[r][c][0] == 0 and cntOne == 1:
                return False
        return True
    def backtracking(r,c,status): #status is a tuple of (previous row, this row)
        #print(str(r) + "," + str(c) + "," + str(status))
        #print(memo)
        if c == n+1:
            #print("valid grid found")
            #print(grid)
            memo[r][c][status] = 1
            return 1
        if status in memo[r][c]:
            return memo[r][c][status]
        count = 0
        if r == m+1:
            count += backtracking(0,c+1,(status[1],0)) # fill next col
            memo[r][c][status] = count
            return count

        if grid[r][c] != -1:
            count += backtracking(r+1,c,status)# fill next cell
            memo[r][c][status] = count
            return count
        # fill this cell with 0 || 1 and check whether valid
        for i in range(0,2):
            grid[r][c] = i
            #a cell [i,j] needs to be reflected in maximum 4 cells:
            #[i-1,j-1], [i-1,j],[i,j-1],[i,j]
            cells = [[r-1,c-1], [r-1,c],[r,c-1],[r,c]]
            going = True
            minus1 = []
            for j in range(0,4):
                #print("grid")
                #print(grid)
                if isValid(cells[j][0],cells[j][1],minus1) == False:
                    going = False
                    break
            if going:
                if i == 1:
                    count += backtracking(r+1,c,(status[0],status[1] | (1<<r)))
                else:
                    count += backtracking(r+1,c,status)
            #backtracking
            for k in range(0,len(minus1)):
                matrix[minus1[k][0]][minus1[k][1]][1]+=1
            grid[r][c] = -1
        memo[r][c][status] = count
        return count
    ans= backtracking(0,0,(0,0))
    return ans
x = solution([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]])
print(x)
