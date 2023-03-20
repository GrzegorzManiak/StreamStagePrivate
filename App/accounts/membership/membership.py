from accounts.models import Member
from accounts.models import MembershipStatus

def get_membership(member):
    return MembershipStatus.objects.filter(member=member).first()

def has_membership(member):
    membership = get_membership(member)

    if membership == None:
        return False
    
    return membership.is_valid()