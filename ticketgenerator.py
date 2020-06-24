from random import shuffle,choice

def tickect_generator():
        row_1 = [1]*5 + [0]*4
        shuffle(row_1)
        row_2 = [1]*5 + [0]*4
        shuffle(row_2)
        row_3 = [0] * 9
        for i in range(len(row_1)):
                if row_1[i] == row_2[i] and row_1[i] == 0:
                        row_3[i] = 1
        for i in range(len(row_3)):
                if row_3.count(1) == 5:
                        break
                if row_3[i] == 0 and row_1[i]!= row_2[i]:
                        row_3[i] = 1
        
        for i in range(len(row_1)):
                temp = []
                while(len(temp)!=3):
                        x = choice(list(range(i*10+1,i*10+2+len(row_1))))
                        if x not in temp:
                                temp.append(x)
                temp.sort()
                if row_1[i] == 1:
                        row_1[i] = temp[0]
                if row_2[i] == 1:
                        row_2[i] = temp[1]
                if row_3[i] == 1:
                        row_3[i] = temp[2]

        tickect = []
        tickect_num = [row_1,row_2,row_3]
        temp = []
        for k in range(len(row_1)):
                temp.append([row_1[k],False])
        tickect.append(temp)
        temp = []
        for k in range(len(row_2)):
                temp.append([row_2[k],False])
        tickect.append(temp)
        temp = []
        for k in range(len(row_3)):
                temp.append([row_3[k],False])
        tickect.append(temp)
        return (tickect,tickect_num)
