#
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
#
# __init__.py 29-Aug-2011
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
This is a little application `Framework` for use with `Tornado` and `ZeroMQ`.

The idea is pretty simple: DRY.

So instead of writing the same socket creation code over and over again
throughout your application, you may simply create classes that inherit from
`BaseZmqHandler` and use the `Bind` or `Connect` decorator like so::

    from zerobelt.app import BaseZmqHandler, Bind, Connect, ZmqContext
    from zerobelt.eventloop import IOLoop

    @Bind('inproc://tmp', zmq.PUB, name='publisher')
    class MyPublisher(BaseZmqHandler):

        def __init__(self, context=None, io_loop=None):
            super(MyPublisher, self).__init__(context=context, io_loop=io_loop)

            self._context = context or ZmqContext.instance()
            self._io_loop = io_loop or IOLoop.instance()

            self.pub = self.get_stream('publisher')

        def important_method_doing_stuff(self):
            # important stuff
            self.pub.send('done')

    @Connect('inproc://tmp', zmq.SUB, name='subscriber',
        opts=[(zmq.SUBSCRIBE, '')], on_recv='log_everything')
    class MySubscriber(BaseZmqHandler):

        def __init__(self, context=None, io_loop=None):
            super(MySubscriber, self).__init__(context=context, io_loop=io_loop)

            self._context = context or ZmqContext.instance()
            self._io_loop = io_loop or IOLoop.instance()

        def log_everything(self, msg):
            log.info(msg)

The sockets and corresponding `ZMQStreams` are created in the `BaseZmqHandler`.
Both decorators allow to set the callbacks for the stream, namely `on_recv`,
`on_err` and `on_send`.

Creating the sockets, binding and connecting them leaves us with the simple
lines::

    if __name__ == '__main__':
        pub = MyPublisher()
        sub = MySubscriber()

        pub.important_method_doing_stuff()

        IOLoop.instance().start()
"""
import zmq

from .decorators import *
from .basehandler import *


class ZmqContext(object):
    """
    A singleton for the `zmq.Context`.
    """

    context = None
    """
    The class level variable storing the context.
    """

    @classmethod
    def initialize(cls, io_threads):
        """
        Initialize the context.

        This method really creates a new `zmq.Context`, so use with care!
        """
        cls.context = zmq.Context(io_threads)

    @classmethod
    def instance(cls, io_threads=1):
        """
        Return the `zmq.Context` and create it, if it has not been created
        before.
        """
        if not cls.context:
            ZmqContext.initialize(io_threads)
        return cls.context

    @classmethod
    def term(cls):
        """
        Terminate the `zmq.Context`.

        First we need to check if all sockets have been closed.
        """
        sockets = []
        map(sockets.extend, BaseDecorator.sockets)

        for sock in sockets:
            print 'closing %s' % sock
            sock.setsockopt(zmq.LINGER, 0)
            sock.close()

        print 'terminating the context'
        ZmqContext.instance().term()
