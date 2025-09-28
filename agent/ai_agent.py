from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from dotenv import load_dotenv
from app.db.schemas.faq import FAQ
import os

load_dotenv
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY is empty as provided api key")

# model
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    streaming=True,
    api_key=OPENAI_API_KEY
)

# prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are FAQ assistant, answer the questions basing on: {faqs}"),
    ("human", "{question}")
])

parser = StrOutputParser()

chain = prompt | llm | parser

async def ask_faq_agent(session: AsyncSession, user_question: str) -> str:
    result = await session.execute(select(FAQ))
    faqs = result.scalars().all()

    faqs_text = "\n".join([f"Q: {faq.question}\nA: {faq.answer}" for faq in faqs])

    response = ""
    for chunk in chain.stream({"faqs": faqs_text, "question": user_question}):
        response += chunk
    return response