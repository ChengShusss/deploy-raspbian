import paramiko

class ExecuteObject:
    def __init__(self, hostname, username, password, port=22):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ssh = paramiko.SSHClient()
    
    def __enter__(self):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self.hostname, port=self.port,
                         username=self.username, password=self.password)
        return self
    
    def exec_command(self, command):
        _, stdout, _ = self.ssh.exec_command(command)
        return (stdout.read().decode("utf-8"))

    def __exit__(self, type, value, trace):
        if self.ssh:
            self.ssh.close()


def main():
    with ExecuteObject('192.168.137.82', 'pi', 'raspberry') as exec:
        result = exec.exec_command('df')
        print(result)

if __name__ == "__main__":
    main()