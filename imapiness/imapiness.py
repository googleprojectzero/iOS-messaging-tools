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


import random
import socket, ssl
import base64
import time
import sys
import traceback


fetchnum = "1234"
currcmd = ""
fetcht = 0
valid_resps = []
valid_types = []
squares = []
maxtimes = 10
comnum = 0

def anotherresponse():
	return random.choice(valid_resps)

def anotherparam():
	return random.choice(valid_types)()

def takechance():
	r = random.randrange(0, 10)
	if(r == 7):
		return True
	else:
		return False





def rand_string_nospecial():
	p = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890.,/.!@#$%^&*"
	l  = random.randrange(0, 248)
	s = ""
	for i in range(0, l):
		lp = len(p)
		j = random.randrange(0, lp)
		s = s + p[j:j+1]
	return s

def quoted_string():
	l  = random.randrange(0, 248)
	s = ""
	for i in range(0, l):
		c = chr(random.randrange(0, 256))
		if c == '\"':
			s = s + "\\\""
		else:
			s = s + c
	return s

def rand_string():
	q = random.randrange(0, 5)
	if q == 1:
		l  = random.randrange(0, 248)
		s = ""
		for i in range(0, l):
			c = chr(random.randrange(0, 256))
			if (c== '\r')|(c== '\n'):
				s = s +""
			else: 
				s = s + c 
		return s
	else:
		return rand_string_nospecial()


def rand_string_for_literal():
	q = random.randrange(0, 5)
	if q == 1:
		l  = random.randrange(0, 248)
		s = ""
		for i in range(0, l):
			s = s + chr(random.randrange(0, 256))
		return s
	else:
		return rand_string_nospecial()

class StringLiteral:

    def generate(self, suggestions=[]):
	if takechance():
		return anotherparam().generate()
        s = rand_string_for_literal()
	l = len(s)
	return "{" + str(l) + "}\r\n" + s

class QuotedString:

    def generate(self, suggestions=[]):
	if takechance():
		return anotherparam().generate()
	
	if len(suggestions)==0 or takechance(): 
        	s = quoted_string()
		l = len(s)
	else:
		s = random.choice(suggestions)
	return "\"" + s + "\""

class Atom:

    def generate(self, suggestions=[]):
	if takechance():
		return anotherparam().generate()
        s = rand_string_nospecial()
	l = len(s)
	return s

class Number:


    def generate(self, suggestions=[]):
	if takechance():
		return anotherparam().generate()
        n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
	q = random.randrange(0, 10)
	if q == 1:
		return Atom().generate()
	if q == 2:
		s = ""
		l = random.randrange(0, 1000)
		for i in range(0, l):
			s = s + str(random.choice(n))
		return s	
	else:
		s = ""
		l = random.randrange(0, 32)
		for i in range(0, l):
			s = s + str(random.choice(n))
		return s


class nil:

    def generate(self, suggestions=[]):
	return "NIL"

def any_str():
	l = random.randrange(0, 10)
	if l == 0:
		return StringLiteral().generate()
	if l == 1:
		return QuotedString().generate()
	if l == 2:
		return nil().generate()
	else:
		return Atom().generate()


class Nothing:
	def generate(self, suggestions=[]):
		return ""

class AnyString:

    def generate(self, suggestions=[]):
	if takechance():
		return anotherparam().generate()
	if len(suggestions) == 0:
		return any_str()
	else:
		if takechance():
			return any_str()
		else:
			return random.choice(suggestions) 

class StringArray:

    def generate(self, suggestions=[]):
	l = random.randrange(0, maxtimes)
	s = "("
	for i in range(0, l):
		if suggestions and (len(suggestions)!=0) and (takechance()==False):
			s = s+ random.choice(suggestions)
		else:
			s = s + any_str()
		if i < (l -1):
			s = s + " "
	s = s + ")"        
	return s

class StringPairArray:

    def generate(self, suggestions=[]):
	if takechance():
		return anotherparam().generate()
	l = random.randrange(0, maxtimes)
	s = "("
	for i in range(0, l):
		if suggestions and (len(suggestions)!=0) and (takechance()==False):
			p = random.choice(suggestions)
			s = s + "\"" + p[0] + "\" \"" + p[1] + "\""
		elif suggestions and (len(suggestions)!=0) and (takechance()==False):
			p = random.choice(suggestions)
			s = s + "\"" + p[0] + " " + QuotedString().generate()
		else:
			s = s + AnyString().generate() + " " + AnyString().generate()
		if i < (l -1):
			s = s + " "
	s = s + ")"        
	return s

