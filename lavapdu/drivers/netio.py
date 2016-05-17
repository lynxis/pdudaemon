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
from lavapdu.drivers.apcbase import APCBase
log = logging.getLogger(__name__)


class NETIO(APCBase):
    @classmethod
    def accepts(cls, drivername):
        if drivername == "netio4":
            return True
        return False

    def _pdu_login(self, username, password):
        log.debug("attempting login with username %s, password %s",
                  username, password)

        self.connection.expect("100 HELLO 00000000 - KSHELL")
        self.connection.send("login %s %s\r" % (username, password))

    def _pdu_logout(self):
        self.connection.send("quit\r")
        log.debug("Logging out")

    def _port_interaction(self, command, port_number):
        if command == "on":
            self.connection.send("port %d 1\r")
            self.connection.expect("250 OK")
        elif command == "off":
            self.connection.send("port %d 0\r")
            self.connection.expect("250 OK")
        else:
            log.debug("Unknown command!")
