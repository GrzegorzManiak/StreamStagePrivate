from accounts.models import Member, MembershipStatus
from accounts.membership.membership import get_membership, has_membership
import time
from datetime import datetime, timedelta, timezone

def add_or_extend_membership(member: Member, time: timedelta):
    membership = get_membership(member)

    if membership == None:
        print("Creating membership")
        membership = MembershipStatus(
            member = member,
            expires_on = datetime.now(tz=timezone.utc)
        )
        membership.save()

    membership.expires_on = membership.expires_on + time
    membership.save()
    print("Added", time, "for a total of", (membership.expires_on - datetime.now(tz=timezone.utc)), "(expiry:",membership.expires_on,")")