class StringNumPairArray:

    def generate(self, suggestions=[]):
	if takechance():
		return anotherparam().generate()
	l = random.randrange(0, maxtimes)
	s = "("
	for i in range(0, l):
		if suggestions and (len(suggestions)!=0) and (takechance()==False):
			p = random.choice(suggestions)
			s = s + "\"" + p + "\" \"" + Number().generate() + "\""
		else:
			s = s + AnyString().generate() + " " + AnyString().generate()
		if i < (l -1):
			s = s + " "
	s = s + ")"        
	return s

class NamespaceArray:

    def generate(self, suggestions=[]):
	if takechance():
		return anotherparam().generate()
	s = "(("

	s = s + any_str()

	s = s + " "
	s = s + any_str()
	s = s + "))"        
	return s

class MixedArray:

    def __init__(self):
	self.recursioncount = 10;

    def generate(self, suggestions=[]):
	if takechance():
		return anotherparam().generate()
	l = random.randrange(0, 20)
	s = "("
	for i in range(0, l):
		if takechance():
			if self.recursioncount > 0:
				self.recursioncount = self.recursioncount - 1
				s = s + self.generate(suggestions)
		elif takechance():
				s = s + Number().generate()
		else:
			if len(suggestions)==0 or takechance():
				if takechance():
					s = s + AnyString().generate()
				else:
					s = s + QuotedString().generate()
			else:
				s = s + "\"" + random.choice(suggestions) + "\""
		if i < l - 1:
			s = s + " "
        s = s + ")"
	return s

class QuotaArray:

    def generate(self, suggestions=[]):
	if takechance():
		return anotherparam().generate()
	s = "("
	if takechance():
		s = s + any_str() + " "
	else:
		s = s + "STORAGE "

	s = s + Number().generate() + " " + Number().generate() + ")"       
	return s

class QuotedStringArray:


    def generate(self, suggestions=[]):
	if takechance():
		return anotherparam().generate()
	l = random.randrange(0, maxtimes)
	s = "("
	for i in range(0, l):
		if suggestions and (len(suggestions)!=0) and (takechance()==False):
			s = s+ random.choice(suggestions)
		else:
			s = s + QuotedString().generate([])
		if i < (l -1):
			s = s + " "
		s = s + ")"        
	return s

class responseparameter:
	def __init__(self, response, multiple):
		self.response = response
		self.multiple = multiple



class parameter:
	def __init__(self, ptype, multiple, rightvals, rightvals_gen=[]):
		self.ptype = ptype
		self.multiple = multiple
		self.rightvals = rightvals
		self.rightvals_gen = rightvals_gen

	def generate(self, suggestions=[]):
		s = ""
		q = self.ptype()
		return q.generate(suggestions)


class squareparam:
	def __init__(self, name, paramarray):
		self.name = name
		self.paramarray = paramarray





def add_square(resp):
	if takechance():
		sq = random.choice(squares)
		s = "[" + sq.name + " "
		for item in sq.paramarray:
			times = 1			
			if item.multiple | takechance():
				times = times + random.randrange(0, maxtimes)
			for u in range(0, times):

				if (takechance() == False) & (len(item.rightvals)!=0):
					s = s + random.choice(item.rightvals)
			
				elif takechance():
					s = s + anotherparam().generate()		
				else:
					s = s + item.generate()
				s = s + " "
		s = s[:len(s)-1] + "] "
		return s
	if resp.square:
		sq = resp.recommended_square
		s = "[" + sq.name + " "
		for item in sq.paramarray:
			times = 1
			if item.multiple | takechance():
				times = times + random.randrange(0, maxtimes)
			for u in range(0, times):

				if (takechance() == False) & (len(item.rightvals)!=0):
					s = s + random.choice(item.rightvals)
			
				elif takechance():
					s = s + anotherparam().generate([])		
				else:
					s = s + item.generate()
				if u+1 != times:
					s = s + " "
		s = s + "] "
		return s
	else:
		return ""
			 

def numbered_command(resp):
	s = Number().generate() + " " + resp.command + "\r\n"
	return s
		
def gen_from_array(resp):
	s = resp.command + " "
	s = s + add_square(resp) 
	for item in resp.params:
		times = 1
		if item.multiple | takechance():
			times = times + random.randrange(0, maxtimes)
		for u in range(0, times):

			if (takechance() == False) & (len(item.rightvals)!=0):
				s = s + random.choice(item.rightvals)
			
			elif takechance():
				s = s + anotherparam().generate(item.rightvals_gen)		
			else:
				s = s + item.generate(item.rightvals_gen)
			if u+1 < times:
				s = s + " "
		s = s + " "
	s = s[:len(s)-1]			
				 
	return s + "\r\n"
		
	
			

