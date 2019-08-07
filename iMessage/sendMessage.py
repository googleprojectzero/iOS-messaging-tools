#!/usr/bin/python
#
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import frida
import sys
import subprocess
import time

receiver = "TARGET" # phone number or email

exit = False

def on_message(message, data):
    global exit
    if message['type'] == 'send':
        payload = message['payload']
        if payload == "DONE":
            print("done")
            exit = True
            return
        #print(payload)
    else:
        print(message)


session = frida.attach("imagent")

code = open('injectMessage.js', 'r').read()
script = session.create_script(code);
script.on("message", on_message)
script.load()

# Send a message through apple script. Our hook will detect it and replace it before sending.
subprocess.call(["osascript", "sendMessage.applescript", receiver, "REPLACEME"])

while not exit:
    time.sleep(0.1)
