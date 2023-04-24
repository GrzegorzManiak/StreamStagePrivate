import json
from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model

from StreamStage.templatetags.tags import cross_app_reverse
from accounts.models import Member, Broadcaster, BroadcasterContributeInvite
from datetime import datetime, timedelta

from .invitations import (
    send_invite,
    accept_invite,
    reject_invite,
    is_invited,
    get_invitations
)

class BroadcasterTests(TestCase):
    def setUp(self):
        
        # Create Test Member 1
        self.member1 = Member.objects.create(
            username = 'TestMember1',
            cased_username = "testmember1",
            email = 'test@gmail.com',
            country = 'IE',
            is_streamer = True
        )
        # Create Test Member 2
        self.member2 = Member.objects.create(
            username = 'TestMember2',
            cased_username = "testmember2",
            email = 'test2@gmail.com',
            country = 'IE',
            is_streamer = False
        )

        # Create Test Broadcaster
        self.broadcaster = Broadcaster.objects.create(
            handle = 'TestBroadcaster',
            streamer = self.member1,
            name = 'Broadcaster',
            biography = 'test biography',
            over_18 = True,
            approved = True
        )

    def test_send_invite(self):

        inviter = self.member1
        invitee = self.member2
        message = "Test message!"
        broadcaster= self.broadcaster

        # Call send invitation method
        send_invite(inviter, invitee, broadcaster, message)

        # Attempt to query invite object
        invite = BroadcasterContributeInvite.objects.filter(inviter=self.member1).first()

        # Test if invite exists
        self.assertIsNotNone(invite)

        # Test if invitee and inviter are correct

        self.assertEqual(invite.inviter, inviter)
        self.assertEqual(invite.invitee, invitee)

    def test_accept_invite(self):
        
        # Create test invitation
        inviter = self.member1
        invitee = self.member2
        message = "Test message!"
        broadcaster= self.broadcaster

        invite = send_invite(inviter, invitee, broadcaster, message)

        # Invoke accept method
        accept_invite(invite)

        # Test invitation pending status has changed
        self.assertFalse(invite.is_pending)

        # Test if member2 has been added to broadcaster contributors

        self.assertIn(invitee, broadcaster.contributors.iterator())
        
    def test_reject_invite(self):
        
        # Create test invitation
        inviter = self.member1
        invitee = self.member2
        message = "Test message!"
        broadcaster= self.broadcaster

        invite = send_invite(inviter, invitee, broadcaster, message)

        # Invoke reject method
        reject_invite(invite)

        # Test invitation pending status has changed
        self.assertFalse(invite.is_pending)

                
    def test_is_invited(self):
        
        # Create test invitation
        inviter = self.member1
        invitee = self.member2
        message = "Test message!"
        broadcaster= self.broadcaster

        invite = send_invite(inviter, invitee, broadcaster, message)

        # Invoke is_invited method
        invited = is_invited(invitee, broadcaster)

        # Test method return value
        self.assertTrue(invited)
    
    def test_get_invitations(self):
        
        # Create test invitation
        inviter = self.member1
        invitee = self.member2
        message = "Test message!"
        broadcaster= self.broadcaster

        invites = [send_invite(inviter, invitee, broadcaster, message)]

        # Invoke is_invited method
        invitations = get_invitations(invitee)

        # Test method return value
        self.assertListEqual(list(invitations), list(invites))

        


