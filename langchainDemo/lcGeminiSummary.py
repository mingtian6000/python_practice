from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate



#Initialize Model from remote
llm = ChatGoogleGenerativeAI(model="gemini-pro")

#Load the blog
loader = WebBaseLoader("https://thenewstack.io/the-building-blocks-of-llms-vectors-tokens-and-embeddings/")
docs = loader.load()

#Define the Summarize Chain
template = """Write a concise summary of the following:
"{text}"
CONCISE SUMMARY:"""

prompt = PromptTemplate.from_template(template)

llm_chain = LLMChain(prompt | llm)
stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

#Invoke Chain
response=stuff_chain.invoke(docs)
print(response["output_text"])