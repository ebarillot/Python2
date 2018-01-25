# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import logging
import os
import pprint
import sys
import paramiko as pk
from paramiko import SSHClient
from typing import List, Union, Dict, Any, Callable, NamedTuple, Optional

from EBCommons.prog_helper import call_stack

__author__ = 'Emmanuel Barillot'


def connect_to_host(host,username,password):
    # type: (str, str, str) -> Optional[SSHClient]
    try:
        ssh = pk.SSHClient()
        ssh.load_system_host_keys()
        # la commande précédente va lire le fichier C:\Users\emmanuel_barillot\.ssh\known_hosts
        ssh.set_missing_host_key_policy(pk.AutoAddPolicy())
        ssh.connect(host, username=username, password=password)
        logging.info("Connected to %s" % host)
        return ssh
    except pk.AuthenticationException:
        logging.critical("Authentication failed when connecting to %s" % host)
        return None
    except:
        logging.critical("Could not SSH to %s, waiting for it to start" % host)
        return None


def exec_command(ssh, command):
    # type: (Optional[SSHClient], str) -> List[Any]
    data = []
    # Send the command (non-blocking)
    stdin, stdout, stderr = ssh.exec_command(command)
    stdin.close()
    for line in stdout.read().splitlines():
        data.append(line)
        # logging.debug('line: %s' % line)
    return data
    # autre méthode qui n'arrive pas à tout récupérer
    # # Wait for the command to terminate
    # while not stdout.channel.exit_status_ready():
    #     # Only print data if there is data to read in the channel
    #     if stdout.channel.recv_ready():
    #         rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
    #         if len(rl) > 0:
    #             # Print data from stdout
    #             data += stdout.channel.recv(1024)
    #             # logging.info(stdout.channel.recv(1024),)


def exists_dest_dir(dest_dir):
    # type: (unicode) -> bool
    return os.access(dest_dir, os.F_OK)


def access_dest_dir(dest_dir):
    # type: (unicode) -> bool
    return os.access(dest_dir, os.R_OK|os.W_OK|os.X_OK)


def become_accessible_dest_dir(dest_dir):
    # type: (unicode) -> bool
    access_mode = 0o755
    if os.access(dest_dir, os.F_OK):    # existe
        if os.access(dest_dir, os.R_OK | os.W_OK | os.X_OK):  # existe et accessible
            return True
        else: # existe et non accessible => on essaie de le rendre accessible
            os.chmod(dest_dir, access_mode)
    else: # inexistant => on essaie de le créer
        os.makedirs(dest_dir, access_mode)
    # on vérifie s'il est accesible maintenant
    if os.access(dest_dir, os.R_OK | os.W_OK | os.X_OK): # existe et accessible
        return True
    else:
        return False


def is_accessible_src_dir(ssh,src_dir):
    # type: (Optional[SSHClient], unicode) -> bool
    sftp = ssh.open_sftp()
    sftp_attr = sftp.stat(src_dir)
    if sftp_attr is not None:
        return sftp_attr.st_size > 0
    else:
        return False


def     read_host_src_dir_file_names(ssh, src_dir, how):
    # type: (Optional[SSHClient], str, str) -> List[unicode]
    if how == "ls":
        cmd = b"ls " + src_dir + b"/chgInfnegs*.log"
        logging.info(cmd)
        file_names = exec_command(ssh, cmd)
    else:
        sftp = ssh.open_sftp()
        file_names = sftp.listdir(path=".")
    return file_names


def copy_files_src_to_dest(dest_dir, src_dir, host, host_user, host_password):
    # type: (str, str, str, str, str) -> bool
    def print_file_names(file_names):
        logging.info("""Find: %d files """ % len(file_names))
        for file_name in file_names:
            logging.info("""%s""" % file_name)

    logging.info("Copy files from {}:{} to {}".format(host, src_dir, dest_dir))
    try:
        if become_accessible_dest_dir(dest_dir):
            logging.info("Destination directory {} is accessible".format(dest_dir))
        else:
            raise Exception("Destination directory {} is not accessible, STOP".format(dest_dir))
    except:
        raise
    try:
        ssh = connect_to_host(host, host_user, host_password)
        if not ssh:
            raise Exception("Connexion refused to remote server " + host)
    except:
        raise
    try:
        if is_accessible_src_dir(ssh, src_dir):
            logging.info("Source directory {} is accessible".format(src_dir))
        else:
            raise Exception("source directory {} is not accessible, STOP".format(dest_dir))
    except:
        raise
    file_names = read_host_src_dir_file_names(ssh, src_dir, b"ls")
    file_basenames = [f.split('/')[-1:][0] for f in file_names]
    # print_file_names(file_names2)
    os.chdir(dest_dir)
    sftp = ssh.open_sftp()
    for i in range(len(file_names)):
        message_file = "File {} {}".format(i+1, file_basenames[i])
        already_exists = os.access(file_basenames[i], os.F_OK)
        if already_exists:
            logging.warning(message_file + "  -> already exists")
        else:
            try:
                sftp.get(file_names[i], file_basenames[i])  # remote => local
                logging.info(message_file + "  -> Copy OK")
            except:
                logging.error(message_file + "  -> !! Pb copy file")
    logging.info("Copy done, closing SSH connection")
    ssh.close()
    return True


#####################
# programme principal
#####################
def main(argv):
    host            = br'frtrsifd01'
    host_user       = br'bfrance'
    host_password   = br'bfrance'
    src_dir         = br"/PROSIP_LOGS/BFRANCE"
    work_dir        = b"C:\Users\emmanuel_barillot\Documents\Work"
    dest_dir        = work_dir + br"\Infnegs_logs\2018-01"

    copy_files_src_to_dest(dest_dir, src_dir, host, host_user, host_password)


def main_logging():
    # logger = logging.getLogger('root')
    LOG_FORMAT = "%(asctime)s|%(levelname)-7s|%(name)s|%(filename)s|%(funcName)-20s - %(lineno)s|%(message)s"
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)


##################################
# lancement du programme principal
##################################
if __name__ == "__main__":
    main_logging()
    logging.info(">>>>>>>>>>>>>>>>>>>> Nouvelle série de tests <<<<<<<<<<<<<<<<<<<<")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint("Local path: {}".format(os.environ['HOMEPATH']))
    main(sys.argv)

