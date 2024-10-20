
# for the source, don't even use this sh in production
HARDCODED_DEVELOPMENT_JWT = 'HARDCODED_DEVELOPMENT_JWT'


class AuthenticationService:

    # change this sh when required
    @staticmethod
    def is_valid_jwt(jwt: str) -> bool:
        return jwt == HARDCODED_DEVELOPMENT_JWT
