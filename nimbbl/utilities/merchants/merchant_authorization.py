import jwt

SECRET_KEY="MANAV"
ALGORITHM = 'HS256'

def validate_jwt_token(token_to_validate):
    # secret_key =SECRET_KEY
    algorithm = 'HS256'
    try:
        decoded_payload = jwt.decode(token_to_validate, SECRET_KEY, algorithms=[algorithm])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        print("Token has expired. Please log in again.")
    except jwt.InvalidTokenError:
        print("Invalid token. Access denied.")
    return None