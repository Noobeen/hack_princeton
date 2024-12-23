from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.vectorstores import FAISS  # Updated import for FAISS
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import TextLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st
import os
import tempfile
import requests
from hist import get_session_history, store  # importing from hist.py

# Accessing secrets
Embd_key = st.secrets["OPENAI_API_KEY"]
key = st.secrets["ELEVEN_API_KEY"]
os.environ["OPENAI_API_KEY"] = Embd_key  # API key imported from secrets

# Initialize the Language Model
llm = ChatOpenAI(
    model="gpt-4",  # Corrected model name from "gpt-4o" to "gpt-4"
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Set up your API key and endpoint for ElevenLabs TTS
API_KEY = key
VOICE_ID = "nZptPqACGe9qLrBchcWI"  
API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

def speak_text(text):
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1", 
    }

    # Send request to ElevenLabs API
    response = requests.post(API_URL, json=data, headers=headers)
    if response.status_code == 200:
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name

            # Play the audio in Streamlit
            st.audio(temp_file_path)

            # Optional: Delete the file after playing
            os.remove(temp_file_path)
        except Exception as e:
            st.error(f"Error playing audio: {e}")
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

### Constructing retriever for RAG ###
loader = TextLoader(file_path="gandi.txt")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(data)

# Initialize FAISS vectorstore
embedding = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.from_documents(documents=splits, embedding=embedding)

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
    llm, retriever, contextualize_q_prompt
)

### Framing question ###
qa_system_prompt = """Imagine you are Mahatma Gandhi, a leader known for your unwavering commitment to truth, nonviolence, and compassion. You approach each question with humility and a desire to inspire peace and justice, valuing patience and understanding above all else.

When responding, consider:

Nonviolent Approach: Address all questions with a focus on empathy, nonviolence, and peaceful resolution, aiming to uplift and unify.
Commitment to Truth: Embrace honesty and integrity, encouraging others to live authentically and with moral clarity.
Respect for Humanity: Show deep compassion for all people, emphasizing unity and understanding in the face of differences.
Self-Discipline and Simplicity: Encourage simplicity, humility, and self-discipline, promoting values that reflect inner strength and restraint.
Empowerment and Social Justice: Inspire courage and resilience in the pursuit of justice, advocating for equality, freedom, and compassion for all.

In each response, reflect Gandhi’s commitment to nonviolence, truth, and service, offering wisdom that seeks to guide others toward peace and positive change.


Answer should be in plain text without any text formatting.
Answer should be not more than a paragraph.

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

## Passing to Streamlit and running our chatbot 
st.title("Gandhi")
Prompt = st.chat_input("Enter your queries here : ")  # taking prompt for the user
if Prompt:
    st.write(f"You have sent the following prompt: {Prompt}")
    ans = conversational_rag_chain.invoke(
        {"input": Prompt},
        config={
            "configurable": {"session_id": "abc"}
        },  # constructs a key "abc" in `store` so our history will be saved with key "abc"
    )["answer"]
    language = 'en'

    st.header(ans)  # printing output 
    speak_text(ans)
else:
    st.write("Please enter a query to start the conversation.")
