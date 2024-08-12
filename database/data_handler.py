# database/data_handler.py
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from database.models import Credential, TikTokRequest, Hashtag, Comment, Message


class DataHandler:
    @staticmethod
    async def save_credential(username: str, password: str, session: AsyncSession):
        credential = Credential(username=username, password=password)
        session.add(credential)
        await session.commit()

    @staticmethod
    async def get_credential_by_username(username: str, session: AsyncSession):
        async with session.begin():
            stmt = select(Credential).where(Credential.username == username)
            result = await session.execute(stmt)
            credential = result.scalar()
        return credential

    @staticmethod
    async def create_tiktok_request(chat_id: int, credential: Credential, hashtags: list[str], comments: list[str],
                                    messages: list[str], session: AsyncSession):
        tiktok_request = TikTokRequest(chat_id=chat_id, credential=credential)
        session.add(tiktok_request)
        await session.flush()

        for tag in hashtags:
            session.add(Hashtag(request_id=tiktok_request.id, hashtag=tag))

        for comment in comments:
            session.add(Comment(request_id=tiktok_request.id, comment=comment))

        for msg in messages:
            session.add(Message(request_id=tiktok_request.id, message=msg))

        await session.commit()
        return tiktok_request

    @staticmethod
    async def get_all_requests(session: AsyncSession) -> List[TikTokRequest]:
        result = await session.execute(
            select(TikTokRequest).options(
                selectinload(TikTokRequest.credential),
                selectinload(TikTokRequest.hashtags),
                selectinload(TikTokRequest.comments),
                selectinload(TikTokRequest.messages)
            )
        )
        return result.scalars().all()

    @staticmethod
    async def get_request_by_id(request_id: int, session: AsyncSession) -> TikTokRequest:
        async with session.begin():
            stmt = select(TikTokRequest).options(
                selectinload(TikTokRequest.credential),
                selectinload(TikTokRequest.hashtags),
                selectinload(TikTokRequest.comments),
                selectinload(TikTokRequest.messages)
            ).where(TikTokRequest.id == request_id)

            result = await session.execute(stmt)
            request = result.scalar()
            return request
