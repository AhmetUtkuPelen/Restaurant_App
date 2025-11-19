import os
import logging
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, Union

from fastapi import HTTPException, status
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError
from dotenv import load_dotenv

## logging config ##
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

###### JWT Configuration - get .env fields #######
SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.getenv("SECRET_KEY", "your-default-secret-key-for-dev"))
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
ISSUER = os.getenv("JWT_ISSUER", "ecommerce-api")
AUDIENCE = os.getenv("JWT_AUDIENCE", "ecommerce-client")


class TokenError(Exception):
    """Base exception class for token related errors"""
    def __init__(self, message: str = "Token validation failed", error_code: str = "token_error", **kwargs):
        self.message = message
        self.error_code = error_code
        self.details = kwargs
        super().__init__(self.message)
        
    def to_dict(self) -> dict:
        return {
            "error": self.error_code,
            "message": self.message,
            **self.details
        }
        
    def __str__(self) -> str:
        details = ", ".join(f"{k}={v}" for k, v in self.details.items())
        return f"{self.message} ({self.error_code}){f' - {details}' if details else ''}"



class TokenExpiredError(TokenError):
    """ Raises when a token has expired """
    def __init__(self, message: str = "Token has expired", **kwargs):
        super().__init__(
            message=message,
            error_code="token_expired",
            **kwargs
        )



class TokenInvalidError(TokenError):
    """ Raises when a token is invalid """
    def __init__(self, message: str = "Invalid token", reason: str = None, **kwargs):
        details = {"reason": reason} if reason else {}
        details.update(kwargs)
        super().__init__(
            message=message,
            error_code="token_invalid",
            **details
        )





def create_access_token(
    data: Dict[str, Any], 
    expires_delta: Optional[timedelta] = None,
    additional_claims: Optional[Dict[str, Any]] = None
) -> str:
    """
    Creates an access token with all required claims.
        
    Returns : str: The encoded access token.
        
    Raises : TokenError: If token creation fails or required claims are missing.
    """
    try:
        # Validate required data
        if not data.get("sub"):
            raise TokenError("Missing required 'sub' claim for token creation")
        
        to_encode = data.copy()
        now = datetime.now(timezone.utc)
        
        # Set expiration time
        if expires_delta:
            expire = now + expires_delta
        else:
            expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({
            "exp": expire,
            "iat": now,
            "iss": ISSUER,
            "aud": AUDIENCE,
            "sub": str(data["sub"]),
            "jti": str(uuid.uuid4()),
            "token_type": "access",
            "nbf": now,
        })
        
        if "role" in data:
            to_encode["role"] = data["role"]
        
        if additional_claims:
            to_encode.update(additional_claims)
        
        required_claims = ["sub", "exp", "iat", "iss", "aud", "jti", "token_type"]
        missing_claims = [claim for claim in required_claims if claim not in to_encode]
        if missing_claims:
            raise TokenError(f"Missing required claims: {missing_claims}")
        
        # Encode and return the token
        encoded_token = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        
        logger.info(f"Access token created successfully for user: {data['sub']}")
        return encoded_token
        
    except TokenError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating access token: {str(e)}", exc_info=True)
        raise TokenError(
            "Failed to create access token",
            error_type=type(e).__name__,
            details=str(e)
        )




