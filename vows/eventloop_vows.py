#
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
#
# eventloop_vows.py 26-Aug-2011
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
from functools import partial
import time

from pyvows import Vows, expect
from tornado_pyvows import TornadoContext

from zerobelt.eventloop import *


# install the tornado eventloop
install_ioloop()


def time_callback(callback):
    callback(time.time())


@Vows.batch
class WithAnEventloop(TornadoContext):

    class DelayedCallbacks(TornadoContext):

        def topic(self):
            cb = DelayedCallback(partial(time_callback, self.stop), 1000,
                    io_loop=self.io_loop)
            cb.start()
            return (time.time(), self.wait())

        def shouldGetCalled(self, topic):
            t1, t2 = topic
            expect(t2).to_be_numeric()

        def andTheDelayShouldBeAlmostEqual(self, topic):
            t1, t2 = topic
            expect(1.0 < t2-t1 < 1.001).to_be_true()
