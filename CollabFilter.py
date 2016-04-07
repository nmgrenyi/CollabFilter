import sys
import math


def pearson_correlation(User1,User2):
    U1 = {}
    U2 = {}
    global inputdata
    for line in open(inputdata):
        line2 = line.split('\t')
        if line2[0] == User1:
            U1[line2[2]] = float(line2[1])
        elif line2[0] == User2:
            U2[line2[2]] = float(line2[1])
    i = 0
    n = 0
    for pair in U1:
        i = i + 1
        n = n + float(U1[pair])
    averageUserOne = n / i
    j = 0
    m = 0
    for pair in U2:
        j = j + 1
        m = m + float(U2[pair])
    averageUserTwo = m / j

    temp = list(set(U1.keys()) & set(U2.keys()))
    U1_intersection = {}
    U2_intersection = {}
    for key in temp:
        U1_intersection[key] = U1[key]
        U2_intersection[key] = U2[key]
    for key in U1_intersection:
        U1_intersection[key] = U1_intersection[key] - averageUserOne
    for key in U2_intersection:
        U2_intersection[key] = U2_intersection[key] - averageUserTwo
    number = 0
    nn = 0
    for key in temp:
        nn = U1_intersection[key]*U2_intersection[key]
        number = number + nn
    number1 = 0
    nn1 = 0
    for key in temp:
        nn1 = U1_intersection[key]*U1_intersection[key]
        number1 = number1 + nn1
    sqrtu1 = math.sqrt(number1)
    number2 = 0
    nn2 = 0
    for key in temp:
        nn2 = U2_intersection[key]*U2_intersection[key]
        number2 = number2 + nn2
    sqrtu2 = math.sqrt(number2)
    demoniator = sqrtu1 * sqrtu2
    if demoniator == 0:
        return 0
    w = number / demoniator
    return w

def K_nearest_neighbors(user1,k):
    list_of_userid = []
    global inputdata
    for line in open(inputdata):
        line2 = line.split('\t')
        if line2[0] not in list_of_userid:
            list_of_userid.append(line2[0])
    list_of_userid.remove(user1)
    list_of_allrate_alluser = []
    for i in list_of_userid:
        list_of_1rate_1user=[pearson_correlation(i,user1),i]
        list_of_allrate_alluser.append(list_of_1rate_1user)
    list_of_allrate_alluser.sort(reverse=True)
#    print list_of_allrate_alluser[*][0]
    X = []
    for i in list_of_allrate_alluser:
        X.append(i[0])
    index = 0
    compare = 1
    compare1 = 0
    while compare1 < int(k):
        if cmp(X[index],X[compare])==0:
            compare = compare + 1
            compare1 = compare1 + 1
        else:
            compare1 = compare1 + 1
    if compare == int(k):
        list_of_allrate_alluser.sort(key = lambda x:x[1])
    list_of_top_10rate_user = list_of_allrate_alluser[0:int(k)]
    return list_of_top_10rate_user


def Predict(user1,item,k_nearest_neighbors):
    L = k_nearest_neighbors
    total = 0
    allw = 0
    global inputdata
    for rate_user in L:
        print rate_user[1],
        print rate_user[0]
        n = 0
        item_rate = 0
        for line in open(inputdata):
            line2 = line.split('\t')
            if line2[2].replace("\n","") == item and line2[0] == rate_user[1]:
                item_rate = float(line2[1])
                allw = allw + abs(rate_user[0])
        n = item_rate * rate_user[0]
        total = total + n
    if allw == 0:
        print '\n'
        print "Sorry, wrong input"
    else:
        p = total / allw
        print '\n'
        print p
    return


if __name__ == '__main__':
    inputdata = sys.argv[1]
    inputdata1 = sys.argv[2]
    inputdata2 = sys.argv[3]
    inputdata3 = sys.argv[4]

    S = K_nearest_neighbors(inputdata1,inputdata3)
    Predict(inputdata1,inputdata2,S)
