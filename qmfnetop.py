#!/usr/bin/env python3
import subprocess
import os
import threading
import logging
import yaml
from datetime import datetime


class QMFNetOp:
    SETTTINGS_FILE='settings.yml'
    """ QMF network operation
    """
    def querySn(self, sn):
        found = []
        threads = []
        error = dict()
        # ls -1rt
        # -t     sort by modification time
        cmd = "find /RACKLOG/ -type f -iname *{}* -exec ls -tlhgG --time-style=long-iso {{}} +".format(sn)
        for ip in self.ts:
            x=threading.Thread(target=self.remoteJob, args=(found, ip, cmd, error))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()

        # The search result append into the list by multiple thread.
        found.sort(reverse=True, key=lambda d: datetime.strptime(d['date'], "%Y-%m-%d %H:%M"))
        return found, error

    def scp(self, ip, path):
        """ Copy file to a temporary file location
            copy without middle file system.
            estable password less login 
            ssh-copy-id -o ProxyCommand="ssh -W %h:%p cchiang@192.168.66.28" root@192.168.0.84
            scp -o ProxyCommand="ssh -W %h:%p cchiang@192.168.66.28" root@192.168.0.83:[file] /tmp
        """
        
        logging.info("Copy file {} form ip {}".format(path, ip))
        path= path.replace('[', '\[').replace(']', '\]').replace('(', '\(').replace(')', '\)')
        # .replace('(', '\(').replace(')', '\)')
        fn = os.path.basename(path)
        # Copy file to hop station 
        cmd = "scp {}:'{}' /tmp".format(ip, path)
        if self.hopStation is not None:
            cmd = "scp -o ProxyCommand=\"ssh -W %h:%p {}\" {}:'{}' /tmp".format(self.hopStation, ip, path)
        logging.debug(cmd)

        # using subprocess run will have problem when copy filename with brace.
        #result = subprocess.run(cmds, universal_newlines=True, stdout=subprocess.PIPE)
        os.system(cmd)

        return 
        

    def remoteJob(self, found, ip, cmd, error):
        """ Execute the find cmd on the remote server, the return the dict of the result
        """
        hopcmd = self.__sshHop(cmd, '{}'.format(ip))
        if self.hopStation is not None:
            hopcmd = self.__sshHop(hopcmd, self.hopStation)
        logging.debug("Running command {}".format(hopcmd))
        error[ip] = "searched"
        try:
            result = subprocess.run(hopcmd.split(), universal_newlines=True, stdout=subprocess.PIPE, check=True)
        except Exception as inst:
            error[ip] = inst
            return

        contents = result.stdout.splitlines()
        for r in contents:
            line=dict()
            line['ip']=ip
            # parsing ls -l output
            # line['file']=r
            line['size'] = r.split()[2]
            line['date'] = r.split()[3] + ' ' + r.split()[4]
            line['file'] = r.split()[5]
            logging.debug(line)
            found.append(line)
        # logging.debug("{} done!".format(cmd))
        return
                

    def __sshHop(self, cmd, hop):
        return "ssh {} {}".format(hop, cmd)

    def __readSettings(self):
        with open(QMFNetOp.SETTTINGS_FILE, 'r') as cfg:
            log_cfg = yaml.safe_load(cfg)

        ts = log_cfg.get('STATIONS')
        if ts is not None:
            self.ts = ts.split(',')
        self.hopStation = log_cfg.get('hopStation')
        

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        # logging.basicConfig(level=logging.DEBUG)
        self.hopStation = None
        self.ts = []
        self.__readSettings()

if __name__ == "__main__":
    pass
    # s= QMFNetOp().remote('find /RACKLOG/ -type f -name ZNH02200016.* ' )
    # QMFNetOp().querySn('B98340412317603B')
    # QMFNetOp().scp('192.168.0.81', '/RACKLOG/S2PL_PY/2020/Aug12/ZNH02200016/RUNIN/ZNH02200016.log')
    q = QMFNetOp()
    print(q.hop, q.ts)
