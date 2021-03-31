"""
Description: 

Author: Cheng Shu
Date: 2021-03-31 21:56:40
LastEditTime: 2021-04-01 00:09:59
LastEditors: Cheng Shu
FilePath: \deploy-raspbian\src\SSHConnection.py
@Copyright © 2020 Cheng Shu
License: MIT License
"""

import paramiko
from Setting import TIMEOUT, HOST, USER, PASSWORD

class SSHConnection:
    """
    description: 
    param {*} self
    param {str} hostname
    param {str} username
    param {str} password
    param {int} port
    return {*}
    """
    def __init__(self, hostname:str, username:str, password:str, port:int=22):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
    
    def __enter__(self):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.hostname, port=self.port,
                         username=self.username, password=self.password,
                         timeout=TIMEOUT)
        return self
    
    def exec_command(self, command):
        _, stdout, _ = self.ssh.exec_command(command, timeout=TIMEOUT)
        return (stdout.read().decode("utf-8"))

    def __exit__(self, type, value, trace):
        if self.ssh:
            self.ssh.close()


def main():
    try:
        with SSHConnection(HOST, USER, PASSWORD) as conn:
            result = conn.exec_command('ps |grep "open"')
            print(result)
    except paramiko.ssh_exception.NoValidConnectionsError as e:
        print(e)

if __name__ == "__main__":
    main()