from djb_api.config import config
from djb_api.domain.auth.actions.login_action import LoginAction
from djb_api.domain.auth.actions.register_action import RegisterAction
from djb_api.domain.auth.dto import UserCredentials
from djb_api.domain.auth.exceptions import RegistrationBlocked
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/login", tags=["auth"])
async def login(
    form_data: UserCredentials,
    login_action: LoginAction = Depends(LoginAction),
):
    return await login_action(form_data)


@router.post("/register", tags=["auth"])
async def register(
    user_data: UserCredentials,
    register_action: RegisterAction = Depends(RegisterAction),
):
    if config.BLOCK_REGISTER == "True":
        raise RegistrationBlocked
    return await register_action(user_data)
