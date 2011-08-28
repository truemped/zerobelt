#
# Copyright (c) 2011 Daniel Truemper truemped@googlemail.com
#
# setup.py 06-Jul-2011
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# under the License.
#
import os
from setuptools import setup, find_packages

tests_require = ['coverage>=3.4', 'tornado_pyvows']

setup(
    name = "zerobelt",
    version = '0.1.0',
    description = "ZeroMQ Tool Belt",
    author = "Daniel Truemper",
    author_email = "truemped@googlemail.com",
    url = "https://github.com/truemped/zerobelt",
    license = "Apache 2.0",
    long_description = file(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),

    packages = find_packages(),
    include_package_data = True,
    install_requires = [
    ],
    tests_require = tests_require,
    extras_require = {
        'test': tests_require,
        'pyzmq': [
            'pyzmq>=2.1.7',
        ],
        'pyzmq-ctypes': [
            'pyzmq-ctypes>=2.1.3',
        ]
    },
    entry_points = {
        'console_scripts' : [
        ]
    },
    classifiers = [
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.6',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
