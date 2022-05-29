from enum import Enum

class PhoneVerificationStatus(str, Enum):
    VERIFIED = 'verified'
    UNVERIFIED = 'unverified'
    PENDING = 'pending'
    REJECTED = 'rejected'
