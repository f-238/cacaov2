from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, event, func, insert, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.user import User


class UserSettings(Base):
    __tablename__ = "user_settings"
    __table_args__ = (
        CheckConstraint(
            "theme_mode IN ('light', 'dark', 'system')",
            name="ck_user_settings_theme_mode",
        ),
        CheckConstraint(
            "font_size IN ('small', 'medium', 'large')",
            name="ck_user_settings_font_size",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )
    theme_mode: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        server_default=text("'system'"),
    )
    font_size: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        server_default=text("'medium'"),
    )
    primary_color: Mapped[str] = mapped_column(
        String(7),
        nullable=False,
        server_default=text("'#1f2937'"),
    )
    secondary_color: Mapped[str] = mapped_column(
        String(7),
        nullable=False,
        server_default=text("'#526075'"),
    )
    accent_color: Mapped[str] = mapped_column(
        String(7),
        nullable=False,
        server_default=text("'#f3a6ba'"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="settings")


@event.listens_for(User, "after_insert")
def create_default_settings_after_user_insert(_, connection, target: User) -> None:
    connection.execute(insert(UserSettings).values(user_id=target.id))
