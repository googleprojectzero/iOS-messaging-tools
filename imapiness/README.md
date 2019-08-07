#The Persuit of IMAPiness Fuzzer

Test tool for IMAP clients. Emulates a server and sends back malformed responses.

Written and maintained by Natalie Silvanovich, natashenka@google.com.

#Usage

1) Edit imapiness.py to replace "YOUR CERT" with the location of your server's certs

2) On your remote server, run:

python imapiness.py

3) Set up the test client to use the address of your server as its IMAP server with port 993 and SSL enabled. Set it to query the IMAP server as frequently as possible.

4) Let IMAPiness ensue! 
