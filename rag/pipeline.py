from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.documents import Document

from rag.llm import get_llm

_SYSTEM_PROMPT = """You are a demographic intelligence assistant helping policy analysts, researchers, and planners understand population trends across Australia and OECD peer countries.

Answer using ONLY the context provided below. Cite each claim with the source organisation and year in parentheses — e.g. (ABS, 2022). If the data is absent from the context, say so clearly rather than speculating.

Context:
{context}"""

_PROMPT = ChatPromptTemplate.from_messages([
    ("system", _SYSTEM_PROMPT),
    ("human", "{question}"),
])


def _format_docs(docs: list[Document]) -> str:
    if not docs:
        return ""
    parts = []
    for doc in docs:
        meta = doc.metadata
        header = f"[{meta.get('source_org', 'Unknown')} — {meta.get('country', '?')} | {meta.get('publication', '')} ({meta.get('year', '?')})]"
        parts.append(f"{header}\n{doc.page_content}")
    return "\n\n---\n\n".join(parts)


def build_chain(retriever, streaming: bool = False):
    llm = get_llm(streaming=streaming)
    return (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | _PROMPT
        | llm
        | StrOutputParser()
    )


def build_chain_with_sources(retriever, streaming: bool = False):
    llm = get_llm(streaming=streaming)

    answer_chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | _PROMPT
        | llm
        | StrOutputParser()
    )

    return RunnableParallel(
        answer=answer_chain,
        sources=retriever,
    )
