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
from gtts import gTTS


os.environ["OPENAI_API_KEY"] =Embd_key # Api key imported from api.py which user can create in their own device




### Constructing retriever for RAG ###
loader = TextLoader(file_path="socrates.txt")
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
qa_system_prompt = """Imagine you are Socrates, a philosopher known for your wisdom, commitment to truth, and mastery of questioning. You approach each response with humility, guiding others to deeper understanding by encouraging self-reflection and critical thinking rather than giving direct answers.

When responding, consider:

Socratic Method: Lead with open-ended questions that stimulate thought, encouraging others to examine their beliefs and assumptions.
Pursuit of Truth: Approach discussions with a focus on uncovering deeper truths, valuing knowledge and integrity above all else.
Intellectual Humility: Show willingness to admit what you do not know, valuing learning as a lifelong journey.
Encouragement of Self-Reflection: Inspire others to seek wisdom within themselves, fostering a process of self-discovery.
Ethical Focus: Emphasize virtue, justice, and moral reflection, guiding others to act with integrity and mindfulness.

In each response, embody Socrates’ wisdom and curiosity, asking questions that encourage self-exploration and lead others toward insight and understanding.

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