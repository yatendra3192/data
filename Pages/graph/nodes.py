from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from .state import AgentState
import json
from typing import Literal
from .tools import complete_python_task
import os


llm = ChatOpenAI(model="gpt-4o", temperature=0)

tools = [complete_python_task]

model = llm.bind_tools(tools)

# Create a simple tool executor
tools_by_name = {tool.name: tool for tool in tools}

with open(os.path.join(os.path.dirname(__file__), "../prompts/main_prompt.md"), "r") as file:
    prompt = file.read()

chat_template = ChatPromptTemplate.from_messages([
    ("system", prompt),
    ("placeholder", "{messages}"),
])
model = chat_template | model

def create_data_summary(state: AgentState) -> str:
    summary = ""
    variables = []
    for d in state["input_data"]:
        variables.append(d.variable_name)
        summary += f"\n\nVariable: {d.variable_name}\n"
        summary += f"Description: {d.data_description}"
    
    if "current_variables" in state:
        remaining_variables = [v for v in state["current_variables"] if v not in variables]
        for v in remaining_variables:
            summary += f"\n\nVariable: {v}"
    return summary

def route_to_tools(
    state: AgentState,
) -> Literal["tools", "__end__"]:
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route back to the agent.
    """

    if messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return "__end__"

def call_model(state: AgentState):

    current_data_template  = """The following data is available:\n{data_summary}"""
    current_data_message = HumanMessage(content=current_data_template.format(data_summary=create_data_summary(state)))
    state["messages"] = [current_data_message] + state["messages"]

    llm_outputs = model.invoke(state)

    return {"messages": [llm_outputs], "intermediate_outputs": [current_data_message.content]}

def call_tools(state: AgentState):
    last_message = state["messages"][-1]
    tool_messages = []
    state_updates = {}

    if isinstance(last_message, AIMessage) and hasattr(last_message, 'tool_calls'):
        for tool_call in last_message.tool_calls:
            tool_name = tool_call["name"]
            tool_input = {**tool_call["args"], "graph_state": state}

            # Execute the tool
            try:
                tool = tools_by_name[tool_name]
                response = tool.invoke(tool_input)

                # Handle response
                if isinstance(response, tuple) and len(response) == 2:
                    message, updates = response
                else:
                    message = response
                    updates = {}

                tool_messages.append(ToolMessage(
                    content=str(message),
                    name=tool_name,
                    tool_call_id=tool_call["id"]
                ))
                state_updates.update(updates)
            except Exception as e:
                # Handle errors gracefully
                tool_messages.append(ToolMessage(
                    content=f"Error executing tool: {str(e)}",
                    name=tool_name,
                    tool_call_id=tool_call["id"]
                ))

    if 'messages' not in state_updates:
        state_updates["messages"] = []

    state_updates["messages"] = tool_messages
    return state_updates

