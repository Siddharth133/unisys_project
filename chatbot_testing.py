from langchain.llms import HuggingFaceHub
from langchain import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize language model from Hugging Face Hub
repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
llm = HuggingFaceHub(
  repo_id=repo_id,
  model_kwargs={"temperature": 0.8, "top_k": 50},
  huggingfacehub_api_token=os.getenv('HUGGINGFACE_API_KEY')
)


template = """
As a knowledgeable medical assistant, you're equipped with 
a vast database of medical information. 
Your purpose is to provide informative, accurate, and 
helpful advice on health and disease-related questions. 
Your responses should be concise yet informative, 
offering insights based on the latest medical knowledge. 
If a question falls outside your expertise or 
if providing advice could be potentially harmful without 
professional consultation, you must advise seeking a 
healthcare professional's guidance.

Question: {question}

Answer:

"""

prompt = PromptTemplate(
  template=template,
  input_variables=["question"]
)

pipeline = (
  RunnablePassthrough()
  | prompt
  | llm
  | StrOutputParser()
)

# Example usage
class ChatBot:
    def ask(self, question):
        result = pipeline.invoke({"question": question})
        result_without_paragraph = result.split("healthcare professional's guidance.")[1]
        return result_without_paragraph

# Initialize the ChatBot
# bot = ChatBot()
# question = input("Ask me Anything about medical field: ")
# result = bot.ask(question)
# print(result)
