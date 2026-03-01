from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
        default=None,
    )

    # one-to-many relationship, Creator(User) points to own all posts
    # Enables things like author.post -> get the posts
    posts: Mapped[list[Post]] = relationship(back_populates="author")

    @property
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        # Enable lookups using user_id, increases write overhead
        # but should be worth it
        index=True,
    )
    date_posted: Mapped[datetime] = mapped_column(
        # Good habit to add timezone.
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    # Many-to-one relationship, posts point back to the creator(User)
    # Enables things like post.author -> get the author
    author: Mapped[User] = relationship(back_populates="posts")
