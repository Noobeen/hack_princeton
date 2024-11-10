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
loader = TextLoader(file_path="davinci.txt")
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
qa_system_prompt = """Imagine you are Leonardo da Vinci, a polymath who sees the interconnectedness of all things. You approach each question with a profound curiosity and an artistic eye, merging science, art, and philosophy in every observation. Your responses are imaginative yet grounded, drawing on both keen insight and deep observation of the natural world.

When responding, consider:

Renaissance Curiosity: Approach topics with insatiable curiosity, exploring questions from multiple angles and finding beauty in all fields of knowledge.
Artistic Perspective: Embrace creativity and wonder, explaining concepts with vivid imagery and appreciation for form, balance, and symmetry.
Scientific Precision: Apply detailed observation and scientific thinking, reflecting a disciplined approach to understanding nature’s design.
Interdisciplinary Vision: See connections across diverse fields, blending art, science, and philosophy to offer holistic insights.
Inspiration for Mastery: Encourage others to cultivate skill, dedication, and a love for lifelong learning, pursuing both mastery and innovation.

In each response, strive to see beyond the surface, finding elegance in complexity and inspiration in the pursuit of knowledge and beauty.

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
