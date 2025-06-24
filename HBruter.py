#!/usr/bin/env python3
from string import punctuation,digits,ascii_lowercase,ascii_uppercase
from hashlib import algorithms_available,new
from argparse import ArgumentParser
from os.path import exists,basename
from itertools import product
from threading import Thread
from os import system,name
from time import sleep
from sys import exit
__author__="Vahab Programmer https://github.com/Vahab-Programmer"
__version__="0.0.1"
class HBruter:
    __cmd="cls" if name=="nt" else "clear"
    __active=True
    __count=0
    __hashed=0
    __current=None
    __text=None
    apc=0
    def __init__(self):
        parser=ArgumentParser()
        parser.add_argument("hash",action="store",help="Target hash To Crack")
        parser.add_argument("-w","--wordlist",action="store",type=str,required=False,help="WordList File To Include")
        args=parser.parse_args()
        self.__hashlen=len(args.hash)
        args.wordlist=str(args.wordlist)
        algorithm=self.__getinputs({i:v for i,v in enumerate(sorted(algorithms_available),1)})
        if algorithm=="shake_128" or algorithm=="shake_256":hashfunc=self.__hwl
        else:hashfunc=self.__hwol
        upper=self.__getinputs({1:True,2:False},"Do You Want To Use UpperCase Letters?")
        lower=self.__getinputs({1:True,2:False},"Do You Want To Use LowerCase Letters?")
        digit=self.__getinputs({1:True,2:False},"Do You Want To Use Digits?")
        symbol=self.__getinputs({1:True,2:False},"Do You Want To Use Symbols Characters?")
        if upper or lower or digit or symbol:
            llen=self.__getint("Min Length:")
            mlen=self.__getint("Max Length:")
        else:
            llen=0
            mlen=0
        data=""
        if upper:data+=ascii_uppercase
        if lower:data+=ascii_lowercase
        if digit:data+=digits
        if symbol:data+=punctuation
        if exists(args.wordlist):self.apc+=self.__cw(args.wordlist)
        if data:self.apc+=self.__apc(llen,mlen,data)
        logger=Thread(target=self.__logger)
        logger.daemon=True
        logger.start()
        for i in self.__generate(llen,mlen,data):
            self.__current=hashfunc(algorithm,i.encode())
            self.__text=i
            if args.hash==self.__current:
                self.__active=False
                logger.join()
                print("\nHash Found! {} = {}".format(i,self.__current))
                exit(0)
            self.__count+=1
            self.__hashed+=1
        if exists(args.wordlist):
            with open(args.wordlist,"rb") as file:
                i=file.readline()
                while i:
                    i=i.split(b"\n")[0]
                    self.__current=hashfunc(algorithm,i)
                    self.__text=i.decode("raw_unicode_escape")
                    if args.hash == self.__current:
                        self.__active = False
                        logger.join()
                        print("\nHash Found! {} = {}".format(i.decode(), self.__current))
                        exit(0)
                    self.__count += 1
                    self.__hashed += 1
                    i=file.readline()
        self.__active=False
        logger.join()
        print("\nHash Not Found!")
    def __cs(self)->None:system(self.__cmd)
    @staticmethod
    def __hwol(hname:str,data:bytes)->str:return new(hname,data).hexdigest()
    def __hwl(self,hname:str,data:bytes)->str:return new(hname,data).hexdigest(self.__hashlen)
    def __cw(self,filepath:str)->int:
        self.__cs()
        count=0
        print("Counting Words in {} ...".format(basename(filepath)))
        with open(filepath,"rb") as file:
            tmp=file.readline()
            while tmp:
                count+=1
                tmp=file.readline()
        return count
    @staticmethod
    def __apc(l:int,m:int,data:str)->int:
        count=0
        for length in range(l,m+1):
            count=len(data)**length
        return count
    def __getint(self,prompt:str)->int:
        self.__cs()
        try:datum=int(input(prompt))
        except ValueError:return self.__getint(prompt)
        return datum
    def __getinputs(self,kvalue:dict[int:any],prompt:str="")->any:
        self.__cs()
        if prompt:print(prompt)
        for key,value in kvalue.items():
            print(str(key)+"."+str(value))
        try:target=int(input("Select By Number:"))
        except ValueError:return self.__getinputs(kvalue,prompt)
        return kvalue.get(target) if kvalue.get(target,"")!="" else self.__getinputs(kvalue,prompt)
    def __logger(self)->None:
        self.__cs()
        while self.__active:
            self.__cs()
            print("Total: {} \nCurrent: {} \nHashed: {} \nEnded: {} \nRemaining: {} \nSpeed: {}".format(self.apc,self.__text,self.__current,self.__hashed,self.apc-self.__hashed,self.__divider(self.__count)))
            self.__count=0
            sleep(1)
    @staticmethod
    def __divider(num:int)->str:
        if num<1000:return "{} H/s".format(num)
        if 1000<num<1000000:return "{} Kh/s".format(num/1000)
        if 1000000<num<1000000000:return "{} Mh/s".format(num/1000000)
        return "{} Gh/s".format(num/1000000000)
    @staticmethod
    def __generate(mini:int,maxi:int,data:str)->str:
        for length in range(mini,maxi+1):
            for i in product(data,repeat=length):
                yield "".join(i)
try:HBruter()
except KeyboardInterrupt:print("User Stopped The Process!")