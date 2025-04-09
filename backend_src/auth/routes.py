import hmac
import logging

from fastapi import Depends, status, HTTPException, Response, APIRouter, Request
from redis import Redis

from core.redis_conf import get_redis
from database.models.auth import User
from . import schemas
from .depends import get_form_data, validate_code
from .jwt_module import jwt_schemas
from .jwt_module.creator import create_access_token, create_refresh_token
from .jwt_module.depends import get_user_from_token, get_user_id_from_refresh_token
from .services import UserService
from .utils import send_verification_code

router: APIRouter = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

database: dict[int, schemas.User] = {}


@router.post('/auth')
async def auth_user(
        phone_number: schemas.PhoneNumber = Depends(get_form_data),
        redis_client: Redis = Depends(get_redis)
) -> schemas.SuccessMessageSend:
    """
    first authorization router, user enter phone number and will receive 6-digits code
    :param phone_number: validated phone number
    :param redis_client: redis connection
    :return: success message
    :raise HTTPException with 500(some gone wrong)
    """
    try:
        await send_verification_code(phone_number.phone_number, redis_client)
        return schemas.SuccessMessageSend(
            message="Verification code sent successfully",
        )
    except Exception:
        logging.exception("Exception")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/verify_code")
async def verify_code(
        request: Request,
        response: Response,
        user_auth_info: schemas.UserAuthInfo = Depends(validate_code),
        redis_client: Redis = Depends(get_redis)
):
    """
    second authorization handler, user has received the code, and will enter it to form with code
    set cookies with access and refresh token with httpOnly
    :param response: base fastapi response
    :param request: fastapi request
    :param user_auth_info: validated user information
    :param redis_client: redis connection
    :return: None(only set cookies)
    :raise HTTPException 410 (when code not found in redis)
    :raise HTTPException 403 (when code is wrong)
    """
    # get code from redis using phone number
    backend_code_from_user = redis_client.get(
        user_auth_info.phone_number.phone_number
    )
    if backend_code_from_user is None:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Code lifetime is expired"
        )
    # using to avoid time attack
    if hmac.compare_digest(backend_code_from_user, str(user_auth_info.code)):
        # delete code from redis
        redis_client.delete(user_auth_info.phone_number.phone_number)
        # insert or get user from db
        # create user schema
        user_to_create_schema = schemas.User(phone_number=user_auth_info.phone_number)

        # db business logic
        user_model = await UserService.get_user(user_to_create_schema, request.state.db)
        if user_model is None:
            user_model: User = await UserService.create_user(
                user_to_create_schema,
                request.state.db,
            )
        user_to_create_schema.id = user_model.id

        # user auth success!
        # create jwt tokens
        access_token: str = create_access_token(user=user_to_create_schema)
        refresh_token: str = create_refresh_token(user_to_create_schema.id)

        # set jwt tokens in cookies
        response.set_cookie(
            key=jwt_schemas.TokenType.refresh_token.value,
            value=refresh_token,
            httponly=True,
            secure=False,  # MAKE TRUE ON PRODUCTION
        )

        return {jwt_schemas.TokenType.access_token.value: access_token}

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Wrong code'
    )


@router.get("/refresh_token")
async def get_new_access_token(
        response: Response,
        user_id: int = Depends(get_user_id_from_refresh_token),
):
    """
    using to update access token
    :param response:
    :param user_id: user id from refresh token(token after validation)
    :return: None (set new access token in cookies)
    """
    # get user from database
    user = database[user_id]

    # set jwt
    access_token = create_access_token(user=user)

    response.set_cookie(
        key=jwt_schemas.TokenType.access_token.value,
        value=access_token,
        httponly=True,
        secure=False,  # MAKE TRUE ON PRODUCTION
    )


@router.get("/logout")
async def logout(
        response: Response,
        _=Depends(get_user_from_token)
):
    """
    delete user cookies
    :param response:
    :param _: uses to check that user logged
    :return: None (delete both tokens cookies)
    """
    response.delete_cookie(
        key=jwt_schemas.TokenType.access_token.value,
    )
    response.delete_cookie(
        key=jwt_schemas.TokenType.refresh_token.value,
    )


@router.get("/protected")
async def start_page(
        _=Depends(get_user_from_token)
):
    """
    random protected hand
    :param _: uses to check that user logged
    :return:
    """
    return {"status": "success"}
