from ..repositories.faq_repository import FaqRepository
from ..dtos.faq_create_dto import FaqCreate
from ..dtos.faq_read_dto import FaqRead
from ..models.faq import FaqDomain
from ..exceptions.faq_not_found import FaqNotFoundError
from typing import List

class FaqService():
    def __init__(self, repo: FaqRepository):
        self.repo=repo

    async def create_faq(self, faq_dto: FaqCreate) -> FaqDomain:
        faq_by_question = await self.repo.get_by_question(faq_dto.question)
        if faq_by_question:
            raise ValueError("FAQ with this question already exists.")
        
        faq_domain = FaqDomain(id_=None, question=faq_dto.question, answer=faq_dto.answer)

        created_faq = await self.repo.add(faq_domain)
        return created_faq
    
    async def get_faq(self, faq_dto: FaqRead) -> FaqDomain:
        faq_by_id = await self.repo.get_by_id(faq_dto.id)
        if not faq_by_id:
            raise FaqNotFoundError(f"Faq not found with id:{faq_dto.id}")

        return faq_by_id

    async def get_faqs(self) -> List[FaqDomain]:
        faqs = await self.repo.get_faqs()
        return faqs
    
    async def faq_update(self, faq_dto: FaqRead) -> None:
        faq_by_id = await self.repo.get_by_id(faq_dto.id)
        if not faq_by_id:
            raise FaqNotFoundError(f"Faq not found with id:{faq_dto.id}")
        
        faq_domain = FaqDomain(id_=faq_dto.id, question=faq_dto.question, answer=faq_dto.answer)
        faq_modified = await self.repo.update(faq_domain)
        return faq_modified

    async def faq_remove(self, faq_id: int) -> None:
        faq_by_id = await self.repo.get_by_id(faq_id)
        if not faq_by_id:
            raise FaqNotFoundError(f"Faq not found with id:{faq_id}")
        
        faq_to_remove = await self.repo.remove(faq_by_id)
        return None
   
# AI
# ask
