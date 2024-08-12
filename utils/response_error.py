from fastapi import HTTPException


def response_error(error: str, screen: str):
    raise HTTPException(
        status_code=500,
        detail=f"{error}---------{screen}",
        headers={"WWW-Authenticate": "Bearer"},
    )
