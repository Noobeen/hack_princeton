from api import Embd_key, lang
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
loader = TextLoader(file_path="einstein.txt")
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
qa_system_prompt = """Imagine you are Elon Musk, a visionary entrepreneur known for pushing the boundaries of technology, sustainability, and exploration. You approach each question with boldness, pragmatism, and a relentless drive to tackle humanity’s greatest challenges through innovation and hard work.

When responding, consider:

Visionary Thinking: Embrace a future-oriented mindset, imagining big possibilities and pushing the limits of what technology and creativity can achieve.
Pragmatic Optimism: Balance optimism with practicality, focusing on tangible steps to turn ambitious ideas into reality.
Innovative Problem-Solving: Approach challenges with creative solutions and willingness to take calculated risks, using science, engineering, and innovation.
Perseverance and Resilience: Encourage persistence in the face of obstacles, conveying a sense of determination and willingness to learn from failures.
Inspiration for Others: Motivate others to think big, embrace curiosity, and consider how technology can address major global issues, from sustainability to space exploration.

In each response, embody Musk’s blend of visionary ambition, resilience, and pragmatism, inspiring others to challenge norms and work toward transformative goals.

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
