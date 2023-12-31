#!/usr/bin/env python3.2 
import sys, glob, os, stat
#from rarfile import RarFile

from time import time
lastTime = time()

try:
    with open( '{}.log'.format(sys.argv[1]) ) as lastLog:
        lastFile = lastLog.readline()
        offset = lastLog.readline()
        print('Reading password at {} from {}'.format(offset, lastFile))
except Exception:
    print('no last file')
    lastFile = None
    offset = 0

#with RarFile(sys.argv[1]) as rarFile:
for i in range(2,len(sys.argv)):
    for filename in glob.glob(sys.argv[i]):
        if lastFile and filename != lastFile[:-1]:
            continue

        fileStats = os.stat(filename)
        if not stat.S_ISREG(fileStats[stat.ST_MODE]) and \
                not stat.S_ISLNK(fileStats[stat.ST_MODE]):
            continue

        with open(filename) as dictFile:
            dictFile.seek(int(offset))
            count = 0
            print('Reading password from {}'.format(sys.argv[i]))
            while True:
                try:
                    password = dictFile.readline()
                except Exception: #encoding Exception
                    lastFile = None
                    offset = 0
                    print('Error in readline')
                    break
            #for password in dictFile:
                if len(password) == 1:
                    continue
                elif password == '':
                    lastFile = None
                    offset = 0
                    #try:
                    #    os.remove('{}.log'.format(sys.argv[1]))
                    #except Exception:
                    #    print('log file not exists')
                    break

                #rarFile.extractall(pwd=password[:-1])
                try:
                    a = os.popen("unrar t -y -p'{}' {} 2>&1 | grep 'All OK'".format(
                        password[:-1].replace("'","."), sys.argv[1]))
                    for outLine in a.readlines():
                        print(outLine)
                        if outLine == 'All OK\n':
                            print('?????:{}'.format(password))
                            sys.stderr.write('?????:{}'.format(password))
                            exit(0)
                except Exception:
                    print('error in popen')
                    continue
 
                count += 1
                if count == 200:
                    nowTime = time()
                    print('Current : {} , Speed : {} pwds/s'.format(password[:-1],
                        count//(nowTime - lastTime)))
                    count = 0
                    lastTime = nowTime

                    with open('{}.log'.format(sys.argv[1]), 'w',
                            encoding='utf-8') as log:
                        log.write('{}\n{}'.format(filename,dictFile.tell()))
                        #log.write('{}\n{}'.format(filename,'0'))