class capability_resp:
	def __init__(self):
		self.command = "CAPABILITY"
		p = parameter(Atom, True, ["IMAP4rev1", "LITERAL+", "LITERAL-", "UIDPLUS", "METADATA", "QUOTA", "CHILDREN", "AUTH=DIGEST-MD5", "XYMHIGHESTMODSEQ", "SASL-IR", "CONDSTORE", "ESEARCH",  "XLIST", "UNSELECT", "QUOTA", "XAPPLEPUSHSERVICE"])
		self.params = [p]
		self.square = False

	def generate(self):
		return gen_from_array(self)


class login_resp:
	def __init__(self):
		self.command = "OK"
		self.params = []
		self.square = True
		p = parameter(Atom, True, ["IMAP4rev1", "LITERAL+", "LITERAL-", "UIDPLUS", "METADATA", "QUOTA", "CHILDREN", "AUTH=DIGEST-MD5", "XYMHIGHESTMODSEQ", "SASL-IR", "CONDSTORE", "ESEARCH", "XLIST", "UNSELECT", "QUOTA", "XAPPLEPUSHSERVICE"])
		s = squareparam("CAPABILITY", [p])
		self.recommended_square = s

	def generate(self):
		return gen_from_array(self)

class ok_resp:
	def __init__(self):
		self.command = "OK"
		self.params = []
		self.square = False

	def generate(self):
		return gen_from_array(self)

class bad_resp:
	def __init__(self):
		self.command = "BAD"
		self.params = []
		self.square = False

	def generate(self):
		return gen_from_array(self)

class no_resp:
	def __init__(self):
		self.command = "NO"
		self.params = []
		self.square = False

	def generate(self):
		return gen_from_array(self)

class namespace_resp:
	def __init__(self):
		self.command = "NAMESPACE"
		self.params = [parameter(NamespaceArray, True, [])]
		self.square = False

	def generate(self):
		return gen_from_array(self)

class quota_resp:
	def __init__(self):
		self.command = "QUOTA"
		self.params = [parameter(QuotaArray, True, [])]
		self.square = False

	def generate(self):
		return gen_from_array(self)

class quotaroot_resp:
	def __init__(self):
		self.command = "QUOTAROOT"
		p = parameter(Atom, True, ["INBOX", "Inbox", "Trash", "Greetings"])
		self.params = [p]
		self.square = False

	def generate(self):
		return gen_from_array(self)

class flags_resp:
	def __init__(self):
		self.command = "FLAGS"
		self.params = [parameter(StringArray, False,[], ["\\Seen", "\\Answered", "\\Flagged", "\\Deleted", "\\Draft", "\\Recent", "\\Noinferiors", "\\Noselect", "\\Marked", "\\Unmarked", "\\HasChildren", "\\HasNoChildren", "\\NonExistent"])]
		self.square = False

	def generate(self):
		return gen_from_array(self)

class id_resp:
	def __init__(self):
		self.command = "ID"
		self.params = [parameter(QuotedStringArray, False, [])]
		self.square = False

	def generate(self):
		return gen_from_array(self)

class stock_select_resp:
	def __init__(self):
		self.command = "ID"
	def generate(self):
		return "32 EXISTS\r\n* 1 RECENT\r\n* OK [UNSEEN 1] Message 12 is first unseen\r\n* OK [UIDNEXT "+str(random.randrange(0, 10000))+"] Predicted next UID\r\n* FLAGS (\\Answered \\Flagged \\Deleted \\Seen \\Draft {10}\r\n0123456789)\r\n* OK [UIDVALIDITY "+str(random.randrange(0, 10000))+"]\r\n* OK [PERMANENTFLAGS (\\Deleted \\Seen \\Answered \\Draft \\*)] Limited\r\n* OK [READ-WRITE] SELECT completed\r\n"

class exists_resp:
	def __init__(self):
		self.command = "EXISTS"
		self.params = [parameter(Number, False, [])]
		self.square = False

	def generate(self):
		return numbered_command(self)

class recent_resp:
	def __init__(self):
		self.command = "RECENT"
		self.params = [parameter(Number, False, [])]
		self.square = False

	def generate(self):
		return numbered_command(self)

