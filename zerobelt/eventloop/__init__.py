#
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
#
# __init__.py 26-Aug-2011
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
from .ioloop import *
from .stack_context import *
from .zmqstream import *

def install_ioloop():
    """Install the custom eventloop as the tornado eventloop.
    """
    import tornado.ioloop
    tornado.ioloop.IOLoop = IOLoop

    import tornado.stack_context
    tornado.stack_context.StackContext = StackContext
    tornado.stack_context.NullContext = NullContext
    tornado.stack_context.wrap = wrap
