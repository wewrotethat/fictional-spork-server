import re


class UserValidators:
    def validateSignUpInput(self, data: dict):
        errors = []
        # validate first name
        if "firstName" not in data:
            errors.append("firstName is required")
        elif not isinstance(data["firstName"], str):
            errors.append("firstName must be a string")
        elif len(data["firstName"]) < 2:
            errors.append("firstName must be at least 2 characters")

        # validate last name
        if "lastName" not in data:
            errors.append("lastName is required")
        elif not isinstance(data["lastName"], str):
            errors.append("lastName must be a string")
        elif len(data["lastName"]) < 2:
            errors.append("lastName must be at least 2 characters")

        # validate email
        if "email" not in data:
            errors.append("email is required")
        elif not isinstance(data["email"], str):
            errors.append("email must be a string")
        elif len(data["email"]) < 5:
            errors.append("email must be at least 5 characters")
        # check email with regex
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
            errors.append("email must be a valid email")

        # validate phone number
        if "phoneNumber" not in data:
            errors.append("phoneNumber is required")
        elif not isinstance(data["phoneNumber"], str):
            errors.append("phoneNumber must be a string")
        elif len(data["phoneNumber"]) < 10:
            errors.append("phoneNumber must be at least 10 characters")
        elif not data["phoneNumber"].startswith("+251"):
            errors.append(
                "phoneNumber should be an Ethiopian number and it must start with +251"
            )

        # validate medical license id
        if "medicalLicenseId" not in data:
            errors.append("medicalLicenseId is required")
        elif not isinstance(data["medicalLicenseId"], str):
            errors.append("medicalLicenseId must be a string")
        elif len(data["medicalLicenseId"]) < 5:
            errors.append("medicalLicenseId must be at least 5 characters")

        # validate password
        if "password" not in data:
            errors.append("password is required")
        elif not isinstance(data["password"], str):
            errors.append("password must be a string")
        elif len(data["password"]) < 8:
            errors.append("password must be at least 8 characters")
        elif not re.match(r"[A-Za-z0-9@#$%^&+=]{8,}", data["password"]):
            errors.append(
                "password must contain at least one uppercase letter, one lowercase letter, one number and one special character"
            )

        return errors
