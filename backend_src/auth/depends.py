from typing import Annotated

from fastapi import Form, HTTPException

from . import schemas


def get_form_data(
        phone_number: Annotated[str, Form()]
) -> schemas.PhoneNumber:
    """
    extract phone number from authorization form
    :param phone_number: string from form
    :return: validated phone number using pydantic
    :raises: HTTPException with 422(validation error)
    """
    try:
        return schemas.PhoneNumber(
            phone_number=phone_number,
        )
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid format of phone number, phone number must be entered in the format: +7123456789",
        )


def validate_code(
        code: int,
        phone_number: str
) -> schemas.UserAuthInfo:
    """
    validate full user information
    :param code: 6-digit code
    :param phone_number: string
    :return: validated code and phone_number in UserAuthInfo schema
    :raise: HTTPException with 422(validation error)
    """
    try:
        return schemas.UserAuthInfo(
            phone_number=schemas.PhoneNumber(phone_number=phone_number),
            code=code,
        )
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid format of code or phone number",
        )
