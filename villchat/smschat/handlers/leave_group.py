from __future__ import unicode_literals

from rapidsms.contrib.handlers import KeywordHandler
from rapidsms.models import Contact

from smschat.models import Group,Member

class LeaveGroup(KeywordHandler):

	keyword = 'leave'

	def help(self):
		return self.respond('An error was encounted while processing you request. Please try again.')

	def handle(self,text):
		""" Leave group handler """
		
		try:
			group = Group.objects.get(groupname=text.strip().lower())
		except Group.DoesNotExist:
			self.respond('This %s group does not exist' % text.strip())
		else:
			connection = self.msg.connections[0]
			contact = connection.contact
			if contact:
				left = Member.objects.get(contact=contact).delete()
				left_cont = Contact.objects.get(id=contact.id).delete()
				self.respond('You have left the group')
			else:
				self.respond('An error was encounted while processing you request. Please try again.')




