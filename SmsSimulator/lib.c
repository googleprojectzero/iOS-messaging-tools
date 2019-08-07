/*
 * Copyright 2019 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <os/log.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <dispatch/dispatch.h>
#include <unistd.h>

#include <unistd.h>
#include <notify.h>

#define EXPORT __attribute__((visibility("default")))

extern void* _ZN3sms10Controller19simulateSmsReceivedERKNSt3__112basic_stringIcNS1_11char_traitsIcEENS1_9allocatorIcEEEE(void* a, void* b);

char* mycontroller = 0;

EXPORT void CTSimulateSmsReceived(void* a, void* b){
    
    _ZN3sms10Controller19simulateSmsReceivedERKNSt3__112basic_stringIcNS1_11char_traitsIcEENS1_9allocatorIcEEEE(mycontroller, b);
    
}

EXPORT void CTSimulateSmsDeferredMessage(void* a, void* b, void* c, char d){
    
    char* q = (char*) 0x7788990012341567L;
    *q = 7;
    
}