def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Creates a refresh token with all required claims.
        
    Returns : str: The encoded refresh token.
        
    Raises : TokenError: If token creation fails or required claims are missing.
    """
    try:
        if not data.get("sub"):
            raise TokenError("Missing required 'sub' claim for refresh token creation")
        
        to_encode = data.copy()
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode.update({
            "exp": expire,
            "iat": now,
            "iss": ISSUER,
            "aud": AUDIENCE,
            "sub": str(data["sub"]),
            "jti": str(uuid.uuid4()),
            "token_type": "refresh",
            "nbf": now,
        })
        
        required_claims = ["sub", "exp", "iat", "iss", "aud", "jti", "token_type"]
        missing_claims = [claim for claim in required_claims if claim not in to_encode]
        if missing_claims:
            raise TokenError(f"Missing required claims: {missing_claims}")
        
        # Encode and return the token
        encoded_token = jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        
        logger.info(f"Refresh token created successfully for user: {data['sub']}")
        return encoded_token
        
    except TokenError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating refresh token: {str(e)}", exc_info=True)
        raise TokenError(
            "Failed to create refresh token",
            error_type=type(e).__name__,
            details=str(e)
        )





async def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decodes and validates an access token with comprehensive error handling.
        
    Returns : Dict[str, Any]: The decoded token payload.
        
    Raises: TokenExpiredError: If the token has expired. TokenInvalidError: If the token is invalid or malformed. TokenError: For other token-related errors.
    """
    try:
        if not token or not isinstance(token, str):
            raise TokenInvalidError("Token must be a non-empty string")
        
        ### Remove 'Bearer' prefix if present ###
        if token.startswith('Bearer '):
            token = token[7:]
        
        ### Decode the token ###
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience=AUDIENCE,
            issuer=ISSUER,
            options={
                "verify_aud": True,
                "verify_iss": True,
                "verify_exp": True,
                "verify_iat": True,
                "verify_nbf": True,
                "verify_signature": True,
                "require": ["exp", "iat", "sub", "iss", "aud", "jti", "token_type"]
            }
        )
        
        _validate_token_claims(payload)
        
        now = datetime.now(timezone.utc)
        
        if "nbf" in payload:
            nbf = datetime.fromtimestamp(payload["nbf"], tz=timezone.utc)
            if now < nbf:
                raise TokenInvalidError(
                    "Token is not yet valid",
                    reason="Token not before time has not been reached",
                    not_before=nbf.isoformat()
                )
        
        # Verify token type is access token
        if payload.get("token_type") != "access":
            raise TokenInvalidError(
                "Invalid token type",
                reason=f"Expected 'access' token, got '{payload.get('token_type')}'",
                token_type=payload.get("token_type")
            )
        
        logger.debug(f"Access token decoded successfully for user: {payload.get('sub')}")
        return payload
        
    except ExpiredSignatureError as e:
        logger.warning(f"Token has expired: {str(e)}")
        expired_at = None
        try:
            unverified_payload = jwt.decode(token, options={"verify_signature": False})
            if "exp" in unverified_payload:
                expired_at = datetime.fromtimestamp(unverified_payload["exp"], tz=timezone.utc).isoformat()
        except Exception:
            pass
            
        raise TokenExpiredError(
            "Your session has expired. Please log in again.",
            expired_at=expired_at
        )
        
    except JWTClaimsError as e:
        logger.warning(f"Token claims invalid: {str(e)}")
        raise TokenInvalidError(
            "Invalid token claims",
            reason=str(e),
            expected_issuer=ISSUER,
            expected_audience=AUDIENCE
        )
        
    except TokenError:
        raise
        
    except JWTError as e:
        logger.warning(f"Invalid token: {str(e)}")
        raise TokenInvalidError(
            "Invalid authentication token",
            reason=str(e),
            error_type=type(e).__name__
        )
        
    except ValueError as e:
        logger.warning(f"Token value error: {str(e)}")
        raise TokenInvalidError(
            "Malformed token",
            reason=str(e),
            error_type="ValueError"
        )
        
    except Exception as e:
        logger.error(f"Unexpected error decoding token: {str(e)}", exc_info=True)
        raise TokenError(
            "An error occurred while processing your authentication token",
            error_type=type(e).__name__,
            details=str(e)
        )


async def decode_refresh_token(token: str) -> Dict[str, Any]:
    """
    Decodes and validates a refresh token with comprehensive error handling.
        
    Returns : Dict[str, Any]: The decoded token payload.
        
    Raises : TokenExpiredError: If the token has expired. TokenInvalidError: If the token is invalid or malformed. TokenError: For other token-related errors.
    """
    try:
        if not token or not isinstance(token, str):
            raise TokenInvalidError("Token must be a non-empty string")
        
        #### Remove 'Bearer ' prefix if present ###
        if token.startswith('Bearer '):
            token = token[7:]
        
        ### Decode the token ###
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            audience=AUDIENCE,
            issuer=ISSUER,
            options={
                "verify_aud": True,
                "verify_iss": True,
                "verify_exp": True,
                "verify_iat": True,
                "verify_nbf": True,
                "verify_signature": True,
                "require": ["exp", "iat", "sub", "iss", "aud", "jti", "token_type"]
            }
        )
        
        _validate_token_claims(payload)
        
        # Verify token type is refresh token #
        if payload.get("token_type") != "refresh":
            raise TokenInvalidError(
                "Invalid token type",
                reason=f"Expected 'refresh' token, got '{payload.get('token_type')}'",
                token_type=payload.get("token_type")
            )
        
        logger.debug(f"Refresh token decoded successfully for user: {payload.get('sub')}")
        return payload
        
    except ExpiredSignatureError as e:
        logger.warning(f"Refresh token has expired: {str(e)}")
        expired_at = None
        try:
            unverified_payload = jwt.decode(token, options={"verify_signature": False})
            if "exp" in unverified_payload:
                expired_at = datetime.fromtimestamp(unverified_payload["exp"], tz=timezone.utc).isoformat()
        except Exception:
            pass
            
        raise TokenExpiredError(
            "Your refresh token has expired. Please log in again.",
            expired_at=expired_at
        )
        
    except JWTClaimsError as e:
        logger.warning(f"Refresh token claims invalid: {str(e)}")
        raise TokenInvalidError(
            "Invalid refresh token claims",
            reason=str(e),
            expected_issuer=ISSUER,
            expected_audience=AUDIENCE
        )
        
    except TokenError:
        raise
        
    except JWTError as e:
        logger.warning(f"Invalid refresh token: {str(e)}")
        raise TokenInvalidError(
            "Invalid refresh token",
            reason=str(e),
            error_type=type(e).__name__
        )
        
    except ValueError as e:
        logger.warning(f"Refresh token value error: {str(e)}")
        raise TokenInvalidError(
            "Malformed refresh token",
            reason=str(e),
            error_type="ValueError"
        )
        
    except Exception as e:
        logger.error(f"Unexpected error decoding refresh token: {str(e)}", exc_info=True)
        raise TokenError(
            "An error occurred while processing your refresh token",
            error_type=type(e).__name__,
            details=str(e)
        )




