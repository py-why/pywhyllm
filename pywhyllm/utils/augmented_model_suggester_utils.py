import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, util


def find_top_match_in_causenet(causenet_dict, variable1, variable2, threshold=0.7):
    pair_strings = [
        f"{causenet_dict[key]['causal_relation']['cause']}-{causenet_dict[key]['causal_relation']['effect']}"
        for key in causenet_dict]

    tokenized_pairs = [text.split() for text in pair_strings]
    bm25 = BM25Okapi(tokenized_pairs)

    query = variable1 + "-" + variable2
    reverse_query = variable2 + "-" + variable1
    tokenized_query = query.split()
    tokenized_reverse_query = reverse_query.split()

    combined_query = list(set(tokenized_query + tokenized_reverse_query))

    k = 5
    scores = bm25.get_scores(combined_query)
    top_k_indices = np.argsort(scores)[::-1][:k]
    candidate_pairs = [pair_strings[i] for i in top_k_indices]

    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(query, convert_to_tensor=True)
    reverse_query_embedding = model.encode(reverse_query, convert_to_tensor=True)
    candidate_embeddings = model.encode(candidate_pairs, convert_to_tensor=True)

    similarities = util.cos_sim(query_embedding, candidate_embeddings).flatten()
    reverse_similarities = util.cos_sim(reverse_query_embedding, candidate_embeddings).flatten()

    max_similarities = np.maximum(similarities, reverse_similarities)

    top_idx = np.argmax(max_similarities)
    top_similarity = max_similarities[top_idx]
    top_pair = candidate_pairs[top_idx]

    if top_similarity >= threshold:
        print(f"Best match: {top_pair} (Similarity: {top_similarity:.4f})")
        return causenet_dict[top_pair]
    else:
        print(f"No match found with similarity above {threshold} (Best similarity: {top_similarity:.4f})")
        return None


def get_source_text(causenet_query_result):
    source_text = ""
    if causenet_query_result:
        for item in causenet_query_result["sources"]:
            if item["type"] == 'wikipedia_sentence' or item["type"] == 'clueweb12_sentence':
                source_text += item["payload"]["sentence"] + " "

    return source_text


def split_data_and_create_vectorstore_retriever(source_text):
    document = Document(page_content=source_text)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )
    splits = text_splitter.split_documents([document])

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory="./chroma_db"  # Optional: Save to disk for reuse
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    return retriever


def query_llm(variable1, variable2, source_text=None, retriever=None):
    llm = OpenAI()
    if source_text:
        system_prompt = """You are a helpful assistant for causal reasoning.

    Context: {context}
    """
    else:
        system_prompt = """You are a helpful assistant for causal reasoning.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    query = f"""Which cause-and-effect-relationship is more likely? Provide reasoning and you must give your final answer (A, B, or C) in <answer> </answer> tags with the letter only.
            A. {variable1} causes {variable2} B. {variable2} causes {variable1} C. neither {variable1} nor {variable2} cause each other."""

    if source_text:
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        response = rag_chain.invoke({"input": query})
        return response['answer']


    else:
        default_chain = prompt | llm
        response = default_chain.invoke({"input": query})
        return response
