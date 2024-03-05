# from gpt4all import GPT4All
import time
from typing import List

model_name = 'llama-2-7b-chat.Q4_0.gguf'
model_path = './models/' 
pdf_path = "./materials/iGridd_Demo_book.pdf"
index_path = "./index/iGridd_Demo_book_index"

# ##### LANGCHAIN #####
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp #,GPT4All
from langchain.chains import LLMChain, ConversationChain, ConversationalRetrievalChain
# Memory
from langchain.schema import ( SystemMessage, messages_to_dict )
from langchain.memory import ConversationBufferMemory
# Loaders
from langchain_community.document_loaders import PyPDFLoader #UnstructuredURLLoader
from langchain_community.document_loaders.merge import MergedDataLoader
# Enbeddings
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_history_aware_retriever
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains import create_retrieval_chain

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

# Functions
def initialize_embeddings() -> GPT4AllEmbeddings:
    return GPT4AllEmbeddings(model_path=model_path, model_name=model_name)

def load_documents() -> List:
    loader_pdf = PyPDFLoader(pdf_path)
    loader = MergedDataLoader(loaders=[loader_pdf])
    return loader.load()

def split_chunks(sources: List) -> List:
    chunks = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=32)
    for chunk in splitter.split_documents(sources):
        chunks.append(chunk)
    return chunks

def generate_index(chunks: List, embeddings: GPT4AllEmbeddings) -> FAISS:
    texts = [doc.page_content for doc in chunks]
    metadatas = [doc.metadata for doc in chunks]
    return FAISS.from_texts(texts, embeddings, metadatas=metadatas)
#   vector = FAISS.from_documents(chunks, embeddings)

local_path = (
    model_path + model_name
)

# Callbacks support token-wise streaming
callbacks = [StreamingStdOutCallbackHandler()]

# Verbose is required to pass to the callback manager
# llm = GPT4All(model=localp_path, callbacks=callbacks, verbose=True)
llm = LlamaCpp(model_path=local_path, callbacks=callbacks, verbose=True)

# If you want to use a custom model add the backend parameter
# Check https://docs.gpt4all.io/gpt4all_python.html for supported backends
# llm = GPT4All(model=local_path, backend="gptj", callbacks=callbacks, verbose=True)

# 3
# embeddings = initialize_embeddings()
# # ###   Create indexes for documents (comment everithing else when running these for other docs)
# sources = load_documents()
# chunks = split_chunks(sources)
# # vectorstore = generate_index(chunks, embeddings)
# # vectorstore.save_local(index_path)

# # ###   Load the saved indexex of documents (To uncomment for ConversationalRetrievalChain)
# index = FAISS.load_local(index_path, embeddings)

# retriever = index.as_retriever()

prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content="""You are a helpful assistant and travel guide.
            You can also engage in some casual talk, like answering greetings and simple questions like "How/Who are you?". 
            At the beginning of a conversation in your first message, introduce yourself. 
            DO NOT COMPLETE THE SENTENCE!
            ONLY answer the user's questions regarding travelling. If you do not know how to answer, reply by saying you do not know. Do not reply to any irrelevant questions."""
        ),  # The persistent system prompt
        MessagesPlaceholder(
            variable_name="chat_history"
        ),  # Where the memory will be stored.
        HumanMessagePromptTemplate.from_template(
            "{human_input}"
        ),  # Where the human input will injected
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, ai_prefix="ASSISTANT:")

# 1
llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=True, memory=memory)
# 2
# conv_retr_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=index.as_retriever(), max_tokens_limit=400, verbose=True, memory=memory)
# 3      Create a retriever that gets the relevant document sections that could answer the question
# prompt = ChatPromptTemplate.from_messages([
#     MessagesPlaceholder(variable_name="chat_history"),
#     ("user", "{input}"),
#     ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
# ])
# retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
# #       Create the retrical chain that answers the question based on the retrieved document sections
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "Answer the user's questions based on the below context:\n\n{context}"),
#     MessagesPlaceholder(variable_name="chat_history"),
#     ("user", "{input}"),
# ])
# document_chain = create_stuff_documents_chain(llm, prompt)
# retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)

def callLLM(user_message, past_user_inputs=[], generated_responses=[]):
    start_time = time.time()
    
    # 0. TEST
    # response = "test"
    # 1
    response = llm_chain.predict(human_input=user_message)
    # Print each word as it is generated
    start_markers = ["CHATBOT:", "Bot:", "AI:", "ASSISTANT:"]
    end_markers = ["USER:", "HUMAN:"]
    extracted_section = response

    for start_marker in start_markers:
        start_index = extracted_section.lower().find(start_marker.lower())
        if start_index != -1:
            extracted_section = extracted_section[start_index + len(start_marker):]
            break
        
    if extracted_section:
        start_index = 0
        start_index = ""
        
    for end_marker in end_markers:
        end_index = extracted_section.lower().find(end_marker.lower())
        if end_index != -1:
            extracted_section = extracted_section[:end_index]
            break

    # If none of the markers are found, use the entire response
    if extracted_section is None:
        extracted_section = response
    else:
        response = extracted_section

    # 3. Print the extracted section
    print("-------")
    print("extracted response: ", extracted_section)
    print("-------")
    # 2
    # response = conv_retr_chain.invoke(user_message)
    # 3
    # response = retrieval_chain.invoke({"input": user_message, "chat_history": memory.chat_memory.messages}) # memory is empty -> not reliant
    if llm_chain.memory.chat_memory.messages:
        llm_chain.memory.chat_memory.messages.pop()
    if extracted_section.strip():
        llm_chain.memory.chat_memory.add_ai_message(extracted_section)

    end_time = time.time()
    latency = end_time - start_time
    print(f"Latency: {latency} seconds")
    print("-------")
    print("Response: ", str(response))
    print("-------")
    # current_memory = messages_to_dict(llm_chain.memory.chat_memory.messages)
    # print("Current Memory: ", current_memory)
    # 2 & 3
    # return response['answer']
    return response
