for x in '0123456789ABCDE':
    x1 = '1' + str(x) + '563'
    x2 = '871' + str(x) + '3'
    res = int(x1, 14) + int(x2, 14)
    if res % 24 == 0:
        print(res // 24) 
