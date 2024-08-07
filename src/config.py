import os
import shutil
import gradio as gr
from langchain_community.document_loaders import DirectoryLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.indexes import VectorstoreIndexCreator


template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer or the question is not related to the provided context, just say that you don't know, don't try to make up an answer.
Use 10 sentences maximum, add bullet points where applicable and keep the answer as reasonable as possible.
Get idea from below Examples:
Examples:
"question": What does the study "Disrupting Industries With Blockchain: The Industry, Venture Capital Funding, and Regional Distribution of Blockchain Ventures" investigate and what are its key findings?",
"answer": "The study investigates the emerging landscape of blockchain business applications by analyzing their presence across industries, venture capital funding, and regional distribution. It uses data from four venture databases to explore the diffusion of blockchain technology. Key findings include:
1- Blockchain startups are present across all industry segments, with the most significant representation in the Finance & Insurance and Information & Communication industries.
2- These industries are also the primary recipients of venture capital funding, though blockchain startups exist in various sectors.
3- The regional distribution analysis identifies the US and UK as leading geographical clusters for blockchain ventures."
"question": "How to play snooker?"
"answer": "I don't know the answer. The question is not relevant to the provided context."
"question": "Who is Nicolas Poran?"
"answer": "I don't know the answer. The question is not relevant to the provided context."

You will know answer the questions from the provided context. If the questions is not relevant, just say you don't know the answer.
{context}
Question: {question}
Helpful Answer:"""

# Function to create the retriever and QA chain
def setup_qa_system(csv_folder_path):
    """
    Set up the QA system by creating a retriever and QA chain using CSV files.

    Args:
        csv_folder_path (str): Path to the folder containing CSV files.

    Returns:
        qa_chain: The initialized QA chain object.
    """
    loader = DirectoryLoader(csv_folder_path, glob="**/*.csv",
                             loader_cls=CSVLoader, loader_kwargs={'encoding': 'utf-8'})
    embedding_model = OpenAIEmbeddings()
    index_creator = VectorstoreIndexCreator(embedding=embedding_model)
    docsearch = index_creator.from_loaders([loader])
    retriever = docsearch.vectorstore.as_retriever(
        search_type="mmr", search_kwargs={'k': 1})
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
    chain_type_kwargs = {"prompt": QA_CHAIN_PROMPT}
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)
    qa_chain = RetrievalQA.from_chain_type(
        llm, chain_type="stuff", retriever=retriever, return_source_documents=True, chain_type_kwargs=chain_type_kwargs)
    return qa_chain

# Function to handle file uploads
def upload_files(files):
    """
    Handle the upload and storage of files, specifically CSV files.

    Args:
        files (list): List of file objects to be uploaded.

    Returns:
        str: The path to the folder where the files are stored.
    """
    folder_path = 'csv_data'
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)  # Clear existing directory
    os.makedirs(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file.name)
        shutil.move(file.name, file_path)
    return folder_path

# Function to handle queries
def query_data(question):
    """
    Handle user queries by passing the question to the QA system.

    Args:
        question (str): The user's query question.

    Returns:
        str: The answer retrieved by the QA system.
    """
    global qa_chain
    if qa_chain is None:
        return "QA system is not initialized. Please upload CSV files first."
    result = qa_chain({"query": question})
    answer = result["result"]
    return answer

# Initialize the QA system variable
qa_chain = None

# Gradio interface for file upload
def file_upload_interface(files):
    """
    Interface for uploading files and initializing the QA system.

    Args:
        files (list): List of file objects to be uploaded.

    Returns:
        str: Status message indicating the files are uploaded and QA system is initialized.
    """
    global qa_chain
    folder_path = upload_files(files)
    qa_chain = setup_qa_system(folder_path)
    return "Files uploaded and QA system initialized. You can now ask questions."