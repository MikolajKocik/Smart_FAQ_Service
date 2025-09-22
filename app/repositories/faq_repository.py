from typing import Optional, List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.faq import FaqDomain
from ..db.schemas.faq import FAQ
from ..exceptions.faq_not_found import FaqNotFoundError

class FaqRepository:
    def __init__(self, session: AsyncSession):
        self.session=session

    async def get_faqs(self) -> List[FaqDomain]:
        query = await self.session.execute(
            select(FAQ)
        )
        return query.scalars().all() or [] 

    async def get_by_id(self, faq_id: int) -> Optional[FaqDomain]:
        query = await self.session.execute(
            select(FAQ).where(FAQ.id == faq_id)
        )
        faq_sql = query.scalar_one_or_none()

        if faq_sql:
            return FaqDomain(
                id=faq_sql.id,
                question=faq_sql.question,
                answer=faq_sql.answer
            )
        return None
    
    async def get_by_question(self, question: str) -> Optional[FaqDomain]:
        query = await self.session.execute(
            select(FAQ).where(FAQ.question == question)
        )
        faq_sql = query.scalar_one_or_none()
        if faq_sql:
            return FaqDomain(
                id=faq_sql.id,
                question=faq_sql.question,
                answer=faq_sql.answer
            )
        return None
        
    async def add(self, faq_domain: FaqDomain) -> FaqDomain:
        faq_sql=FAQ(
            question=faq_domain.question,
            answer=faq_domain.answer
        )
        self.session.add(faq_sql)
        await self.session.commit()
        await self.session.refresh(faq_sql)

        return FaqDomain(
            id_=faq_sql.id,
            question=faq_sql.question,
            answer=faq_sql.answer
        )   
    
    async def update(self, faq_domain: FaqDomain) -> None:
        faq_sql = await self.session.get(FAQ, faq_domain.id)
        if not faq_sql:
            raise FaqNotFoundError(f"FAQ with id {faq_domain.id} not found")
        
        faq_sql.question=faq_domain.question,
        faq_sql.answer=faq_domain.answer
        
        await self.session.commit()
        await self.session.refresh(faq_sql)
        return None
    
    async def remove(self, faq_sql: FAQ) -> None:
        await self.session.delete(faq_sql)
        await self.session.commit()
        return None