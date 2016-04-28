from __future__ import unicode_literals

from rapidsms.models import Contact,Connection
from rapidsms.contrib.handlers import PatternHandler
from rapidsms.router import send

from ..models import Group,Member

class MsgiHandler(PatternHandler):
	pattern = '^([0-9]{4}):\s?(\S.*)'

	def handle(self,slug,text):
		"""Broadcast message in a village group"""
		try:
			group = Group.objects.get(groupname=slug.strip())
		except Group.DoesNotExist:
			self.respond("Group Does not Exist")
		else:
			connection = self.msg.connections[0]
			contacts = Contact.objects.filter(member__group=group)
			if not contacts.filter(connection__pk=connection.pk):
				self.respond('You are not a member of this group')
			else:
				contact_name = contacts.get(connection__pk=connection.pk)
				connections = Connection.objects.filter(contact__in=contacts,
					backend=connection.backend,).exclude(pk=connection.pk)
				count = connections.count
				if count:
					send('From %s(%s): %s' % (contact_name.name,slug,text), connections=connections)
				else:
					self.respond('Message was sent to %s member%s.' % (count, count != 1 and 's' or ''))
