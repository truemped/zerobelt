#
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
#
# handlers.py 30-Aug-2011
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
from zerobelt.eventloop import IOLoop, ZMQStream
from .app import ZmqContext
from .decorators import *


class BaseZmqHandler(object):

    def __init__(self, context=None, io_loop=None):
        """
        """
        self.context = context or ZmqContext.instance()
        self.io_loop = io_loop or IOLoop.instance()

        for sockname in self.socket_definitions:
            sockdef = self.socket_definitions[sockname]

            if not (isinstance(sockdef, Bind) or isinstance(sockdef, Connect)):
                raise TypeError

            # create the socket
            sock = self.context.socket(sockdef.socktype)

            # set the socket options
            for oname, ovalue in sockdef.opts:
                sock.setsockopt(oname, ovalue)

            # connect or bind
            if isinstance(sockdef, Bind):
                sock.bind(sockdef.sockspec)
            elif isinstance(sockdef, Connect):
                sock.connect(sockdef.sockspec)

            # create the ZMQStream
            stream = ZMQStream(sock, self.io_loop)

            # setup callbacks
            if sockdef.on_recv_name:
                stream.on_recv(getattr(self, sockdef.on_recv_name))
            if sockdef.on_send_name:
                stream.on_send(getattr(self, sockdef.on_send_name))
            if sockdef.on_err_name:
                stream.on_err(getattr(self, sockdef.on_err_name))

            self.sockets[sockname] = sock
            self.streams[sockname] = stream

    def get_socket(self, name):
        """
        Return the socket with the given name.
        """
        return self.sockets[name]

    def get_stream(self, name):
        """
        Return the `ZMQStream` with the given name.
        """
        return self.streams[name]
