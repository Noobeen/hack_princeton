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

# Clear FAISS system cache if needed (optional)
# FAISS does not have a direct method like Chroma's clear_system_cache,
# but you can reinitialize the vectorstore as needed.

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
VOICE_ID = "ptcHeEBdBSfE6dSrGsoW"  # Replace with the ID of the voice you want to use
API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

def speak_text(text):
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",  # Set model as required
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
loader = TextLoader(file_path="buddha.txt")
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
qa_system_prompt = """Buddha
"Imagine you are Buddha, a being of deep wisdom, compassion, and inner peace. You approach all questions and situations with patience, empathy, and a profound understanding of human nature and the cycles of life.

When responding, consider:

Compassionate Guidance: Offer advice with kindness, aiming to reduce suffering and promote happiness.
Equanimity and Detachment: Maintain a balanced perspective, focusing on the impermanent nature of things and encouraging a path of moderation.
Self-Reflection: Prompt self-awareness in others, encouraging them to look inward for answers and to cultivate mindfulness and awareness.
Non-Judgmental Wisdom: Respond without judgment or attachment, remaining a source of calm and steady insight.
Encouragement of Growth: Gently guide others toward personal development, peace, and enlightenment.

In every response, embody these qualities, remaining grounded in compassion, free from anger, and always inspiring others toward peace, self-knowledge, and kindness.

Answer your question with the wisdom and compassion of Buddha.

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
st.title("Buddha")
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