class permanent_flags_resp:
	def __init__(self):
		self.command = "OK"
		self.params = []
		self.square = True
		p = parameter(Atom, True, ["\Seen", "\Answered", "\Flagged", "\Deleted", "\Draft", "\Recent"])
		s = squareparam("CAPABILITY", [p])
		self.recommended_square = s

	def generate(self):
		return gen_from_array(self)

class unseen_resp:
	def __init__(self):
		self.command = "OK"
		self.params = []
		self.square = True
		p = parameter(Number, False, [])
		s = squareparam("UNSEEN", [p])
		self.recommended_square = s

	def generate(self):
		return gen_from_array(self)

class uidvalidity_resp:
	def __init__(self):
		self.command = "OK"
		self.params = []
		self.square = True
		p = parameter(Number, False, [])
		s = squareparam("UIDVALIDITY", [p])
		self.recommended_square = s

	def generate(self):
		return gen_from_array(self)

class uidnext_resp:
	def __init__(self):
		self.command = "OK"
		self.params = []
		self.square = True
		p = parameter(Number, False, [])
		s = squareparam("UIDNEXT", [p])
		self.recommended_square = s

	def generate(self):
		return gen_from_array(self)

class list_resp:
	def __init__(self):
		self.command = "LIST"
		self.params = [parameter(StringArray, False, [], ["\Seen", "\Answered", "\Flagged", "\Deleted", "\Draft", "\Recent"]), parameter(QuotedString, False, ["\\"]), parameter(QuotedString, False, [])]
		self.square = False

	def generate(self):
		return gen_from_array(self)

class search_resp:
	def __init__(self):
		self.command = "SEARCH"
		self.params = [parameter(Number, True, [])]
		self.square = False

	def generate(self):
		return gen_from_array(self)

class status_resp:
	def __init__(self):
		self.command = "STATUS"
		self.params = [parameter(AnyString, False, ["INBOX"]), parameter(StringNumPairArray, False, ["MESSAGES", "RECENT", "UNSEEN", "UIDNEXT", "UIDVALIDITY"])]
		self.square = False

	def generate(self):
		return gen_from_array(self)


class fetchtype:
	def __init__(self, name, params):
		self.name = name
		self.params = params

	def generate(self):
		s = self.name + " "
		for item in self.params:
			if takechance():
				s = s + anotherparam().generate(item.rightvals_gen)		
			else:
				s = s + item.generate(item.rightvals_gen)
			s = s + " "
		s = s[:len(s)-1]
		return s

class bodystructfetchtype:
	def __init__(self):
		self.name = "BODYSTRUCTURE"

	def generate_mime(self):
		entries = random.randrange(1, 3)
		s = ""		
		for i in range(0, entries):
			s = s + "(" + QuotedString().generate(["AUDIO", "AUDIO", "AUDIO", "AUDIO", "AUDIO", "AUDIO", "AUDIO", "AUDIO", "AUDIO", "AUDIO", "AUDIO", "AUDIO", "AUDIO", "AUDIO", "MULTIPART"]) + " " + QuotedString().generate(["AMR"]) + " "
			s = s + StringPairArray().generate([["name", "test.amr"], ["charset", "UTF-8"]]) + " "
			s = s + QuotedString().generate() + " " # email
			s = s + QuotedString().generate() + " " # subject
			s = s + QuotedString().generate(["BASE64", "7BIT", ]) + " " # encoding
			s = s + Number().generate() + " "
			s = s + Number().generate() + " "
			if takechance():
				s = s + StringPairArray().generate([["name", "test.amr"], ["charset", "UTF-8"]]) + " " # body parameters
				if takechance():
					s = s + StringPairArray().generate([["attachment", "(\"filename\" \"test.amr\")"], ["charset", "UTF-8"]]) + " " # disposition
					if takechance():
						s = s + StringArray().generate() + " " #lang
						if takechance():
							s = s + StringArray().generate() + " " #uri				
			s = s[:len(s)-1] + ")"
		s = "(" + s + " \"VOICE-MESSAGE\""
		return s

	def generate(self):
		
		s = self.name + " " + self.generate_mime() + " "
		s = s + StringPairArray().generate([["name", "test.amr"], ["charset", "UTF-8"]]) + " " # body parameters
		if takechance():
			s = s + StringPairArray().generate([["attachment", "(\"filename\" \"test.amr\")"], ["charset", "UTF-8"]]) + " " # disposition
			if takechance():
				s = s + StringArray().generate() + " " #lang
				if takechance():
					s = s + StringArray().generate() + " " #uri
		s = s + ")"			
		return s




