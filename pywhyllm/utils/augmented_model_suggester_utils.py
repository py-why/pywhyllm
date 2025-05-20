import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer, util


def find_top_match_in_causenet(causenet_dict, variable1, variable2):
    # Sample dictionary
    pair_strings = [
        f"{causenet_dict[key]['causal_relation']['cause']}-{causenet_dict[key]['causal_relation']['effect']}"
        for key in causenet_dict]

    # Tokenize for BM25
    tokenized_pairs = [text.split() for text in pair_strings]
    bm25 = BM25Okapi(tokenized_pairs)

    # Query
    query = variable1 + "-" + variable2
    tokenized_query = query.split()

    # Get top-k candidates using BM25
    k = 5
    scores = bm25.get_scores(tokenized_query)
    top_k_indices = np.argsort(scores)[::-1][:k]
    candidate_pairs = [pair_strings[i] for i in top_k_indices]

    # Apply SBERT to candidates
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(query, convert_to_tensor=True)
    candidate_embeddings = model.encode(candidate_pairs, convert_to_tensor=True)
    similarities = util.cos_sim(query_embedding, candidate_embeddings).flatten()
    top_idx = top_k_indices[np.argmax(similarities)]
    top_pair = pair_strings[top_idx]
    print(f"Best match: {top_pair}")
    result = causenet_dict[top_pair]
    return result


def get_source_text(causenet_query_result):
    source_text = ""

    for item in causenet_query_result["sources"]:
        if item["type"] == 'wikipedia_sentence' or item["type"] == 'clueweb12_sentence':
            source_text += item["payload"]["sentence"] + " "

    return source_text


def split_data_and_create_vectorstore_retriever(source_text):
    document = Document(page_content=source_text)

    # Initialize the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,  # Adjust chunk size as needed
        chunk_overlap=20  # Overlap for context
    )
    # Split the documents
    splits = text_splitter.split_documents([document])

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create a vector store from the document splits
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory="./chroma_db"  # Optional: Save to disk for reuse
    )

    # Create a retriever from the vector store
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}  # Retrieve top 5 relevant chunks
    )

    return retriever


def query_llm(source_text, variable1, variable2, retriever):
    # Initialize the language model
    llm = ChatOpenAI(model="gpt-4")

    if source_text:
        system_prompt = """You are a helpful assistant for causal reasoning.

    Context: {context}
    """
    else:
        system_prompt = """You are a helpful assistant for causal reasoning.
    """

    # prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    query = f"""Which cause-and-effect-relationship is more likely? Provide reasoning and you must give your final answer (A, B, or C) in <answer> </answer> tags with the letter only.
            A. {variable1} causes {variable2} B. {variable2} causes {variable1} C. neither {variable1} nor {variable2} cause each other."""

    # Define the system prompt
    if source_text:
        # Create a document chain to combine retrieved documents
        question_answer_chain = create_stuff_documents_chain(llm, prompt)

        # Create the RAG chain
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        response = rag_chain.invoke({"input": query})
        return response['answer']


    else:
        default_chain = prompt | llm
        response = default_chain.invoke({"input": query})
        return response.content
