#
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
#
# decorators.py 29-Aug-2011
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
"""
Idea:

    @Bind('inproc://test', zmq.PUB, 'publisher', on_recv='on_recv',
            on_err='on_err', on_send='on_send')
    class ExampleSubscriber(BaseZmqHandler):

        def on_recv(self, msg):
            pass

        def on_err(self, msg):
            pass

        def on_send(self, msg):
            pass

    @Connect('inproc://test', zmq.SUB, 'subscriber', on_recv='print_message',
            opts=[(zmq.SUBSCRIBE, '')])
    class ExamplePublisher(BaseZmqHandler):

        def print_message(self, msg):
            print msg
"""
import zmq

from zerobelt.eventloop import *


__all__ = ['Bind', 'Connect']


class BaseDecorator(object):

    def __init__(self, sockspec, socktype, name=None, on_recv=None,
            on_send=None, on_err=None, opts=[]):
        """
        Initialize the decorator with the *ZeroMQ Socket Type* and the url
        string.
        """
        self.sockspec = sockspec
        self.socktype = socktype
        self.sockname = name
        self.on_recv_name = on_recv
        self.on_send_name = on_send
        self.on_err_name = on_err
        self.opts = opts

    def __call__(self, handler):
        """
        """
        if not hasattr(handler, 'socket_definitions'):
            setattr(handler, 'socket_definitions', {})

        if not hasattr(handler, 'sockets'):
            setattr(handler, 'sockets', {})

        if not self.sockname:
            self.sockname = "%s(%s, %s)" % (handler.__name__, self.sockspec,
                    self.socktype)

        handler.socket_definitions[self.sockname] = self
        return handler


class Bind(BaseDecorator):
    """
    The `Bind` decorator.
    """
    pass


class Connect(BaseDecorator):
    """
    The `Connect` decorator.
    """
    pass
