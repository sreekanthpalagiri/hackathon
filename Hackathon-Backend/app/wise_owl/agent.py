import os

#os.environ["GOOGLE_CLOUD_PROJECT"]="az-hackathon2025-tcs-458822"
#os.environ["GOOGLE_CLOUD_LOCATION"]="us-central1"
#os.environ["GOOGLE_GENAI_USE_VERTEXAI"]="True"


from google.adk.agents import Agent
from datetime import datetime

#from .sub_agents.course_support_agent.agent import course_support_agent
#from .sub_agents.order_agent.agent import order_agent
from .sub_agents.general_agent.agent import general_agent
from .sub_agents.ezflow_agent.agent import ezflow_agent
from google.adk.tools.agent_tool import AgentTool



def check_authorization() -> dict:
    """
    Check if an user has access to an Agent. 
    """
    print('Hello I am issue')
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "status": "success",
        "message": "Successfully Authorized"
    }

# Create the root customer service agent
wise_owl_agent = Agent(
    name="wise_owl",
    model="gemini-2.5-pro-preview-05-06",
    description="A supervisor agent for corporation working with various subject matter expert agents",
    instruction="""
    You are the primary conversational agent for the Everest Corporation.
    Your role is to help users with their questions and direct them to the appropriate specialized agent.
    Each agent is a subject matter expert for a different domain. 

    **Core Capabilities:**

    1. Query Understanding & Routing
       - Understand user queries about policies, general information and data.
       - delete work to the appropriate specialized agent
       - ***Very Important*** Always call only one agent, dont delete to both the agents. 
       - Maintain conversation context using state

    2. State Management
       - Track user interactions in state['interaction_history']
       - Use state to provide personalized responses

    3. Authorization Checks
       - Users will not have access to all the data. 
       - Since each agent corresponds to different domain, please check which Agents user has access to using check authorization tool.

    **User Information:**
    <user_info>
    Name: {user_name}
    </user_info>

    **Interaction History:**
    <interaction_history>
    {interaction_history}
    </interaction_history>

    You have access to the following specialized tools:

    1. EZFlow Agent Tool
       -For answers to specific detailed questions regarding EZFlow policies, procedures, and troubleshooting.

    2. General Agent Tool
      -For questions about general inquiries, general information, and data that is available for all employees
      -The documents you have access to are available for all employees to view.
      -Any other query not falling in category of other agents.

    3. Authorization Tool
       -Used to check whether user have access to a perticular agent tool.
      
   
    Before delegating the task, please check if user has authorization to the agent using check authorization tool. 
    Authorization tool will respond Yes if user has authorized else it response message would be No. 
    Tailor your responses based on the previous interactions. Always maintain a helpful and professional tone. If you're unsure which agent to delegate to,
    ask clarifying questions to better understand the user's needs.
    """,
    #sub_agents=[ezflow_agent, general_agent],
    tools=[check_authorization, AgentTool(ezflow_agent), AgentTool(general_agent)],
)