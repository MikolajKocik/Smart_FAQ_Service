from app.repositories.faq_repository import FaqRepository
from app.dtos.faq_create_dto import FaqCreate
from app.dtos.faq_read_dto import FaqRead
from app.models.faq import FaqDomain
from app.exceptions.faq_not_found import FaqNotFoundError
from app.exceptions.faq_already_exists import FaqAlreadyExistsError
from app.exceptions.faq_bad_request import FaqBadRequestError
from typing import List

class FaqService():
    def __init__(self, repo: FaqRepository):
        self.repo=repo

    async def create_faq(self, faq_dto: FaqCreate) -> FaqDomain:
        faq_by_question = await self.repo.get_by_question(faq_dto.question)
        if faq_by_question:
            raise FaqAlreadyExistsError("FAQ with this question already exists.")
        if faq_dto.question is None or faq_dto.question.strip() == "":
            raise FaqBadRequestError("Question cannot be empty value")
        if faq_dto.answer is None or faq_dto.answer.strip() == "":
            raise FaqBadRequestError("Answer cannot be empty value")
        
        faq_domain = FaqDomain(question=faq_dto.question, answer=faq_dto.answer)

        created_faq = await self.repo.add(faq_domain)
        return created_faq
    
    async def get_faq(self, faq_id: int) -> FaqDomain:
        faq_by_id = await self.repo.get_by_id(faq_id)
        if not faq_by_id:
            raise FaqNotFoundError(f"Faq not found with id:{faq_id}")

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
        faq_to_remove = await self.repo.get_by_id(faq_id)
        if not faq_to_remove:
            raise FaqNotFoundError(f"Faq not found with id:{faq_id}")
        
        await self.repo.remove(faq_to_remove)
        return None
