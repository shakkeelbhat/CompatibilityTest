from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pprint
import os,sys
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

#add openai api key and serpapi api key
os.environ["OPENAI_API_KEY"] = ""
os.environ["SERPAPI_API_KEY"] = ""

def extract(filename):
    
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file in file_list:
        #pprint.pprint(file)
        try:
            if file['originalFilename'] == filename:
                content = file.GetContentString()
                return content
        except KeyError:
            print('File not in Gdrive')
            sys.exit()



def query_content(content):
        # We need to split the text using Character Text Split such that it sshould not increse token size
        text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap  = 200,
        length_function = len,
    )
        texts = text_splitter.split_text(content)
        embeddings = OpenAIEmbeddings()
        document_search = FAISS.from_texts(texts, embeddings)
        chain = load_qa_chain(OpenAI(), chain_type="stuff")
        docs = document_search.similarity_search(query)
        return chain.run(input_documents=docs, question=query) 



if __name__ == '__main__':
    if len(sys.argv)==1:
        print("No arguments provided")
        sys.exit()
    try:
        if sys.argv[1]:
            query=sys.argv[1]
    except:
        print("No search argument provided.")
    try:
        filename=sys.argv[2]
    except:
        print("No filename provided. Enter the filename to look for in your drive")
        sys.exit()
    
    
    content = extract(filename)
    results=query_content(content)
    print(results)
