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
import zmq

from .decorators import *
from .handlers import *


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
