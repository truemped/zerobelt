#
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
#
# zmqstream_vows.py 28-Aug-2011
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

from zerobelt.eventloop import install_ioloop, ZMQStream
install_ioloop()

@Vows.batch
class WithAZmqContextAndPublisher(TornadoContext):

    def topic(self):
        env = dict()
        env['ctx'] = zmq.Context()
        env['pub'] = env['ctx'].socket(zmq.PUB)
        env['pub'].bind('inproc://vows/pubsub')
        return env

    class AReceivingZmqStream(TornadoContext):

        def topic(self, env):
            sub = env['ctx'].socket(zmq.SUB)
            sub.setsockopt(zmq.SUBSCRIBE, '')
            sub.connect('inproc://vows/pubsub')
            stream = ZMQStream(sub, self.io_loop)

            def cb(data):
                self.stop(data)
            stream.on_recv(cb)

            env['pub'].send_multipart(["", "This is expected!"])
            return self.wait()

        def shouldGetTheCorrectMessage(self, topic):
            expect(topic).to_equal(["", "This is expected!"])

    class ASendingStream(TornadoContext):

        def topic(self, env):
            sub = env['ctx'].socket(zmq.SUB)
            sub.setsockopt(zmq.SUBSCRIBE, '')
            sub.connect('inproc://vows/pubsub')

            sub_stream = ZMQStream(sub, self.io_loop)
            pub_stream = ZMQStream(env['pub'], self.io_loop)

            def cb(data):
                self.stop(data)
            sub_stream.on_recv(cb)

            pub_stream.send_multipart(["", "This is expected!"])
            return self.wait()

        def shouldSendTheMessageCorrectly(self, topic):
            expect(topic).to_equal(["", "This is expected!"])