class bodytextfetchtype:
	def __init__(self):
		self.name = "BODY"
		self.sectionlist = ["HEADER", "HEADER.FIELDS", "HEADER.FIELDS.NOT", "MIME", "TEXT", ""]

	def generate(self):
		s = self.name + "[TEXT]"
		
		if takechance():
			s = s + "<" + Number().generate() + ">"
		s = s + " "

		s = s + StringLiteral().generate()
		
		return s

class bodyheaderfetchtype:
	def __init__(self):
		self.name = "BODY"
		self.sectionlist = ["HEADER", "HEADER.FIELDS", "HEADER.FIELDS.NOT", "MIME", "TEXT", ""]
		self.myheader = "X-AppleVM-Message-Version: 1.0\r\nReturn-Path: <>\r\nReceived: from vm-asu5.WAVMS012.vms.eng.t-mobile.com (10.182.7.55) by MIPS1.WAVMS012.vms.eng.t-mobile.com (Multi Media IP Store)\r\n                    id 5C3F14B301247B64 for 16505551234@vms.eng.t-mobile.com; Tue, 12 Feb 2019 10:03:19 -0800\r\nDate: Tue, 12 Feb 2019 10:03:19 -0800 (PST)\r\nFrom: VOICE=+6505551237@vms.eng.t-mobile.com\r\nReply-To: 6505551237 <non-mail-user@vms.eng.t-mobile.com>\r\nTo: VOICE=+16505551234@vms.eng.t-mobile.com\r\nMessage-ID: <14206403.48dasdasdasdasdas577421.1549994599138.JavaMail.vxvuser@vm-asu5.WAVMS012.vms.eng.t-mobile.com>\r\nSubject: Voice message\r\nMIME-Version: 1.0 (Voice Version 2.0)\r\nContent-Type: multipart/voice-message;\r\n boundary=\"----=_Part_48164806_21700900.1549568140966\"\r\nMessage-Context: voice-message\r\nX-Voicemail:  \r\nContent-Duration: 31\r\nX-Priority: 3\r\nX-CNS-UID: 10043648-106\r\nX-Mailer: CNS-VxV(4.3.7)\r\nX-CNS-Originator-Phone-Number: 6505551237\r\nX-CNS-Accessed-Phone-Type: MainPhone\r\nX-CNS-Accessed-Phone: 16505551234\r\nImportance: Normal\r\nX-CNS-Message-Context: voice-message\r\nX-CNS-Media-Size: total=1msgs; voice=1msgs; d_voice=31sec;\r\n\r\n"
	
	def generate_header(self):
		h = self.myheader.split("\r\n")
		l = []
		for item in h:
			if len(item) == 0:
				continue
			c = item.find(":")
			if (c == -1) or item[0] == " ":
				l[len(l)-1][1] = l[len(l)-1][1] + "\r\n" + item
				continue
			n = item[:c]
			v = item[c+1:]
			l.append([n, v])
		times = random.randrange(0, maxtimes)
		for i in range(0, times):
			q = random.randrange(0, 5)
			if q == 0:
				ind = random.randrange(0, len(l))
				item = l[ind]
				l[ind][0] = rand_string()
			if q == 1:
				ind = random.randrange(0, len(l))
				item = l[ind]
				l[ind][1] = rand_string()
			if q == 2:
				ind = random.randrange(0, len(l))
				item = l[ind]
				icopy = [item[0], item[1]]
				t = random.randrange(0, maxtimes)	
				for j in range(0, t):
					icopy[1] = rand_string()
					l.append(icopy)	
			if q == 3:
				ind = random.randrange(0, len(l)-1)
				item = l[ind]
				value = l[ind][1]
				ind = random.randrange(0, len(l))
				l[ind][1] = value[ind:] + chr(random.randrange(0, 256)) + value[:ind+1]
			if q == 4:
				ind = random.randrange(0, len(l)-1)
				item = l[ind]
				value = l[ind][1]
				ind = random.randrange(0, len(l))
				l[ind][1] = value[ind:] + rand_string() + value[:ind+1]
		random.shuffle(l)
		s = ""
		
		for item in l:
			s = s + item[0] + ": " + item[1] + "\r\n"
		s = s + "\r\n"
		if takechance():
			ind = random.randrange(0, len(l))
			s = s[ind:] + rand_string() + s[ind:]
		return s 

	def generate(self):
		s = self.name + "[HEADER]"
		
		if takechance():
			s = s + "<" + Number().generate() + ">"
		s = s + " "
		h = self.generate_header()
		s = s + "{" + str(len(h)) + "}\r\n" + h 
		
		return s

