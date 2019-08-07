#SMS Simulator for iOS 11.3.1

Simulates SMS deliver PDUs locally on an iOS device

Written and maintained by Natalie Silvanovich, natashenka@google.com.

#Usage

Notes:

- Using this simulator requires a jailbroken device
- Using this simulator requires the device to have a working SIM card that can receive SMS

To set up simulator:

1) Build lib.c by calling:

clang++ -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS12.1.sdk -arch arm64 -dynamiclib lib.c -Wl,-undefined,dynamic_lookup -g -o sim.lib

2) Build sms.m by calling:

clang -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/SDKs/iPhoneOS12.1.sdk -fobjc-arc -arch arm64 -fmodules -framework CoreTelephony sms.m -o sms -Wno-implicit-function-declaration

3) Transfer sim.lib and sms to the device. Sign them with sms.xml entitlements and copy them to user/bin

4) Create a symlink:

ln -s /usr/bin/sim.lib /usr/local/lib/libCTTestUtil.dylib

5) Attach the debugger to CommCenter and set a breakpoint at discardMTSmsOnThisDevice

6) Send a SMS to the device, and wait for it to hit the breakpoint. Print out the value of the register x21

7) Set a breakpoint at CTSimulateSmsReceived and continue in the debugger

8) Run:

sms AAAA

 and wait for the new breakpoint to be hit

9) Run the the following command in the debugger:

expr mycontroller = (void*) PRINTED_X21_VAL

10) You can now simulate sms messages by running:

sms <hexadecimal pdu>

for example:

sms 07911326040000F0040B911346610089F60000208062917314080CC8F71D14969741F977FD07
