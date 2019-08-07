// Copyright 2019 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Whether the serialized outgoing message should be replaced entirely.
var replaceSerializedMessage = false;

// Create the replacement data.
var dataLen = 0x100;
var rawData = new Uint8Array(dataLen);
for (var i = 0; i < dataLen; i++)
    rawData[i] = 0x41;
var buffer = Memory.alloc(dataLen);
buffer.writeByteArray(rawData.buffer);
var replacementData = ObjC.classes.NSData.dataWithBytes_length_(buffer, dataLen);

// Hook the message serialization routine.
var jw_encode_dictionary_addr = Module.getExportByName(null, "JWEncodeDictionary");
send("Hooking JWEncodeDictionary" + jw_encode_dictionary_addr);
Interceptor.attach(jw_encode_dictionary_addr, {
    onEnter: function(args) {
        var dict = ObjC.Object(args[0]);
        if (dict == null) {
            return;
        }

        send(dict.toString())

        var t = dict.objectForKey_("t")
        if (t == null) {
            return;
        }

        if (t == "REPLACEME") {
            // If set to true, the entire outgoing NSData will be replaced with `replacementData`.
            //replaceSerializedMessage = true;

            // Otherwise, can replace single keys here.
            var newDict = ObjC.classes.NSMutableDictionary.dictionaryWithCapacity_(dict.count());
            newDict.setDictionary_(dict);
            newDict.setObject_forKey_("<html><body>BLABLABLA</body></html>", "x");
            args[0] = newDict.handle;

            send("DONE");
        }
    },

    onLeave: function(retval) {
        if (replaceSerializedMessage) {
            retval.replace(replacementData.handle);
            replaceSerializedMessage = false;
        }
    }
});