class bodyfetchtype:
	def __init__(self):
		self.name = "BODY"
		self.sectionlist = ["HEADER", "HEADER.FIELDS", "HEADER.FIELDS.NOT", "MIME", "TEXT", ""]

	def generate(self):
		s = self.name + "["
		if takechance():
			if takechance():
				s = s + AnyString().generate()
			elif takechance():
				s = s + Number().generate()
			else:
				s = s + Atom().generate()
		else:
			s = s + random.choice(self.sectionlist)
		s = s + "]"
		
		if takechance():
			s = s + "<" + Number().generate() + ">"
		s = s + " "

		s = s + StringLiteral().generate()
		
		return s

class fetch_resp:
	def __init__(self):
		self.command = "FETCH"
		self.params = [
			fetchtype("INTERNALDATE", [parameter(AnyString, False, [])]),
			bodyfetchtype(), 
			fetchtype("BODY", [parameter(MixedArray, False, ["7BIT", "TEXT", "PLAIN", "AUDIO", "AMF", "CHARSET", "NIL", "BASE64", "MIXED"])]),
			fetchtype("BODYSTRUCTURE", [parameter(MixedArray, False, ["7BIT", "TEXT", "PLAIN", "AUDIO", "AMF", "CHARSET", "NIL", "BASE64", "MIXED"]), parameter(MixedArray, False, []), parameter(MixedArray, False, []), parameter(StringArray, False, []), parameter(AnyString, False, [])]), 
			fetchtype("BODYSTRUCTURE", [parameter(MixedArray, False, ["7BIT", "TEXT", "PLAIN", "AUDIO", "AMF", "CHARSET", "NIL", "BASE64", "MIXED"]), parameter(AnyString, False, []), parameter(AnyString, False, []), parameter(AnyString, False, []), parameter(AnyString, False, []), parameter(AnyString, False, []), parameter(AnyString, False, []), parameter(Number, False, [])]), 
			fetchtype("ENVELOPE", [parameter(MixedArray, False, [])]), 
			fetchtype("ENVELOPE", [parameter(StringArray, False, [])]),
			fetchtype("FLAGS", [parameter(StringArray, False, ["\Seen", "\Answered", "\Flagged", "\Deleted", "\Draft", "\Recent"])]), 
			fetchtype("RFC822", [parameter(StringLiteral, False, [])]), 
			fetchtype("RFC822.HEADER", [parameter(StringLiteral, False, [])]), 
			fetchtype("RFC822.TEXT", [parameter(StringLiteral, False, [])]), 
			fetchtype("RFC822.SIZE", [parameter(Number, False, [])]), 
			fetchtype("UID", [parameter(Number, False, [])]),
			bodyheaderfetchtype(),
			bodystructfetchtype()
			]
		self.square = False


	def generate(self):
		global fetcht
		global fetchnum
		global currcmd
		s = fetchnum + " FETCH (UID " + fetchnum + " "
		l = random.randrange(0, 3)
		if currcmd.find("BODY.PEEK[HEADER]") != -1 or currcmd.find("BODY[HEADER]") != -1:
			s = s + bodyheaderfetchtype().generate() 
		if currcmd.find("FLAGS") != -1:
			s = s + fetchtype("FLAGS", [parameter(StringArray, False, ["\Seen", "\Answered", "\Flagged", "\Deleted", "\Draft", "\Recent"])]).generate() + " "
		if currcmd.find("BODYSTRUCTURE"):
			types = [bodystructfetchtype(), fetchtype("BODYSTRUCTURE", [parameter(MixedArray, False, ["7BIT", "TEXT", "PLAIN", "AUDIO", "AMF", "CHARSET", "NIL", "BASE64", "MIXED"]), parameter(MixedArray, False, []), parameter(MixedArray, False, []), parameter(StringArray, False, []), parameter(AnyString, False, [])]), 
			fetchtype("BODYSTRUCTURE", [parameter(MixedArray, False, ["7BIT", "TEXT", "PLAIN", "AUDIO", "AMF", "CHARSET", "NIL", "BASE64", "MIXED"]), parameter(AnyString, False, [])])]
			t = random.choice(types)
			s = s + " " + t.generate() + " "
		if currcmd.find("BODY.PEEK[TEXT") != -1 or currcmd.find("BODY[TEXT]") != -1:
			s = s + bodytextfetchtype().generate() 
		if l==0:
			s = s[:len(s)-1]
		for i in range(0, l):
			s = s + random.choice(self.params).generate()
			if i < l - 1:
				s = s + " "
		s = s + ")\r\n"

		return s

