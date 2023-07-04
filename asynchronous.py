from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pprint
import os,sys
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import timeit
import asyncio
os.environ["OPENAI_API_KEY"] = ""
os.environ["SERPAPI_API_KEY"] = ""

async def extract(filename):
    start = timeit.timeit()
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    # We need to split the text using Character Text Split such that it sshould not increse token size
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap  = 200,
        length_function = len,
    )
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file in file_list:
        #pprint.pprint(file)
        try:
            if file['originalFilename'] == filename:
                content = file.GetContentString()
                end = timeit.timeit()
                print("Time taken: ", end - start)
                task = asyncio.create_task(query_content(content,text_splitter))
                result =  await task
                return result
        except KeyError:
            print('File not in Gdrive')
            sys.exit()



async def query_content(content,text_splitter):
        start = timeit.timeit()

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
        end = timeit.timeit()
        print("Time taken is: ", end - start )

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
    
    
    print(asyncio.run(extract(filename)))
    