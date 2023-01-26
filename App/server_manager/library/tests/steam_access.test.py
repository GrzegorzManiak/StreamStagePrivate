from django.test import TestCase
from ...models import StreamAccess
from accounts.models import Member
from .. import generate_key, invalidate_key, key_exists

class TestStreamAccess(TestCase):
    def setUp(self):
        self.user = Member.objects.create(
            username="test",
            access_level=0
        )

        StreamAccess.objects.create(
            user=self.user,
            stream="test"
        )