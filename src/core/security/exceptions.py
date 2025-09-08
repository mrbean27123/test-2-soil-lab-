"""Security-related exceptions"""


class SecurityError(Exception):
    """Base exception for security-related errors"""
    status_code = 500
    default_message = "Internal server error"

    def __init__(self, message: str | None = None, original_error: Exception | None = None):
        super().__init__(message or self.default_message)
        self.original_error = original_error


# class PasswordError(SecurityError):
#     """Exception for password-related errors"""
#     status_code = 500
#     default_message = "Internal server error"
#
#
# class EmptyPasswordError(PasswordError):
#     """Exception raised when password is empty or None"""
#     status_code = 500
#     default_message = "Internal server error"
#
#
# class InvalidPasswordHashError(PasswordError):
#     """Exception raised when password hash is invalid or corrupted"""
#     status_code = 500
#     default_message = "Internal server error"
#
#
# class PasswordTooLongError(PasswordError):
#     """Exception raised when password exceeds maximum allowed length"""
#     status_code = 500
#     default_message = "Internal server error"
#
#
# class HashingError(PasswordError):
#     """Exception for password hashing errors"""
#     status_code = 500
#     default_message = "Internal server error"
#
#
# class VerificationError(PasswordError):
#     """Exception for password verification errors"""
#     status_code = 500
#     default_message = "Internal server error"
#
#
# class HashContextError(SecurityError):
#     """Exception for password context configuration errors"""
#     status_code = 500
#     default_message = "Internal server error"


class TokenError(SecurityError):
    """Base exception for token-related errors"""
    status_code = 401
    default_message = "Token error"


class TokenCreationError(TokenError):
    """Exception raised when token creation fails"""
    status_code = 500
    default_message = "Failed to create access token"


class TokenVerificationError(TokenError):
    """Exception raised when token verification fails"""
    default_message = "Failed to verify token"


class InvalidTokenError(TokenError):
    """Exception raised when token is invalid or malformed"""
    default_message = "Invalid token claims"


class ExpiredTokenError(TokenError):
    """Exception raised when token is expired"""
    default_message = "Token has expired"


class InvalidTokenTypeError(TokenError):
    """Exception raised when token type is invalid or unexpected"""
    default_message = "Token type is invalid or unexpected"


class EmptyTokenError(TokenError):
    """Exception raised when token is empty or None"""
    default_message = "Token is empty or None"


class TokenSignatureError(TokenError):
    """Exception raised when token signature is invalid"""
    default_message = "Token signature is invalid"
