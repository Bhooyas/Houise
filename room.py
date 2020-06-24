from random import choice
from os import mkdir,path

def create_room(user):
    name = "".join([str(choice(list(range(0,10)))) for _ in range(4)])
    pwd = "".join([str(choice(list(range(0,10)))) for _ in range(4)])
    foldername = "{}.{}".format(name,pwd)
    mkdir(foldername)
    userfile = "{}/user.txt".format(foldername)
    ufile = open(userfile,"a")
    ufile.write("{}\n".format(user))
    ufile.close()
    numbersfile = "{}/numbers.txt".format(foldername)
    nfile = open(numbersfile,"a")
    nfile.close()
    winnerfile = "{}/winners.txt".format(foldername)
    wfile = open(winnerfile,"a")
    for k in ['Full1','Full2','First 5','First Row','Second Row','Third Row','Jawani(1 to 50)','Budhapa(50 to 90)']:
        wfile.write(k)
        wfile.write(',-\n')
    wfile.close()
    return (name,pwd,userfile,numbersfile,winnerfile)
    
def join_room(name,pwd,user):
    foldername = "{}.{}".format(name,pwd)
    if path.exists(foldername):
        userfile = "{}/user.txt".format(foldername)
        numbersfile = "{}/numbers.txt".format(foldername)
        winnerfile = "{}/winners.txt".format(foldername)
        ufile = open(userfile,"a")
        ufile.write("{}\n".format(user))
        ufile.close()
        return (True,userfile,numbersfile,winnerfile)
    return (False,"","","")
