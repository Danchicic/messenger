from pydantic import BaseModel, field_validator
import re


class PhoneNumber(BaseModel):
    phone_number: str

    @field_validator('phone_number')
    def validate_phone_number(cls, value):
        if not re.fullmatch(r"\+7\d{10}", value):
            raise ValueError("Phone number must be entered in the format: +7123456789")
        return value


class SuccessMessageSend(BaseModel):
    message: str


class User(BaseModel):
    id: int
    phone_number: PhoneNumber


class UserAuthInfo(BaseModel):
    code: int
    phone_number: PhoneNumber

    @field_validator("code")
    def validate_code(cls, value):
        if not re.fullmatch(r"\d{6}", str(value)):
            raise ValueError("Code must be 6-digit number")
        return value