def _validate_token_claims(payload: Dict[str, Any]) -> None:
    """
    Validates the structure and content of token claims.
        
    Raises : TokenInvalidError: If required claims are missing or invalid.
    """

    required_claims = ["sub", "exp", "iat", "iss", "aud", "jti", "token_type"]
    missing_claims = [claim for claim in required_claims if claim not in payload]
    if missing_claims:
        raise TokenInvalidError(
            "Missing required token claims",
            reason=f"Missing claims: {missing_claims}",
            missing_claims=missing_claims
        )
    
    if not isinstance(payload.get("sub"), str) or not payload["sub"]:
        raise TokenInvalidError(
            "Invalid subject claim",
            reason="Subject (sub) must be a non-empty string"
        )
    
    if not isinstance(payload.get("jti"), str) or not payload["jti"]:
        raise TokenInvalidError(
            "Invalid JWT ID claim",
            reason="JWT ID (jti) must be a non-empty string"
        )
    
    for claim in ["exp", "iat"]:
        if not isinstance(payload.get(claim), (int, float)):
            raise TokenInvalidError(
                f"Invalid {claim} claim",
                reason=f"{claim} must be a numeric timestamp"
            )
    
    if payload["iss"] != ISSUER:
        raise TokenInvalidError(
            "Invalid issuer",
            reason=f"Expected issuer '{ISSUER}', got '{payload['iss']}'",
            expected_issuer=ISSUER,
            actual_issuer=payload["iss"]
        )
    
    if payload["aud"] != AUDIENCE:
        raise TokenInvalidError(
            "Invalid audience",
            reason=f"Expected audience '{AUDIENCE}', got '{payload['aud']}'",
            expected_audience=AUDIENCE,
            actual_audience=payload["aud"]
        )




def validate_jwt_configuration() -> None:
    """
    Validates JWT configuration at startup to ensure all required settings are present.
    
    Raises : ValueError: If required JWT configuration is missing or invalid.
    """
    errors = []
    
    if not SECRET_KEY or SECRET_KEY == "your-default-secret-key-for-dev":
        errors.append("JWT_SECRET_KEY must be set to a secure value")
    
    if len(SECRET_KEY) < 32:
        errors.append("JWT_SECRET_KEY should be at least 32 characters long")
    
    if not ALGORITHM:
        errors.append("JWT_ALGORITHM must be specified")
    
    if ALGORITHM not in ["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]:
        errors.append(f"Unsupported JWT algorithm: {ALGORITHM}")
    
    if ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
        errors.append("ACCESS_TOKEN_EXPIRE_MINUTES must be positive")
    
    if REFRESH_TOKEN_EXPIRE_DAYS <= 0:
        errors.append("REFRESH_TOKEN_EXPIRE_DAYS must be positive")
    
    if not ISSUER:
        errors.append("JWT_ISSUER must be specified")
    
    if not AUDIENCE:
        errors.append("JWT_AUDIENCE must be specified")
    
    if errors:
        error_message = "JWT configuration errors:\n" + "\n".join(f"- {error}" for error in errors)
        logger.error(error_message)
        raise ValueError(error_message)
    
    logger.info("JWT configuration validated successfully")


def get_token_info(token: str) -> Dict[str, Any]:
    """
    Gets basic information about a token without full validation (for debugging).
        
    Returns : Dict[str, Any]: Basic token information or error details.
    """
    try:
        ### Remove 'Bearer ' prefix if present ###
        if token.startswith('Bearer '):
            token = token[7:]
        
        # Decode without verification #
        payload = jwt.decode(
            token, 
            key="", 
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_iss": False,
                "verify_exp": False,
                "verify_iat": False,
                "verify_nbf": False
            }
        )
        
        info = {
            "valid_structure": True,
            "sub": payload.get("sub"),
            "token_type": payload.get("token_type"),
            "iss": payload.get("iss"),
            "aud": payload.get("aud"),
            "jti": payload.get("jti")
        }
        
        # Add expiration info #
        if "exp" in payload:
            exp_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
            info["expires_at"] = exp_time.isoformat()
            info["is_expired"] = datetime.now(timezone.utc) > exp_time
        
        if "iat" in payload:
            iat_time = datetime.fromtimestamp(payload["iat"], tz=timezone.utc)
            info["issued_at"] = iat_time.isoformat()
        
        return info
        
    except Exception as e:
        return {
            "valid_structure": False,
            "error": str(e),
            "error_type": type(e).__name__
        }