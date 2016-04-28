from __future__ import unicode_literals

from django.test import TestCase

from ..handlers.create_group import NewGroupHandler
from ..handlers.join_group import JoinHandler
from ..handlers.leave_group import LeaveGroup

from ..models import Group,Member

class CreateHandlerTest(TestCase):

	def test_create_group(self):
		""" Test using the keyword into """
		replies = NewGroupHandler.test('into daniel')
		self.assertTrue(replies)
		self.assertEquals(len(replies),1)
		group = Group.objects.latest('pk')
		self.assertIn('Use %s to invite people to join' % group.groupname, replies[0])
		self.assertTrue(group.member_set.count(),1)

class JoinHandlerTest(TestCase):

	def setUp(self):
		self.group = Group.objects.create(groupname='7020')

	def test_join_group(self):
		""" Test join using keyword talk """
		replies = JoinHandler.test('talk %s faith' % self.group.groupname)
		self.assertTrue(replies)
		self.assertEquals(len(replies),1)
		self.assertTrue('You are now a member',replies[0])
		self.assertEquals(self.group.member_set.count(),1)

	def test_existing_member(self):
		JoinHandler.test('talk %s faith2' % self.group.groupname)
		replies = JoinHandler.test('talk %s faith2' % self.group.groupname)
		self.assertTrue(replies)
		self.assertEquals(len(replies),1)
		self.assertTrue('You are already a member',replies[0])
		self.assertEquals(self.group.member_set.count(),1)

class LeaveHandlerTest(TestCase):

	def setUp(self):
		self.group = Group.objects.create(groupname='3067')

	def test_leave_group(self):
		""" Leave group using keyword Leave """
		replies = LeaveGroup.test('leave %s' % self.group.groupname)
		self.assertTrue(replies)
		self.assertEquals(len(replies),1)
		self.assertTrue('You have left the group',replies[0])
		self.assertEquals(self.group.member_set.count(),0)

