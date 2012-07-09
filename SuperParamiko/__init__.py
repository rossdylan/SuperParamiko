import paramiko


class SuperParamiko(object):
    """
    Allows for pbs like functionality over ssh using paramiko

    :type host: str
    :param host: Hostname of the remote server

    :type username: str
    :param username: Username of the remote user

    :type password: str
    :param password: Password of the remote user

    :type port: int
    :param port: Port of the remote server
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
        """
        Generate the command string used to execute the command

        :type cmd: str
        :param cmd: The base command to execute
        """

        command = [cmd.replace("_","-"),]
        command.extend(list(args))
        for key, arg in kwargs.items():
            if arg == None or arg == "":
                command.append("--{0}".format(key))
            else:
                command.append("--{0} {1}".format(key, arg))
        return ' '.join(command)

    def ssh_func_wrapper(self, cmd, *args, **kwargs):
        """
        Function wrapper, wraps the remote command in a python function and
        returns the output as a list of strings

        :type cmd: str
        :param cmd: The root command to execute
        """

        command = self.generate_command_string(cmd, *args, **kwargs)
        stdin, stdout, stderr = self.session.exec_command(command)
        errors = stderr.readlines()
        if errors != []:
            raise Exception(errors)
        else:
            return map(lambda s: s.strip(), stdout.readlines())

    def __getattr__(self, name):
        """
        Use __getattr__ to create out command structure

        :type name: str
        :param name: name of the attribute to find
        """

        return command(name, self)

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        return


class command(object):
    """
    command object,used to recursive build a command string and execute it
    remotely. Allows for calling commands like: ssh.git.pull()

    :type name: str
    :param name: name of this command

    :type sp: SuperParamiko
    :param sp: Instance of SuperParamiko to use in calling the final command

    :type prev: command
    :param prev: the command object that comes before this
    """
    def __init__(self, name, sp, prev=None):
        self.sp = sp #SuperParamiko instance used to run command
        self.name = name
        self.prev = prev

    def __getattr__(self, name):
        setattr(self, name, command(name, self.sp, prev=self))
        return getattr(self, name)

    def cmd_string(self):
        """
        Recursively generates the full command string

        :rtype: str
        """

        if self.prev == None:
            return self.name
        else:
            return "{0} {1}".format(self.prev.cmd_string(), self.name)

    def __call__(self, *args, **kwargs):
        """
        Used to execute the command on the remote system

        :rtype: list of strings
        """

        cmd_string = self.cmd_string()
        cmd_list = cmd_string.split(" ")
        cmd = cmd_list[0]
        cmd_list = tuple(cmd_list[1:])
        args = cmd_list + args
        return self.sp.ssh_func_wrapper(cmd, *args, **kwargs)
