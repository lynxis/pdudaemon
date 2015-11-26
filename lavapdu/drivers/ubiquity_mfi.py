#! /usr/bin/python

#  Copyright 2015 Alexander Couzens <lynxis@fe80.eu>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import logging
from paramiko import SSHClient
from lavapdu.drivers.driver import PDUDriver
log = logging.getLogger(__name__)

class UbiquityBase(PDUDriver):
    client = None
    # overwrite power_count
    port_count = 0

    def __init__(self, hostname, settings):
        self.hostname = hostname
        log.debug(settings)
        self.settings = settings
        self.sshport = 22
        self.username = "ubnt"
        self.password = "ubnt"
        if "sshport" in settings:
            self.sshport = settings["sshport"]
        if "username" in settings:
            self.username = settings["username"]
        if "password" in settings:
            self.password = settings["password"]
        self.connect()

        super(UbiquityBase, self).__init__()

    def connect(self):
        log.info("Connecting to Ubiquity mfi %s@%s:%d",
                self.username, self.hostname, self.sshport)
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.connect(hostname=self.hostname, port=self.sshport,
                            username=self.username, password=self.password)

    def port_interaction(self, command, port_number):
        log.debug("Running port_interaction from UbiquityBase")
        if port_number > self.port_count:
            raise RuntimeError("We only have ports 1 - %d. %d > maxPorts (%d)"
                    % self.port_count, port_number, self.port_count)

        if command == "on":
            command = "bash -c 'echo 1 > /proc/power/relay%d'" % port_number
        elif command == "off":
            command = "bash -c 'echo 0 > /proc/power/relay%d'" % port_number
        
        self.client.exec_command(command, bufsize=-1, timeout=3)

    def _cleanup(self):
        self.client.close()

    def _bombout(self):
        self.client.close()

    @classmethod
    def accepts(cls, drivername):
        log.debug(drivername)
        return False

class Ubiquity3Port(UbiquityBase):
    port_count = 3
    
    @classmethod
    def accepts(cls, drivername):
        log.debug(drivername)
        if drivername == "ubntmfi3port":
            return True
        return False

class Ubiquity6Port(UbiquityBase):
    port_count = 6
    
    @classmethod
    def accepts(cls, drivername):
        log.debug(drivername)
        if drivername == "ubntmfi6port":
            return True
        return False