class capability:
	def __init__(self):
		self.command = "CAPABILITY"
		rr = capability_resp()
		self.responses=[responseparameter(rr, False), responseparameter(ok_resp(), False)]

class id:
	def __init__(self):
		self.command = "ID"
		rr = id_resp()
		self.responses=[responseparameter(rr, False), responseparameter(ok_resp(), False)]


class login:
	def __init__(self):
		self.command = "LOGIN"
		rr = login_resp()
		self.responses=[responseparameter(rr, False)]

class select:
	def __init__(self):
		self.command = "SELECT"

		self.responses = [responseparameter(stock_select_resp(), False), responseparameter(ok_resp(), False)]

class list:
	def __init__(self):
		self.command = "LIST"
		self.responses=[responseparameter(list_resp(), False), responseparameter(ok_resp(), False)]

class search:
	def __init__(self):
		self.command = "SEARCH"
		self.responses=[responseparameter(search_resp(), False), responseparameter(ok_resp(), False)]

class create:
	def __init__(self):
		self.command = "CREATE"
		self.responses=[responseparameter(ok_resp(), False)]

class subscribe:
	def __init__(self):
		self.command = "SUBSCRIBE"
		self.responses=[responseparameter(ok_resp(), False)]

class status:
	def __init__(self):
		self.command = "STATUS"
		self.responses=[responseparameter(status_resp(), False), responseparameter(ok_resp(), False)]

class noop:
	def __init__(self):
		self.command = "NOOP"
		self.responses=[responseparameter(ok_resp(), False)]

class getquotaroot:
	def __init__(self):
		self.command = "GETQUOTAROOT"
		self.responses=[responseparameter(quotaroot_resp(), True), responseparameter(quota_resp(), True), responseparameter(ok_resp(), False)]

class fetch:
	def __init__(self):
		self.command = "FETCH"
		self.responses=[responseparameter(fetch_resp(), False), responseparameter(ok_resp(), False)]

class namespace:
	def __init__(self):
		self.command = "NAMESPACE"
		self.responses=[responseparameter(namespace_resp(), False), responseparameter(ok_resp(), False)]



def fuzzmore(s):

	if takechance():
		ll = random.randrange(0, len(s)-1)
		s = s[:ll] + chr(random.randrange(0, 256))+ s[ll+1:]
	return s

def rearrange(l):
	n = len(l)
	if(n < 2):
		return l
	last = l[n-1]
	t = l[0:n-1]
	random.shuffle(t)
	t.append(last)
	return t

def addtag(l, tag):
	if len(l) < 2:
		 return tag + " " + l[0]
	o = ""
	for i in range(0, len(l) - 1):
		o = o + "* " + l[i]
	o = o + tag + l[len(l)-1]
	return o


command_array = [capability(), login(), select(), search(), create(), noop(), subscribe(), list(), getquotaroot(), fetch(), status()]

valid_resps = [capability_resp(), uidnext_resp(), uidvalidity_resp(), unseen_resp(), permanent_flags_resp(), recent_resp(), exists_resp(), flags_resp(), list_resp(), search_resp(), quota_resp(), quotaroot_resp(), fetch_resp(), bad_resp(), no_resp(), status_resp()]

valid_types = [Atom, StringLiteral, nil, QuotedString, StringArray, MixedArray, Number, NamespaceArray, StringNumPairArray, Nothing]

