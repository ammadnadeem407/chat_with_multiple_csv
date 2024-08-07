import os
import shutil
import gradio as gr
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.indexes import VectorstoreIndexCreator
from src import setup_qa_system, query_data, upload_files, file_upload_interface, template

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_KEY')


# Gradio interface components
upload_interface = gr.Interface(
    fn=file_upload_interface,
    inputs=gr.Files(label="Upload CSV Files"),
    outputs="text",
    title="Upload CSV Files"
)

qa_interface = gr.Interface(
    fn=query_data,
    inputs=gr.Textbox(lines=2, placeholder="Enter your question here..."),
    outputs="text",
    title="Question Answering Interface"
)

# Combine both interfaces
app = gr.Blocks()
with app:
    gr.Markdown("# CSV File Upload and Question Answering System")
    with gr.Tab("Upload CSV Files"):
        upload_interface.render()
    with gr.Tab("Ask Questions"):
        qa_interface.render()

app.launch()
