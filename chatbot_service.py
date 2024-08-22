import chromadb
from flask import Flask, request, jsonify
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
import uuid
from chromadb.config import Settings

app = Flask(__name__)

# Initializing ChromaDB client
client = chromadb.Client(Settings())

# Checking existing collections
collection_name = "my_collection"

try:
    collection = client.get_collection(name=collection_name)
except ValueError:
    raise ValueError(f"Collection {collection_name} does not exist.")

collection = client.get_collection(name=collection_name)

# Initializing LangChain components
embedding_model = HuggingFaceEmbeddings()
vectorstore = Chroma(client=client, embedding_model=embedding_model)
retriever = vectorstore.as_retriever()

# Creating a ConversationalRetrievalChain
chain = ConversationalRetrievalChain(retriever=retriever)

# Initializing chat sessions storage
chat_sessions = {}

@app.route('/api/chat/start', methods=['POST'])
def start_chat():
    data = request.json
    asset_id = data['asset_id']
    chat_thread_id = str(uuid.uuid4())
    chat_sessions[chat_thread_id] = {'asset_id': asset_id, 'messages': []}
    return jsonify({"chat_thread_id": chat_thread_id}), 200

@app.route('/api/chat/message', methods=['POST'])
def chat_message():
    data = request.json
    chat_thread_id = data['chat_thread_id']
    user_message = data['message']
    
    if chat_thread_id not in chat_sessions:
        return jsonify({"error": "Invalid chat thread ID"}), 404
    
    asset_id = chat_sessions[chat_thread_id]['asset_id']
    results = collection.query(
        query_texts=[user_message],
        filter={"asset_id": asset_id},
        top_k=1
    )
    
    response = chain.run(input=user_message, context=results)
    chat_sessions[chat_thread_id]['messages'].append({
        'user_message': user_message,
        'agent_response': response
    })
    
    return jsonify({"response": response}), 200

@app.route('/api/chat/history', methods=['GET'])
def chat_history():
    chat_thread_id = request.args.get('chat_thread_id')
    
    if chat_thread_id not in chat_sessions:
        return jsonify({"error": "Invalid chat thread ID"}), 404
    
    return jsonify({"history": chat_sessions[chat_thread_id]['messages']}), 200

if __name__ == '__main__':
    app.run(debug=True)
