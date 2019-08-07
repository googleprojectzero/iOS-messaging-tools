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

#include <unistd.h>
#include <stdlib.h>
#include <notify.h>
#include <CoreFoundation/CFString.h>
#include <CoreFoundation/CFArray.h>
#include <CoreFoundation/CFDictionary.h>
#include <Foundation/NSArray.h>
#include <Foundation/NSString.h>

OS_OBJECT_DECL(xpc_object);
#define XPC_RETURNS_RETAINED OS_OBJECT_RETURNS_RETAINED
typedef xpc_object_t xpc_connection_t;
typedef void (^xpc_handler_t)(xpc_object_t object);
#define XPC_ARRAY_APPEND ((size_t)(-1))
extern XPC_RETURNS_RETAINED xpc_connection_t xpc_connection_create_mach_service(const char *name, dispatch_queue_t _Nullable targetq, uint64_t flags);
extern void xpc_connection_set_event_handler(xpc_connection_t connection, xpc_handler_t handler);
extern void xpc_connection_activate(xpc_connection_t connection);
extern XPC_RETURNS_RETAINED xpc_object_t xpc_connection_send_message_with_reply_sync(xpc_connection_t connection, xpc_object_t message);
extern char *xpc_copy_description(xpc_object_t object);
extern XPC_RETURNS_RETAINED xpc_object_t xpc_dictionary_create(const char * _Nonnull const * _Nullable keys, const xpc_object_t _Nullable * _Nullable values, size_t count);
extern void xpc_dictionary_set_value(xpc_object_t xdict, const char *key, xpc_object_t _Nullable value);
extern void xpc_dictionary_set_string(xpc_object_t xdict, const char *key, const char *val);
extern void xpc_dictionary_set_uint64(xpc_object_t xdict, const char *key, uint64_t value);
extern XPC_RETURNS_RETAINED xpc_object_t xpc_array_create(const xpc_object_t _Nonnull * _Nullable objects, size_t count);
extern void xpc_array_set_int64(xpc_object_t xarray, size_t index, int64_t value);


char* dec2hex(unsigned char* c, int len){
    int i;
    
    char* ret = malloc(len * 2 + 1);
    for (i = 0; i < len; i++)
    {
        sprintf(&ret[i*2], "%02X", c[i]);
    }
    ret[len*2] = 0;
    printf("%s\n", ret);
    return ret;
}


int main(int argc, char** argv){
        
    char* header = argv[1];
    printf("smes %s\n", header);
    char* mes = header;
    xpc_connection_t connection = xpc_connection_create_mach_service("com.apple.commcenter.xpc", NULL, 2);
    xpc_connection_set_event_handler(connection, ^(xpc_object_t object) {
        char *desc = xpc_copy_description(object);

    });
    xpc_connection_activate(connection);
    xpc_object_t message = xpc_dictionary_create(NULL, NULL, 0);
    xpc_dictionary_set_uint64(message, "action", 10);
    xpc_dictionary_set_string(message, "kRequest", "kSimulateSmsReceived");
    xpc_dictionary_set_string(message, "kCTSmsPdu", mes);
     xpc_dictionary_set_string(message, "kCTSmsPdu", mes);
    xpc_dictionary_set_uint64(message, "flags", 0);
    xpc_dictionary_set_uint64(message, "types", 0x7);
    xpc_object_t pids = xpc_array_create(NULL, 0);
    xpc_array_set_int64(pids, XPC_ARRAY_APPEND, getpid());
    xpc_dictionary_set_value(message, "pids", pids);
    xpc_object_t reply = xpc_connection_send_message_with_reply_sync(connection, message);
    char *desc = xpc_copy_description(reply);


}

