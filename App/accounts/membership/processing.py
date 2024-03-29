from accounts.models import Member, MembershipStatus
from accounts.membership.membership import get_membership, has_membership
import time
from datetime import datetime, timedelta, timezone

def add_or_extend_membership(member: Member, time: timedelta):
    membership = get_membership(member)

    if membership == None:
        membership = MembershipStatus(
            member = member,
            expires_on = datetime.now(tz=timezone.utc)
        )
        membership.save()

    membership.expires_on = membership.expires_on + time
    membership.save()