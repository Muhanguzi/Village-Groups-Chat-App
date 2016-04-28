from __future__ import unicode_literals

from django.db import transaction
from django.utils.crypto import get_random_string

from rapidsms.contrib.handlers import KeywordHandler
from rapidsms.models import Contact

from ..models import Group,Member

class NewGroupHandler(KeywordHandler):
	keyword = "into"

	def handle(self, text):
		"""Create group handler."""
		text=text.strip().upper()
		created=False
		while not created:
			slug = get_random_string(length=4, allowed_chars='01234567890')
			with transaction.atomic():
				group, created = Group.objects.get_or_create(groupname=slug)
				if created:
					connection = self.msg.connections[0]
					contact = connection.contact
					if not contact:
						contact = Contact.objects.create(name=text)
						connection.contact = contact
						connection.save(update_fields=('contact', ))
					Member.objects.create(contact=contact, group=group, is_creator=True)
					reply = '%s YOUR GROUP HAS BEEN CREATED. Use %s to invite people to join'%(text,slug)
					self.respond(reply)

	def help(self):
		self.respond('Please send INTO GROUPNAME YOURNAME to creat group.')

