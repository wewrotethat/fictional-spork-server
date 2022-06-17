from enum import Enum

class ProfileVerificationStatus(str, Enum):
    VERIFIED = 'verified'
    # todo: remove this
    UNVERIFIED = 'unverified'
    PENDING = 'pending'
    REJECTED = 'rejected'
