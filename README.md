# CSV Query System with LangChain and OpenAI

This project enables efficient querying of CSV files using the LangChain library and OpenAI GPT-3.5 turbo model. The source code loads, indexes, and retrieves data from CSV files, providing accurate responses to relevant queries.

## Project Overview

1. **Loading CSV Files**
   - Utilizes LangChain's `DirectoryLoader` class to load all CSV files in a specified directory.
2. **Creating Vector Indexes**
   - Uses the `VectorIndexStore` class of LangChain to create vector indexes with OpenAI embeddings.
3. **Retrieval and Query Execution**
   - Implements the `RetrievalQA` chain, integrating OpenAI GPT-3.5 turbo model and prompt templates for efficient and accurate query responses.
4. **Query Execution**
   - Executes queries on the uploaded CSV files, ensuring responses are relevant to the content of the CSV files.

## Code Structure

1. **Root Directory**
   - Contains the `src` folder, Jupyter notebook, `requirements.txt` file, and `main.py` file.
2. **Jupyter Notebook**
   - Functionality can be run by executing commands in the notebook.
3. **Main.py**
   - Imports functions from `config.py` in the `src` directory and calls them through the Gradio interface.
4. **Config.py**
   - Functions can be used for backend API or modified as needed in the notebook.

## Features

- Only answers queries related to the uploaded CSV files.
- Does not respond to irrelevant queries outside the context of the CSV files.

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

- Python (version 3.10 or later)
- OpenAI API key

### Installation

1. **Clone the Repo**

   Clone the repo open the folder.

2. **Create a Python virtual environment**

   Open your terminal and create a Python virtual environment by using the following command:

   ```sh
   python -m venv venv

3. **Activate the virtual environment**
   ```sh
   .\venv\Scripts\Activate.ps1
5. **Install required packages**
   ```sh
   pip install -r requirements.txt
7. **Set up OpenAI API key**
   ```sh
   export OPENAI_KEY=InsertYourKeyHere
9. **Run the main application**
   ```sh
   python main.py

### Usage

1. Upload your CSV files using the Gradio interface.

2. Start executing queries. The functionality will create indexes of the CSV file data from which the model retrieves the query results.

### Contributing
If you want to contribute to this project, please fork the repository and create a pull request.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

