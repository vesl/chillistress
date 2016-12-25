import err
from html.parser import HTMLParser

class cshtml(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.check=False
		self.result=False

	def checkIfChilliPortal(self,tag,name,value):
		if tag == 'form' and name == 'action': 
			self.result = value
			return True
		else : return False

	def handle_starttag(self, tag, attrs):
		for name,value in attrs:
			if self.check == 'checkIfChilliPortal':
				if self.checkIfChilliPortal(tag,name,value) is not False: break
