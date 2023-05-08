from fastapi import HTTPException, status
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from config import SECRET_KEY


class TokenManager:
    def __init__(self):
        self.serializer = URLSafeTimedSerializer(SECRET_KEY)

    def generate_token(self, data):
        return self.serializer.dumps(data)

    def verify_token(self, token: str, max_age: int = 60):
        try:
            data = self.serializer.loads(token, max_age=max_age)
            return data
        except SignatureExpired:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired.",
            )
        except BadSignature:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token.",
            )
