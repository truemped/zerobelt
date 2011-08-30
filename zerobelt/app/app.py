#
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
#
# mainapp.py 29-Aug-2011
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


class ZmqContext(object):

    context = None

    @classmethod
    def initialize(cls, io_threads):
        cls.context = zmq.Context(io_threads)

    @classmethod
    def instance(cls, io_threads=1):
        if not cls.context:
            ZmqContext.initialize(io_threads)
        return cls.context
