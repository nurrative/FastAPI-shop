import uuid
from datetime import datetime, timedelta
from typing import Optional

import jwt
import bcrypt

from core.config import Settings, settings


# private_key = "-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAuNhCS6bodtd+PvKqNj+tYZYqTNMDkf0rcptgHhecSsMP9Vay\n+6NvJk1tC+IajPaE4yRJVY4jFqEt3A0MJ9sKe5mWDYFmzW/L6VzQvQ+0nrMc1YTE\nDpOf7BQhlW5W0mDj5SwSR50Lxg/acb+SMWq6zmhuAoLRapH17K2RWONA2vr2frox\nJ6N9TGtrQHygDb0p9D6jPnXEe4y+zBuj6o0bCkJgCVNM+CU19xBepj5caetYV28/\n49yl5XPi93n1ATU+7aGAKxuvjudODuHhF/UsZScMFSHeZW367eQldTB2w9uoIIzW\nO46tKimr21zYifMimjwnBQ/PLDqc7HqY0Y/rLQIDAQABAoIBAAdu0CD7/Iu61/LE\nDfV8fgZXOYA5WVgSLCBsVbh1Y+2FsStBFJVrLwRanLCbo6GuJWMqNGC3ryWGebJI\nPAg7lfepEhBHodClAY1yvq9mOvHJa2Fn+KegEWWMMbAxQwCBW5NS6waXhBUE0i3n\ncYOB3TKA9IYuqH52kW22VQqT/imlWEb28pJJT49YfggmOOtAkrKerokO53lAfrJA\ntm8lYvxXnfnuYh7zI835RpZJ1PeaYrMqyAwT+StD9hPKGWGpN1gCJijjcK0aapvq\nMLET/JxMxxcLsINOeLtGhMKawmET3J/esJTumOE2L77MFG83rlCPbsSfLdSAI2WD\nSe3Q2ikCgYEA7JzmVrPh7G/oILLzIfk8GHFACRTtlE5SDEpFq+ARMprfcBXpkl+Q\naWqQ3vuSH7oiAQKlvo3We6XXohCMMDU2DyMaXiQMk73R83fMwbFnFcqFhbzx2zpm\nj/neHIViEi/N69SHPxl+vnUTfeVZptibNGS+ch3Ubawt3wCaWr+IdAcCgYEAx/19\ns5ryq2oTQCD5GfIqW73LAUly5RqENLvKHZ2z+mZ0pp7dc5449aDsHPLXLl1YC3mO\nlZZk+8Jh5yrpHyljiIYwh/1y0WsbungMlH6lG9JigcN8R2Tk9hWT7DQL0fm0dYoQ\njkwr/gJv6PW0piLsR0vsQQpm/F/ucZolVPQIoisCgYA5XXzWznvax/LeYqRhuzxf\nrK1axlEnYKmxwxwLJKLmwvejBB0B2Nt5Q1XmSdXOjWELH6oxfc/fYIDcEOj8ExqN\nJvSQmGrYMvBA9+2TlEAq31Pp7boxbYJKK8k23vu87wwcvgUgPj0lTdsw7bcDpYZT\neI1Xu3WyNUlVxJ6nm8IoZwKBgG6YPjVekKg+htrF4Tt58fa95E+X4JPVsBrBZqou\nFeN5WTTzUZ+odfNPxILVwC2BrTjbRgBvJPUcr6t4zWZQKxzKqHfrrt0kkDb0QHC2\nAHR8ScFc65NHtl5n3F+ZAJhjsGn3qeQnN4TGsEBx8C6XzXY4BDSLnhweqOvlxJNQ\nSJ31AoGAX/UN5xR6PlCgPw5HWfGd7+4sArkjA36DAXvrAgW/6/mxZZzoGA1swYdZ\nq2uGp38UEKkxKTrhR4J6eR5DsLAfl/KQBbNC42vqZwe9YrS4hNQFR14GwlyJhdLx\nKQD/JzHwNQN5+o+hy0lJavTw9NwAAb1ZzTgvq6fPwEG0b9hn0SI=\n-----END RSA PRIVATE KEY-----\n"
# public_key = "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuNhCS6bodtd+PvKqNj+t\nYZYqTNMDkf0rcptgHhecSsMP9Vay+6NvJk1tC+IajPaE4yRJVY4jFqEt3A0MJ9sK\ne5mWDYFmzW/L6VzQvQ+0nrMc1YTEDpOf7BQhlW5W0mDj5SwSR50Lxg/acb+SMWq6\nzmhuAoLRapH17K2RWONA2vr2froxJ6N9TGtrQHygDb0p9D6jPnXEe4y+zBuj6o0b\nCkJgCVNM+CU19xBepj5caetYV28/49yl5XPi93n1ATU+7aGAKxuvjudODuHhF/Us\nZScMFSHeZW367eQldTB2w9uoIIzWO46tKimr21zYifMimjwnBQ/PLDqc7HqY0Y/r\nLQIDAQAB\n-----END PUBLIC KEY-----\n"


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: Optional[timedelta] = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(
    password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


# encoded = jwt.encode({"some": "payload"}, private_key, algorithm="PS256")
# decoded = jwt.decode(encoded, public_key, algorithms=["PS256"])
