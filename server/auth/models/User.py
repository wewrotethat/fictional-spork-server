class User:
    def __init__(self, first_name, last_name, age, medical_license_id, username, password, phone_number, profile_verification_status,profile_picture_url,phone_verification_status, device_tokens,role, created_at, updated_at):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.medical_license_id = medical_license_id
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.profile_verification_status = profile_verification_status
        self.profile_picture_url = profile_picture_url
        self.phone_verification_status = phone_verification_status
        self.device_tokens = device_tokens
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at

