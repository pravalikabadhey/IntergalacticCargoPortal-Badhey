from pydantic import BaseModel, ConfigDict, EmailStr


class SignupIn(BaseModel):
    model_config = ConfigDict(extra="ignore")

    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class CargoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cargo_id: str
    origin: str
    destination: str
    weight_kg: int


class UploadResultOut(BaseModel):
    received: int
    saved: int
    skipped_prime: int
    malformed: int
