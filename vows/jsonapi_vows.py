#
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
#
# jsonapi_vows.py 26-Aug-2011
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
from pyvows import Vows, expect
from tornado_pyvows import TornadoContext


from zerobelt import jsonapi

@Vows.batch
class WithTheJsonApi(Vows.Context):

    class Serialization(Vows.Context):

        def topic(self):
            return jsonapi.dumps({'test': 'this'})

        def shouldBeWorking(self, topic):
            expect(topic).to_equal('{"test":"this"}')

    class Deserialization(Vows.Context):

        def topic(self):
            return jsonapi.loads('{"test":"this"}')

        def shouldBeWorking(self, topic):
            expect(topic).to_equal({'test': 'this'})
