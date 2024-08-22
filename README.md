# BackendAssignment
# Document Processing Service & RAG Chatbot Service

## Overview

This project implements two core services:
1. **Document Processing Service:** Handles the uploading, processing, and retrieval of documents. It extracts text from various file types, generates embeddings using a transformer model, and stores these embeddings along with metadata in both SQLAlchemy and ChromaDB.
2. **RAG Chatbot Service:** Provides a chatbot interface that interacts with the Document Processing Service to retrieve and process documents in real-time.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/SameerPatwari/BackendAssignment.git
cd BackendAssignment
```
### 2. Set Up the Virtual Environment
- Create virtual environment
```bash
python -m venv venv
```
- Activate the virtual environment:
```bash
venv\Scripts\activate
```
### 3. Install the Dependencies
```bash
pip install -r requirements.txt
```
### 5. Run the Application
```bash
python app.py
```
### 6. Test the API Endpoints
- By using Postman we can test the API endpoints. The documentation provided below outlines all available endpoints.
### 7. Running the Chatbot Service
- To run the Chatbot Service, execute:
```bash
python chatbot_service.py
```

## API Documentation
## Base URL

The base URL for all endpoints is:http://localhost:5000


## Endpoints

### 1. **Upload Document**

- **Endpoint**: `/upload`
- **Method**: `POST`
- **Description**: Uploads a document, extracts text from it, generates embeddings, and stores the document with metadata.
- **Request**:
  - **Content-Type**: `multipart/form-data`
  - **Form-data**:
    - `file` (required): The document file to upload.
- **Response**:
  - **201 Created**:
    ```json
    {
      "message": "File processed",
      "asset_id": "<unique_id>"
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "error": "<error_message>"
    }
    ```

### 2. **Update Document**

- **Endpoint**: `/update/<asset_id>`
- **Method**: `PUT`
- **Description**: Updates the document with new embeddings and metadata using its `asset_id`.
- **Request**:
  - **Content-Type**: `multipart/form-data`
  - **Form-data**:
    - `file` (required): The updated document file.
- **Response**:
  - **200 OK**:
    ```json
    {
      "message": "Document updated successfully"
    }
    ```
  - **400 Bad Request**:
    ```json
    {
      "error": "<error_message>"
    }
    ```

### 3. **Get Document**

- **Endpoint**: `/document/<asset_id>`
- **Method**: `GET`
- **Description**: Retrieves document metadata and embeddings by its `asset_id`.
- **Response**:
  - **200 OK**:
    ```json
    {
      "document": {
        "asset_id": "<id>",
        "document_name": "<name>",
        "file_type": "<type>",
        "id": "<id>",
        "timestamp": "<timestamp>"
      },
      "metadata": { ... }
    }
    ```
  - **404 Not Found**:
    ```json
    {
      "error": "Document not found in SQLAlchemy"
    }
    ```
  - **500 Internal Server Error**:
    ```json
    {
      "error": "Failed to query ChromaDB"
    }
    ```

### 4. **Delete Document**

- **Endpoint**: `/document/<asset_id>`
- **Method**: `DELETE`
- **Description**: Deletes the document by its `asset_id`.
- **Response**:
  - **200 OK**:
    ```json
    {
      "message": "Document deleted successfully"
    }
    ```
  - **404 Not Found**:
    ```json
    {
      "error": "Document not found in SQLAlchemy"
    }
    ```

## Error Handling

The API returns standard HTTP status codes and error messages to indicate issues. We can check the `error` field in the response for details on what went wrong.

## Potential Improvements
- Improving error handling across both services, especially in interactions with ChromaDB, to make debugging easier and provide more informative error messages.
- Implementing unit testing and integration testing to ensure that all components are working correctly, especially after any changes.
- Improving logging to get more insights on the flow of data and the interactions between services.
- After the backend system has been made, giving it a front-end interface would make it user friendly.

## Integration Issue: Document Processing Service and RAG Chatbot Service
While integrating the Document Processing Service and the RAG Chatbot Service, there was an issue encountered where the 'my_collection' was not found when running 'chatbot_service.py'. This occurred despite the 'app.py' working fine, as verified by the logger.
### Summary of the Issue:
- The 'app.py' service successfully created and accessed the my_collection in ChromaDB, as confirmed by the logger.
- However, when running 'chatbot_service.py', the collection 'my_collection' could not be found, leading to errors during the execution.


