from __future__ import unicode_literals

from django.db import transaction

from rapidsms.contrib.handlers import KeywordHandler
from rapidsms.models import Contact

from ..models import Group,Member

class JoinHandler(KeywordHandler):
	keyword = 'talk'

	def handle(self,text):
		"""Add member to the village group"""
		text = text.strip().split()
		try:
			group = Group.objects.get(groupname= text[0])
		except Group.DoesNotExist:
			self.respond('Group %s doesnt exist. Please try again'%text[0])
		else:
			with transaction.atomic():
				connection = self.msg.connections[0]
				contact = connection.contact
				if not contact:
					contact = Contact.objects.create(name = text[1])
					connection.contact = contact
					connection.save(update_fields=('contact', ))
					created = Member.objects.get_or_create(contact=contact, group=group, defaults={'is_creator': False})
					if created:
						self.respond('You are now a member')
					else:
						self.respond('Something went wrong')
				else:
					self.respond('You are already a member')

		def help(self):
			self.respond('Something went wrong. Please try again')






