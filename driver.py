'''
Created on May 10, 2020

@author: Zoya Samsonov
'''

import utils

def main():
    data = \
    [utils.point(0,0,0,True),
     utils.point(0,0,1,True),
     utils.point(0,1,0,True),
     utils.point(0,1,1,False),
     utils.point(1,0,0,True),
     utils.point(1,0,0,True),
     utils.point(1,1,0,False),
     utils.point(1,0,1,True),
     utils.point(1,1,0,False),
     utils.point(1,1,0,False)]

    validation = \
    [utils.point(0,0,0,True),
     utils.point(0,1,1,True),
     utils.point(1,1,0,True),
     utils.point(1,0,1,False),
     utils.point(1,0,0,True)]

    forest = utils.forest(data)
    forest.genMTreesNPoints(10, 10)
    for v in validation:
        forest.validate(v)

if __name__ == "__main__":
    main()
