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


// Returns a string representation of an objC object.
function po(p) {
    return ObjC.Object(p).toString();
}

var COMPRESSION_ZLIB = 0x205;
var compression_decode_buffer_addr = Module.getExportByName(null, "compression_decode_buffer");
var compression_decode_buffer = new NativeFunction(compression_decode_buffer_addr, 'ulong', ['pointer', 'ulong', 'pointer', 'ulong', 'pointer', 'int']);

function gunzip(bytes) {
    var input = Memory.alloc(0x10000);
    input.writeByteArray(bytes);
    var output = Memory.alloc(0x10000);
                                                       // Strip header, this function expects "raw" gzip
    var outSize = compression_decode_buffer(output, 0x10000, input.add(10), bytes.length - 10, NULL, COMPRESSION_ZLIB);
    return output.readByteArray(outSize);
}

// Parses an iMessage and returns a string representation of it.
function pm(p) {
    if (p.isNull()) {
        return "";
    }

    // Content is a NSData instance
    var content = ObjC.Object(p);

    var bytes = new Uint8Array(content.bytes().readByteArray(content.length()));
    if (bytes[0] == 0x1f && bytes[1] == 0x8b) {
        // gzip compressed data
        var decompressed = gunzip(bytes);
        var buf = Memory.alloc(decompressed.byteLength);
        buf.writeByteArray(decompressed);
        content = ObjC.classes.NSData.dataWithBytes_length_(buf, decompressed.byteLength);
    }

    var pList = ObjC.classes.NSPropertyListSerialization.propertyListWithData_options_format_error_(content, 0, ObjC.Object(NULL), ObjC.Object(NULL));
    if (pList == null) {
        return content.toString();
    } else {
        return pList.toString();
    }
}

// Offset from macOS 10.14.3
var offsetHandleMessage = 0xe0f9;
var iMessageBase = Module.findBaseAddress('iMessage');
var messageHandlerAddr = iMessageBase.add(offsetHandleMessage);

send("Hooking -[MessageServiceSession handler:incomingMessage:...] @ " + messageHandlerAddr);
Interceptor.attach(messageHandlerAddr, {
    onEnter: function(args) {
        send({message: pm(args[3]), messageID: po(args[5]), toIdentifier: po(args[6]), fromIdentifier: po(args[7])});
    }
});
