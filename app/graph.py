from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode , tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import os
from langchain_core.tools import tool
from langchain.schema import SystemMessage
import re
from pathlib import Path

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

@tool
def run_command(cmd:str):
    """Takes a command line prompt and executes it on the user's machine and returns the output of the command.
     Ensure complete and functional implementations as per Windows environment.
     Example:
      run_command(cmd ="ls") where ls is the command to list the files  """
    result =os.system(command=cmd)
    return result

@tool
def write_file(path: str, content: str, project_hint: str = None):
    """
    Writes the given content to the specified file path.

    - Automatically creates necessary folders.
    - Determines the root folder based on the user's request (e.g., 'to-do', 'weather-app').
    - If no specific app name is detected, defaults to 'myapp/'.
    
    Parameters:
    - path: Relative path within the project (e.g., 'app.py', 'static/style.css').
    - content: The file content to write.
    - project_hint: Optional. If provided, will be used to name the root directory.
    Do the proper formatting of code in efficient manner.
    """

    # Clean project_hint to be a safe folder name
    if project_hint:
        root_folder = re.sub(r'[^\w\-]', '-', project_hint.strip().lower())
    else:
        root_folder = "myapp"

    # Final full path
    full_path = os.path.join(root_folder, path)


    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return f"File written successfully: {full_path}"

@tool
def open_website(site: str):
    """Opens popular websites in the default web browser.
    
    Supports common websites like Google, YouTube, Instagram, Facebook, Twitter, GitHub, etc.
    Can also open any custom URL.
    
    Args:
        site (str): Website name or URL to open
        
    Examples:
        open_website(site="google") - Opens Google.com
        open_website(site="youtube") - Opens YouTube.com
        open_website(site="instagram") - Opens Instagram.com
        open_website(site="https://example.com") - Opens custom URL
    """
    import webbrowser
    
    # Dictionary of popular websites
    websites = {
        'google': 'https://www.google.com',
        'youtube': 'https://www.youtube.com',
        'instagram': 'https://www.instagram.com',
        'facebook': 'https://www.facebook.com',
        'twitter': 'https://www.twitter.com',
        'x': 'https://www.x.com',
        'github': 'https://www.github.com',
        'linkedin': 'https://www.linkedin.com',
        'reddit': 'https://www.reddit.com',
        'stackoverflow': 'https://stackoverflow.com',
        'wikipedia': 'https://www.wikipedia.org',
        'amazon': 'https://www.amazon.com',
        'netflix': 'https://www.netflix.com',
        'spotify': 'https://www.spotify.com',
        'gmail': 'https://mail.google.com',
        'outlook': 'https://outlook.live.com',
        'whatsapp': 'https://web.whatsapp.com',
        'discord': 'https://discord.com',
        'slack': 'https://slack.com',
        'zoom': 'https://zoom.us'
    }
    
    try:
        site_lower = site.lower().strip()
        
        # Check if it's a predefined website
        if site_lower in websites:
            url = websites[site_lower]
            webbrowser.open(url)
            return f"Successfully opened {site.title()} ({url}) in your default browser"
        
        # Check if it's already a URL
        elif site.startswith(('http://', 'https://')):
            webbrowser.open(site)
            return f"Successfully opened {site} in your default browser"
        
        # Try to open as a .com website
        elif '.' not in site:
            url = f"https://www.{site_lower}.com"
            webbrowser.open(url)
            return f"Successfully opened {url} in your default browser"
        
        # Handle other domains
        else:
            if not site.startswith(('http://', 'https://')):
                url = f"https://{site}"
            else:
                url = site
            webbrowser.open(url)
            return f"Successfully opened {url} in your default browser"
            
    except Exception as e:
        return f"Error opening website '{site}': {str(e)}"

@tool
def search_youtube(query: str, max_results: int = 5):
    """Searches for YouTube videos based on user query and opens the results or displays them.
    
    Args:
        query (str): The search term/query to search for on YouTube
        max_results (int): Maximum number of results to return (default: 5, max: 10)
        
    Examples:
        search_youtube(query="python tutorial") - Searches for Python tutorials
        search_youtube(query="cooking recipes", max_results=3) - Searches for cooking videos
        search_youtube(query="music") - Searches for music videos
    """
    import webbrowser
    import urllib.parse
    
    try:
        # Input validation
        if not query or not query.strip():
            return "Error: Search query cannot be empty"
        
        # Limit max_results to prevent overwhelming output
        if max_results > 10:
            max_results = 10
        elif max_results < 1:
            max_results = 1
        
        query = query.strip()
        
        # Method 1: Simple approach - Open YouTube search directly
        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        # Open the search results page
        webbrowser.open(search_url)
        
        return f"Successfully opened YouTube search results for '{query}' in your default browser.\nSearch URL: {search_url}"
        
    except Exception as e:
        return f"Error searching YouTube for '{query}': {str(e)}"
    



llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)
llm_with_tool = llm.bind_tools(tools = [run_command , write_file , open_website , search_youtube])

def chatbot(state: State):
    system_prompt = SystemMessage(content="""
    You are an AI coding assistant who take an input from the user and based on available tool you choose the correct tool
    and execute the commands.First you make a plan how to execute it and then try to enhance that made plan and then execute the enhanced plan .
    
    You can  even execute commands and help user  with output of commands
                                  
    Always make sure to keep your generated codes and files in generated/ folder . You can create one if not already there

     """)
    message =llm_with_tool.invoke([system_prompt] + state["messages"])
    assert len(message.tool_calls) <=1
    return {"messages": [message]}

tool_node = ToolNode(tools=[run_command , write_file ,open_website , search_youtube])

graph_builder =StateGraph(State)

graph_builder.add_node("chatbot" , chatbot)
graph_builder.add_node("tools",tool_node)

graph_builder.add_edge(START , "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot" , END)

graph = graph_builder.compile()

# As like issme memory aa rahi   hai
def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)