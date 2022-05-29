from enum import Enum

class ProfileVerificationStatus(str, Enum):
    VERIFIED = 'verified'
    UNVERIFIED = 'unverified'
    PENDING = 'pending'
    REJECTED = 'rejected'
