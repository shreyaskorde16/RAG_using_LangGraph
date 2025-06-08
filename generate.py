## Name: Shreyas Korde
## Date 5TH June 2025
## Email: shreyaskorde16@gmail.com
## Description: This is a Advanced RAG algorithm with Agentic AI and Langgraph with Streamlit app that 
##              demonstrates various components and functionalities of Streamlit and RAG with Langgraph.

from langchain.schema import HumanMessage, AIMessage
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from typing import Annotated
from langgraph.graph.message import add_messages
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from typing import List
import re
from dotenv import load_dotenv
import os
load_dotenv()


# Start creating the Langraph 
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]   # will append all the messages and connvert to type dict
    

def response_llm(question: str, graph_compile2: StateGraph, llm: ChatGroq) -> str:
    """_summary_
    Args:
        question (str): Human message to be processed by the LLM.
        graph_compile2 (StateGraph): Compiled langgraph for processing the question.
        llm (ChatGroq): LLM instance to be used for processing the question.
    Returns:
        answer (str): Processed answer from the LLM."""
        
    # Define the prompt template for summarization
    prompt =ChatPromptTemplate.from_template("""
        Summarize the context provided in english and german translation of it. 
        The structure should be as **English:**(English summary) **German:**(German translation of english summary).
        Understand the crucial information given in the context and then provide a final answer only as structured above.
        <context>
        {context}
        </context>
        Question: {input}""")
    message =  graph_compile2.invoke({"messages": question})
    #for m in message["messages"]:
        #print(m.pretty_print())

    #prompt = prompt.format_messages(context=message, input=question)
    llm_chain = LLMChain(llm=llm, prompt=prompt, verbose=False)
    response = llm_chain.run(context=message, input=question)
    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    answer = response.strip()
    # Print the response
    #print(f"Processed response from LLM:\n {response}")
    return answer, message


def build_graph(llm_with_tools, tools):
    """ Builds the Langgraph for tool calling with LLM.
    Args:
        llm_with_tools (ChatGroq): LLM instance with tools bound to it.
        tools (list): List of tools to be used in the Langgraph.
    Returns:
        graph_compile2 (StateGraph): Compiled Langgraph for tool calling with LLM."""
    
    # Build the Langgraph  
    def tool_calling_llm(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}
    
    builder2 = StateGraph(State)
    builder2.add_node("tool_calling_llm", tool_calling_llm)
    builder2.add_node("tools", ToolNode(tools))


    ## edges
    builder2.add_edge(START, "tool_calling_llm")
    builder2.add_conditional_edges("tool_calling_llm", tools_condition)
    builder2.add_edge("tools", "tool_calling_llm")

    graph_compile2 = builder2.compile()
    display(Image(graph_compile2.get_graph().draw_mermaid_png()))
    print("Graph compiled successfully.")
    return graph_compile2
   
def get_response(question: str):
    """_summary_

    Args:
        question (str): _description_

    Returns:
        _type_: _description_
    """
    
    # Groq LLM
    llm = ChatGroq(
        model="qwen-qwq-32b",
        temperature=0.1,
        max_tokens=4000,
        verbose=False
    )


    # Arxiv Tool
    api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=4, doc_content_chars_max=1000)
    arxiv = ArxivQueryRun(api_wrapper=api_wrapper_arxiv, description="Arxiv query tool")
    # Wikipedia Tool
    api_wrapper_wikipedia = WikipediaAPIWrapper(top_k_results=4, doc_content_chars_max=1000)
    wikipedia = WikipediaQueryRun(api_wrapper=api_wrapper_wikipedia, description="Wikipedia query tool")
    # Tavily Tool
    tavily = TavilySearchResults()
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
    os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

    # Combining Tools
    tools = [arxiv, wikipedia, tavily]
    print("Tools initialized successfully.")

    # Bind the tools to llm 
    llm_with_tools = llm.bind_tools(tools=tools)
    
    # Build the graph
    compiled_graph = build_graph(llm_with_tools, tools)
    
    # Get the response from the LLM using the compiled graph
    processed_answer, langgraph_output = response_llm(question= question, graph_compile2= compiled_graph, llm=llm)
    print("Final Answer:", processed_answer)
    

    for m in langgraph_output["messages"]:
        print(m.pretty_print())


    seperate_messsages = [None, None, None, None]
    

    for i, m in enumerate(langgraph_output["messages"]):
        role = m.__class__.__name__  # e.g., "HumanMessage", "AIMessage", "ToolMessage"
        content = getattr(m, "content", "")
        #seperate_messsages.append(f"{role}: {content}")
        seperate_messsages[i] = f"{role}: {content}"
    
    print(f"From seperate message {seperate_messsages[0]} \n")      
    print(f"From seperate message {seperate_messsages[2]} \n")     
    print(f"From seperate message {seperate_messsages[3]} \n")     
                
    #get_message(langgraph_output)   
    return processed_answer, seperate_messsages
    
#answer, grapg_output = get_response("What is the latest research on quantum computing?")  # Example question to test the graph


    
    




















