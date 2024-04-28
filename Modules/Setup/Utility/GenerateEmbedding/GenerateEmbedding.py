from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# embeddings = OllamaEmbeddings()
embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")

textSplitter = CharacterTextSplitter(
    separator="--n",
    chunk_size = 50,
    chunk_overlap = 0
)

loader = TextLoader(r'D:\Major_Project\Modules\Setup\Utility\GenerateEmbedding\dataset.txt')
docs = loader.load_and_split(
    text_splitter=textSplitter
)

db = Chroma.from_documents(
    docs,
    embedding=embeddings,
    persist_directory="emb"
)