import os
import constants

os.environ["OPENAI_API_KEY"] = constants.API_SECRET_KEY


from langchain.document_loaders import WebBaseLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

loader = WebBaseLoader("https://www.artofmarketing.org/marketing-2/core-concepts-of-marketing-marketing-management/13373")
data = loader.load()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
# split the loaded data with the created splitter - chunk size 500
all_splits = text_splitter.split_documents(data)

# embed the content of the documents and store them in the vector store
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())


question = "As a marketing student summarise all the core marketing concepts in a few bullet points ?"

template = """You are a helpful marketing advisor, Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
You can write long paragraphs depending on the question no need to be concise. 
Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}
Helpful Answer:"""

QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
# docs = vectorstore.similarity_search(question)

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm,retriever=vectorstore.as_retriever(),chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}, return_source_documents=True)
qa_chain({"query": question})

retriever = vectorstore.as_retriever()
chat = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

result = qa_chain({"query": question})
print(result['result'])
print(result['source_documents'][0])
# index = VectorstoreIndexCreator().from_loaders([loader])

# print(index.query("What is Task Decomposition?"))