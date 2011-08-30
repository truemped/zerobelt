#
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
#
# app_handler_vows.py 30-Aug-2011
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
import zmq

from pyvows import Vows, expect
from tornado_pyvows import TornadoContext

from zerobelt.app import *


@Bind('inproc://test', zmq.PUB)
class TestPublisher(BaseZmqHandler):

    def __init__(self, context=None, io_loop=None):
        super(TestPublisher, self).__init__(context=context, io_loop=io_loop)


@Bind('inproc://test1', zmq.PUB, name='testpublisher1')
class TestPublisher1(BaseZmqHandler):

    def __init__(self, context=None, io_loop=None):
        super(TestPublisher1, self).__init__(context=context, io_loop=io_loop)


@Bind('inproc://test2', zmq.PUB, name='testpublisher2', on_send='print_send')
class TestPublisher2(BaseZmqHandler):

    def __init__(self, context=None, io_loop=None):
        super(TestPublisher2, self).__init__(context=context, io_loop=io_loop)

    def print_send(self, msg):
        print msg


@Bind('inproc://test3', zmq.PUB, name='testpublisher3')
class TestPublisher3(BaseZmqHandler):

    def __init__(self, context=None, io_loop=None):
        super(TestPublisher3, self).__init__(context=context, io_loop=io_loop)


@Connect('inproc://test3', zmq.SUB, name='testsub', on_recv='print_msg',
        opts=[(zmq.SUBSCRIBE, '')])
class TestSubscriber(BaseZmqHandler):

    def __init__(self, context=None, io_loop=None):
        super(TestSubscriber, self).__init__(context=context, io_loop=io_loop)

    def print_msg(self, msg):
        print msg


@Vows.batch
class ZmqHandlers(TornadoContext):

    def topic(self):

        ctx = ZmqContext.instance()

    class ShouldGetInitialized(TornadoContext):

        def topic(self):
            pub1 = TestPublisher(io_loop=self.io_loop)
            pub2 = TestPublisher1(io_loop=self.io_loop)

            return pub1, pub2

        def handler1ShouldHaveASocketAttribute(self, topic):
            pub, _ = topic
            expect(hasattr(pub, 'socket_definitions')).to_be_true()

        def handler2ShouldHaveASocketAttribute(self, topic):
            _, pub = topic
            expect(hasattr(pub, 'socket_definitions')).to_be_true()

        def socketDefinitionsShouldBeUniquePerHandler(self, topic):
            pub1, pub2 = topic
            expect(pub1.socket_definitions).Not.to_equal(pub2.socket_definitions)

        def socketsShouldBeUniquePerHandler(self, topic):
            pub1, pub2 = topic
            expect(pub1.sockets).Not.to_equal(pub2.sockets)

        def gettingTheSocketShouldWork(self, topic):
            pub, _ = topic
            sock, stream = pub.sockets['TestPublisher(inproc://test, 1)']
            expect(pub.get_socket('TestPublisher(inproc://test, 1)')).to_equal(sock)

        def gettingTheStreamShouldWork(self, topic):
            pub, _ = topic
            sock, stream = pub.sockets['TestPublisher(inproc://test, 1)']
            expect(pub.get_stream('TestPublisher(inproc://test, 1)')).to_equal(stream)

    class TheOnSendCallback(TornadoContext):

        def topic(self):
            pub = TestPublisher2(io_loop=self.io_loop)

            def on_send(msg, result):
                self.stop(msg)

            pub.get_stream('testpublisher2').send('test', callback=on_send)

            return self.wait()

        def shouldGetCalledCorrectly(self, topic):
            expect(topic).to_equal((['test'], 0, False))

    class TheOnRecvCallback(TornadoContext):

        def topic(self, context):
            pub = TestPublisher3(context=context, io_loop=self.io_loop)
            sub = TestSubscriber(context=context, io_loop=self.io_loop)

            sub.get_stream('testsub').on_recv(self.stop)
            pub.get_stream('testpublisher3').send('test')

            return self.wait()

        def shouldGetCalledCorrectly(self, topic):
            expect(topic).to_equal(['test'])
