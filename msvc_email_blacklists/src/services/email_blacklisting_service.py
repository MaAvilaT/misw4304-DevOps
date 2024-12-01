import logging

from database.declarative_base import open_session
from models.models import BlacklistedEmail
from sqlalchemy.exc import IntegrityError

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


class BlacklistedEmailService:

    @staticmethod
    def create_email_blacklisting(data):
        logging.debug(f'Creating email blacklisting with data: {data}')
        # with open_session() as session:
        #     try:
        #         blacklisted_email = BlacklistedEmail(
        #             email=data['email'],
        #             app_uuid=data['appUuid'],
        #             blocked_reason=data['blockedReason'],
        #             request_ip=data['requestIp']
        #         )
        #         session.add(blacklisted_email)
        #         session.commit()
        #         logging.info(f'Email blacklisted successfully: {data["email"]}')
        #     except IntegrityError as e:
        #         logging.error(f'IntegrityError while blacklisting email: {e}')
        #         return '', 400
        return {'msg': 'Email blacklisting was successfully created'}, 200

    @staticmethod
    def is_blacklisted(email):
        logging.debug(f'Checking if email is blacklisted: {email}')
        with open_session() as session:
            result = session.query(BlacklistedEmail).filter(BlacklistedEmail.email == email).first()

        if not result:
            logging.info(f'Email not blacklisted: {email}')
            return 'false', 200
        else:
            logging.info(f'Email is blacklisted: {email}, Reason: {result.blocked_reason}')
            return {'status': 'true', 'blockedReason': result.blocked_reason}, 200
