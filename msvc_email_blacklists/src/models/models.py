import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from msvc_email_blacklists.src.database.declarative_base import Base

class BlacklistedEmail(Base):
    __tablename__ = 'blacklisted_email'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = Column(String(length=255), nullable=False)
    app_uuid = Column(String, nullable=False)
    blocked_reason = Column(String(length=255), nullable=True)

    request_ip = Column(String, nullable=False)
    request_timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': str(self.id),
            'email': self.email,
            'appUuid': str(self.app_uuid),
            'blockedReason': self.blocked_reason,
            'requestIp': self.request_ip,
            'requestTimestamp': self.request_timestamp,
        }
