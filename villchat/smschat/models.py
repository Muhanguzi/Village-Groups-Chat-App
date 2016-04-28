from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from rapidsms.models import Contact

@python_2_unicode_compatible
class Group(models.Model):
	""" Village SMS Group"""
	groupname = models.SlugField(max_length=10,unique=True)
	is_active = models.BooleanField(default=True,blank=True)
	datecreated = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return 'Group %s' % self.groupname

@python_2_unicode_compatible
class Member(models.Model):
    """Member of a village SMS group."""
    contact = models.ForeignKey(Contact)
    group = models.ForeignKey(Group)
    is_creator = models.BooleanField(default=False, blank=True)
    joined_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s/%s' % (self.group, self.contact)

