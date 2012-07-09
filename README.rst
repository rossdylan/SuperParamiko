SuperParamiko
=============

Paramiko With Super Powers

SuperParamiko gives Paramiko the power of pbs
So if you want to call ls on a remote machine you can do it like so:

        ssh = SuperParamiko(host, username, password=password)
        ssh.ls()
Or perhaps you want to cat foo.bar on the remote system.

   ssh.cat("foo.bar")

Another feature is this:
   ssh.git.pull()
   or...
   ssh.ps.ax()
Its pretty cool
