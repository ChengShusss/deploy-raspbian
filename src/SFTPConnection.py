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
from Setting import TIMEOUT, HOST, USER, PASSWORD

# ------------------------------------------
# @description: Provide a packaged class for sftp connection.
# @param {host:}
# @return {*}
# ------------------------------------------
class SFTPConnection:
    def __init__(self, host, user, password, path='/home', port=22):
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
        return self.sftp
    
    def __exit__(self, type, value, trace):
        if self.sftp:
            self.sftp.close()


def testCode():
    with SFTPConnection(HOST, USER, PASSWORD, '/home') as sftp:
        sftp.chdir("/home/pi")
        try:
            sftp.listdir("./testDeploy")
        except FileNotFoundError:
            sftp.mkdir("./testDeploy")
        
        print(sftp.listdir("./testDeploy"))

if (__name__=="__main__"):
    testCode()