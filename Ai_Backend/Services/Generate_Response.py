
from ollama import chat
from openai import OpenAI


# import litellm
# from trulens.providers.litellm import LiteLLM

# from trulens.core import Feedback

class Generate_Response():
    def __init__(self):
         pass
    
    def generate_response_Local(self, input, context, model_name):
               """
               Generate a response using a chat model and stream the output.
               
               Args:
                    input (str): The user's question or input
                    context (str): The context to use for answering the question
                    model_name (str): The name of the model to use
               
               Returns:
                    str: The complete response text
               """
               response_text = ""
               
               stream = chat(
                    model=model_name,
                    messages=[
                         {
                              'role': 'system',
                              'content': f"""
                                   You are helpfull Well Excellent Insharp Technologies Company HR  you should answer the question using provided context only 
                                   if you dont know then simply say i dont know.

                                   Fisrt flow the stpes:
                                   1)Compare question and context is those relevant if not say i dont know the answer
                                   2)If yes then provide answer based on the context dont use other contexts.
                                   {context}
                              """
                         },
                         {
                              'role': 'user',
                              'content': input
                         }
                    ],
                              stream=True
                         )
                         
               for chunk in stream:
                    chunk_content = chunk['message']['content']
                    #print(chunk_content, end='', flush=True)
                    response_text += chunk_content
               
               return response_text

                    
    def generate_response_deepseek(self,context,input):
               client = OpenAI(api_key="sk-67f6a82d472142899f2653882af0a925", base_url="https://api.deepseek.com")

               response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                         {"role": "system", 
                         "content": 
                         
                         f"""
                         Role: You are a well-experienced customer care agent. Your task is to answer user questions in a polite manner.

                         Instructions:
                         If User Message is General greetings then repond Polite way your greetings

                         check whether the user's question is relevant to the provided context.

                         If not relevant, politely respond with:
                         "I don't know the answer."

                         If the question is irrelevant to customer care topics, respond with:
                         "I don't know the answer."

                         If the question is relevant to the provided context, answer the question strictly using only the information from the provided context.

                         Do not add any extra information beyond what is in the context.

                         Strictly follow the above rules when answering user questions.

                         {
                         context
                         }

                         """
                         },
                         {
                              "role": "user", 
                              "content":input

                         }
                    ],
                    stream=False
               )

               return response.choices[0].message.content

    def generate_response_common(self,input):
               client = OpenAI(api_key="sk-67f6a82d472142899f2653882af0a925", base_url="https://api.deepseek.com")

               response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                         {"role": "system", 
                         "content": 
                         
                         f"""You are helpfull assistant. Your task is to answer user questions in a polite manner.
                         generate common answer.


                         """
                         },
                         {
                              "role": "user", 
                              "content":input

                         }
                    ],
                    stream=False
               )

               return response.choices[0].message.content

          
          

         
#     #validate query and Response Validation
#     def Relevance_Check(self,query,llm_response):

#                          """input-user query
#                               llm response

#                          return : Relevance score
                         
#                          """
#                          #import litellm
#                          #litellm.set_verbose = False
#                          ollama_provider = LiteLLM(
#                               model_engine= "ollama/qwen2.5:0.5b" ,api_base="http://localhost:11434"
#                          )

#                          # Define a relevance function using LiteLLM
#                          relevance = Feedback(
#                               ollama_provider.relevance_with_cot_reasons
#                          ).on_input_output()

#                          score=ollama_provider.relevance_with_cot_reasons(
#                               query,
#                               llm_response)
#                          return score

