#iMessage Tools

Tools for sending and dumping raw iMessage messages

Written and maintained by Samuel Groß, saelo@google.com.

##Usage

These tools require frida, which can be installed from https://frida.re/. The send and dump scripts only work on a Mac, though the target of a sent message can be any device that can receive iMessage. 


To send a message:

1) Edit sendMessage.py to set the receiver to the target device

2) Edit injectMessage.py to contain the message to be sent

3) Send the message by running:

python3 sendMessage.py


To dump incoming messages:

1) In dumpMessages.js, check that the variable offsetHandleMessage is for the correct version of MacOSm and update it if necessary

2) Run the following command:

python3 dumpIncommingMessages.py

Incoming messages will be output into the console as they are received
