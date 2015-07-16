from io import StringIO
from functools import cmp_to_key
from collections import OrderedDict

class Tag:
	def __init__(self, tag, attr=[], single=False):
		self.tag = tag
		self.attr = attr
		self.sub = []
		self.single = single
		
	def write(self, w, nice=True, level=0, indent="  ", loop=0):
		if nice:
			w(indent*level)
			
		w("<%s" % self.tag)
		
		def cmpfunc(x,y):
			if x[0]=="id":
				return -1
			if y[0]=="id":
				return 1
			#TODO order strings here?
			return 0
		
		for k,v in sorted(self.attr, key=cmp_to_key(cmpfunc)):
			w(" %s=\"%s\"" % (k, str(v)))
		
		if len(self.sub)==0 and not self.single:
			w(" />")
		else:
			if self.tag=="Object":
				w(" ")
			w(">")
			
		if nice and len(self.sub)>0:
			w("\n")

		for s in self.sub:
			if isinstance(s, str):
				if nice:
					w(indent*(level+1))
				w(s)
				if nice:
					w("\n")
			else:
				#if loop<n: prevent recursion
				s.write(w, nice, level+(0 if self.single else 1), indent, loop+1)
				
		if nice and not self.single:
			w(indent*(level))
		if not len(self.sub)==0 and not self.single:
			w("</%s>" % self.tag)
		if nice and not self.single:
			w("\n")
			
		
	def __call__(self, tag):
		print("Adding %s to %s" % (tag.tag, self.tag))
		self.sub.append(tag)
		
	def __repr__(self):
		s = StringIO()
		self.write(s.write)
		s.seek(0)
		return s.read()
