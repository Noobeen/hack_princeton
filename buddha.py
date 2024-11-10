from api import Embd_key
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import TextLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
import streamlit as st
import os
from Locallm import llm #importing from locallm.py to intialize local model : llama 3.2:3B
from hist import get_session_history,store #importing from hist.py
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"]= lang # Api key imported from api.py which user can create in their own device
from gtts import gTTS


os.environ["OPENAI_API_KEY"] =Embd_key # Api key imported from api.py which user can create in their own device




### Constructing retriever for RAG ###
loader = TextLoader(file_path="Buddha.txt")
data=loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(data)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings(model="text-embedding-3-small"))

retriever = vectorstore.as_retriever()


### Contextualizing question ###
contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm,retriever,contextualize_q_prompt)



### framing question ###
qa_system_prompt = """ Buddha
"Imagine you are Buddha, a being of deep wisdom, compassion, and inner peace. You approach all questions and situations with patience, empathy, and a profound understanding of human nature and the cycles of life.

When responding, consider:

Compassionate Guidance: Offer advice with kindness, aiming to reduce suffering and promote happiness.
Equanimity and Detachment: Maintain a balanced perspective, focusing on the impermanent nature of things and encouraging a path of moderation.
Self-Reflection: Prompt self-awareness in others, encouraging them to look inward for answers and to cultivate mindfulness and awareness.
Non-Judgmental Wisdom: Respond without judgment or attachment, remaining a source of calm and steady insight.
Encouragement of Growth: Gently guide others toward personal development, peace, and enlightenment.

In every response, embody these qualities, remaining grounded in compassion, free from anger, and always inspiring others toward peace, self-knowledge, and kindness."

{context}"""

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)


## Passing to streamlit and running our chatbot 
st.title("Herschel")
Prompt= st.chat_input("Enter you queries here : ")# taking prompt for the user
if Prompt:
    st.write(f"You have sent following prompt: {Prompt}")
    ans = conversational_rag_chain.invoke(
    {"input":Prompt},
    config={
        "configurable": {"session_id": "abc"}
    },  # constructs a key "abc" in `store` so our history will be saved with key "abc"
    )["answer"]
    language = 'en'

    st.header(ans)# printing output 
    myobj = gTTS(text=ans, lang=language, slow=False)
    myobj.save("welcome.mp3")
    os.system("start welcome.mp3")
else:
    exit
