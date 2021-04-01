# ------------------------------------------
# @Author: Cheng Shu
# @Date: 2021-03-31 22:50:24
# @LastEditTime: 2021-03-31 23:49:39
# @LastEditors: Cheng Shu
# @Description: Provide File Transport using SFTP.
# @FilePath: \deploy-raspbian\src\SFTPConnection.py
# @@Copyright © 2020 Cheng Shu
# ------------------------------------------

import paramiko
import os
from Setting import TIMEOUT, HOST, USER, PASSWORD

# ------------------------------------------
# @description: Provide a packaged class for sftp connection.
# @param {host:}
# @return {*}
# ------------------------------------------
class SFTPConnection:
    """
    description: 
    param {*} host: Host name, used to be ip.
    param {*} user: User name.
    param {*} password: password.
    param {*} path: base path.
    param {*} port
    return {*}

    example:
    >   with SFTPConnection(HOST, USER, PASSWORD, '/home/pi') as conn:
    >       conn.deploy("./data", "ENBC")
    """
    def __init__(self, host:str, user:str, password:str, path:str='/home', port:int=22):
        self.host = host
        self.user = user
        self.password = password
        self.path = path
        self.port = port
        self.transport = None
        self.sftp = None

    def __enter__(self):
        self.transport = paramiko.Transport((self.host, self.port))
        self.transport.connect(
            username=self.user, password=self.password)
        self.sftp = paramiko.SFTP.from_transport(self.transport)
        self.sftp.chdir(self.path)
        return self
    
    def __exit__(self, type, value, trace):
        if self.sftp:
            self.sftp.close()
    
    """
    description: return fileList and dirList.
    param {*} self
    param {str} srcPath
    return {tuple(list, list)} (fileList, dirList)
    """
    def getList(self, srcPath:str):
        # travel in srcPath using BFS.
        stack = ['.']
        fileList = []
        dirList = []
        while stack:
            path = stack.pop()
            files = os.listdir(srcPath + path)
            for fileName in files:
                if os.path.isdir(srcPath + path + "/" + fileName):
                    stack.append(path + "/" + fileName)
                    dirList.append(path + "/" + fileName)
                else:
                    fileList.append(path + "/" + fileName)
        return (fileList, dirList)
    
    def deploy(self, srcPath:str, name):
        # handle boundary conditions
        if srcPath[-1] != "/":
            srcPath += "/"
        if not os.path.isdir(srcPath):
            print(f"[DIR NOT FOUND]\"{srcPath}\" do not exist. Please Check the path.")
            return

        
        try:
            self.sftp.listdir("./" + name)
        except FileNotFoundError:
            self.sftp.mkdir(name)
        finally:
            self.sftp.chdir(name)

        if not self.sftp:
            pass
            #raise 
        fileList, dirList = self.getList(srcPath)

        for dirName in dirList:
            try:
                self.sftp.listdir(dirName)
            except FileNotFoundError:
                self.sftp.mkdir(dirName)

        for fileName in fileList:
            self.sftp.put(srcPath + fileName, fileName)

  

def testCode():    
    with SFTPConnection(HOST, USER, PASSWORD, '/home/pi') as conn:
        conn.deploy("./data", "ENBC")

if (__name__=="__main__"):
    testCode()