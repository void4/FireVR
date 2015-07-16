# IPFS-VR by void

# To the extent possible under law, the person who associated CC0 with
# IPFS-VR has waived all copyright and related or neighboring rights
# to IPFS-VR.

# You should have received a copy of the CC0 legalcode along with this
# work. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

from io import StringIO
from functools import cmp_to_key

class Tag:
	def __init__(self, tag, **kwargs):
		self.tag = tag
		if not "sub" in kwargs.keys():
			self.sub = []
		if not "single" in kwargs.keys():
			self.single = False
		self.__dict__.update(kwargs)
		
	def write(self, w, nice=True, level=0, indent="  "):
		if nice:
			w(indent*level)
			
		w("<%s" % self.tag)
		
		#TODO use OrderedDict argument instead of **kwargs as Tag() argument
		def cmpfunc(x,y):
			if x[0]=="id":
				return -1
			if y[0]=="id":
				return 1
			#TODO order strings here?
			return 0
		
		for k,v in sorted(self.__dict__.items(), key=cmp_to_key(cmpfunc)):
			if k not in ["tag", "sub", "single", "level", "indent"]:
				w(" %s=\"%s\"" % (k, str(v)))
		
		if len(self.sub)==0 and not self.single:
			w(" />")
		else:
			if self.tag=="Object":
				w(" ")
			w(">")
			
		if nice and len(self.sub)>0:
			w("\n")
				
		for i, s in enumerate(self.sub):
			if isinstance(s, str):
				if nice:
					w(indent*(level+1))
				w(s)
				if nice:
					w("\n")
			else:
				s.write(w, nice, level+(0 if self.single else 1), indent)
				
		if nice and not self.single:
			w(indent*(level))
		if not len(self.sub)==0 and not self.single:
			w("</%s>" % self.tag)
		if nice and not self.single:
			w("\n")
			
		
	def __call__(self, tag):
		self.sub.append(tag)
		
	def __repr__(self):
		s = StringIO()
		self.write(s.write)
		s.seek(0)
		return s.read()
