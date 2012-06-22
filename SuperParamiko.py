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
        return partial(self.ssh_func_wrapper, name)

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        return