def add_squares():
	p = parameter(Atom, True, ["IMAP4rev1", "LITERAL+", "LITERAL-", "UIDPLUS", "METADATA", "QUOTA", "CHILDREN", "AUTH=DIGEST-MD5", "XYMHIGHESTMODSEQ", "SASL-IR", "CONDSTORE", "ESEARCH", "COMPRESS=DEFLATE", "XLIST", "UNSELECT", "QUOTA", "XAPPLEPUSHSERVICE"])
	squares.append(squareparam("CAPABILITY", [p]))
	p = parameter(Number, False, [])
	s = squareparam("UIDVALIDITY", [p])
	squares.append(s)
	p = parameter(Number, False, [])
	s = squareparam("UIDNEXT", [p])
	squares.append(s)
	p = parameter(Number, False, [])
	s = squareparam("UNSEEN", [p])
	squares.append(s)
	p = parameter(Atom, False, [])
	s = squareparam("ALERT", [p])
	squares.append(s)
	s = squareparam("EXPUNGEISSUED", [])
	squares.append(s)
	s = squareparam("UNAVAILABLE", [])
	squares.append(s)
	s = squareparam("AUTHENTICATIONFAILED", [])
	squares.append(s)
	s = squareparam("AUTHORIZATIONFAILED", [])
	squares.append(s)
	s = squareparam("OVERQUOTA", [])
	squares.append(s)
	s = squareparam("ALREADYEXISTS", [])
	squares.append(s)
	s = squareparam("EXPIRED", [])
	squares.append(s)
	s = squareparam("PRIVACYREQUIRED", [])
	squares.append(s)
	s = squareparam("CONTACTADMIN", [])
	squares.append(s)
	s = squareparam("NONEXISTANT", [])
	squares.append(s)
	s = squareparam("NOPERM", [])
	squares.append(s)
	s = squareparam("INUSE", [])
	squares.append(s)
	s = squareparam("SERVERBUG", [])
	squares.append(s)
	s = squareparam("CANNOT", [])
	squares.append(s)
	s = squareparam("LIMIT", [])
	squares.append(s)
	s = squareparam("OVERQUOTA", [])
	squares.append(s)
	s = squareparam("CORRUPTION", [])
	squares.append(s)
	s = squareparam("NEWNAME", [])
	squares.append(s)
	s = squareparam("TRYCREATE", [])
	squares.append(s)
	s = squareparam("READ-ONLY", [])
	squares.append(s)
	s = squareparam("READWRITE", [])
	squares.append(s)
	s = squareparam("HIGHESTMODSEQ", [])
	squares.append(s)
	s = squareparam("NOMODSEQ", [])
	squares.append(s)
	p = parameter(MixedArray, False, [])
	s = squareparam("BADCHARSET", [p])
	squares.append(s)
	p = parameter(Number, False, [])
	s = squareparam("APPENDUID", [p, p])
	squares.append(s)


def deal_with_client(connstream):
    global fetchnum
    global currcmd
    global comnum
    print("here");
    connstream.send("* OK Persuit of IMAPiness serving IMAP realness\r\n")
    data = "test"
    print("new socket");
    while data:
        print "read"
        data = connstream.recv(1000)
	print data
	found = False
	for item in command_array:
		if data.find(" " + item.command) != -1:
			found = True			
			tag = data[:data.find(item.command)]
			o = ""
			l = []
			currcmd = data
			if(data.find("FETCH") != -1):
				fetchnum = data[data.find("FETCH")+6:]
				fetchnum = fetchnum[:fetchnum.find(" ")]
			if takechance():
				num = random.randrange(0, 10)
				for i in range(0, num):
					item1 = anotherresponse()
					l.append(item1.generate())

			for resp in item.responses:
				r = resp.response
				m = resp.multiple
				times = 1
				if m | takechance():
					times = times + random.randrange(0, maxtimes)
				for i in range(0, times):
					#o = o + r.command + " "
					l.append(r.generate())

			l = rearrange(l)
			o = addtag(l, tag)
				
			o = fuzzmore(o)
			f = open("lastcommand"+str(comnum)+".txt", 'wb')
			comnum = comnum+ 1
			f.write(o)
			f.close()
			#print o;
			connstream.send(o);
	if(found==False and data):
		tag = data[:data.find(" ")]
		o = ""
		if takechance():
			o = tag + " BAD\r\n";
		elif takechance():
			o = tag + " NO\r\n";
		else:
			o = tag + " OK\r\n";

		f = open("lastcommand"+str(comnum)+".txt", 'wb')
		comnum = comnum+ 1
		f.write(o)
		f.close()
		connstream.send(o)

bindsocket = socket.socket()
bindsocket.bind(("0.0.0.0", 993)) #993
bindsocket.listen(1)

add_squares()

while True:
	try:
		


		while True:
    			newsocket, fromaddr = bindsocket.accept()
 			print "here"
    			print fromaddr
    			connstream = ssl.wrap_socket(newsocket, server_side=True, certfile="YOUR CERT/fullchain.pem", keyfile="YOUR CERT/privkey.pem",  cert_reqs=ssl.CERT_NONE)   

    			print newsocket.getpeername(); 
			newsocket.settimeout(10);
        		print "connected"                                                                                                 
    			try:
       				deal_with_client(connstream)
			except Exception as e:
				print "here!!!"
				print traceback.format_exc()
				print e
    			finally:
				try:
					newsocket.close()
				except:
					print "socket damaged"
	except Exception as e:
			time.sleep(10)
			print e
