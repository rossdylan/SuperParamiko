import paramiko
from functools import partial

class SuperParamiko(object):
    """
    usage:
    >> ssh = SuperParamiko("hostname", "username")
    >> ssh.ls()
    >> ssh.git("pull")
    OR;
       with SuperParamiko("hostname", "username") as ssh:
           ssh.ls()
           ssh.git("pull")
    """
    def __init__(self, host, username, password=None, port=22):
        self.session = paramiko.SSHClient()
        self.session.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
        if password == None:
            self.session.connect(host, username=username, port=port)
        else:
            self.session.connect(
                    host,
                    username=username,
                    password=password,
                    port=port
            )

    def generate_command_string(self, cmd, *args, **kwargs):
        command = [cmd,]
        command.extend(list(args))
        for key, arg in kwargs.items():
            if arg == None or arg == "":
                command.append("--{0}".format(key))
            else:
                command.append("--{0} {1}".format(key, arg))
        return ' '.join(command)

    def ssh_func_wrapper(self, cmd, *args, **kwargs):
        command = self.generate_command_string(cmd, *args, **kwargs)
        stdin, stdout, stderr = self.session.exec_command(command)
        errors = stderr.readlines()
        if errors != []:
            raise Exception(errors)
        else:
            return map(lambda s: s.strip(), stdout.readlines())

    def __getattr__(self, name):
        return command(name, self)

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        return


class command(object):
    def __init__(self, name, sp, prev=None):
        self.sp = sp #SuperParamiko instance used to run command
        self.name = name
        self.prev = prev

    def __getattr__(self, name):
        setattr(self, name, command(name, self.sp, prev=self))
        return getattr(self, name)

    def cmd_string(self):
        if self.prev == None:
            return self.name
        else:
            return "{0} {1}".format(self.prev.cmd_string(), self.name)

    def __call__(self, *args, **kwargs):
        cmd_string = self.cmd_string()
        cmd_list = cmd_string.split(" ")
        cmd = cmd_list[0]
        cmd_list = tuple(cmd_list[1:])
        args = cmd_list + args
        return self.sp.ssh_func_wrapper(cmd, *args, **kwargs)
