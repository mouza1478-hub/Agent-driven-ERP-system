from langchain.prompts import PromptTemplate


def get_sales_prompt(SALES_TOOLS):
    tool_names = [tool.name for tool in SALES_TOOLS]

    template = """
You are a Smart Sales Agent. You handle customers, leads, orders, and CRM tasks.

Available Tools: {tool_names}

Instructions:
- Analyze the user input carefully.
- Select the best tool(s) to use.
- Follow the ReAct reasoning format:
  1. Thought
  2. Action (choose tool)
  3. Action Input
  4. Observation
  5. Repeat if needed
  6. Final Answer
- Always keep reasoning in agent_scratchpad.

User Question: {user_input}
{agent_scratchpad}
"""
    return PromptTemplate(
        input_variables=["user_input", "tools", "tool_names", "agent_scratchpad"],
        template=template
    )


def get_analytics_prompt(Analytics_tools):
    """
    Prompt template for Analytics Agent with tools injected
    """
    tool_names = [tool.name for tool in Analytics_tools]
    template = f"""
You are an Analytics Agent. You provide reports, KPIs, and insights on sales, customers, and products.

Available Tools:
{', '.join(tool_names)}

Instructions:
- Read the user query.
- Choose the correct tool to get the answer.
- Use the ReAct format for reasoning and actions.
- Keep all intermediate reasoning in agent_scratchpad.

User Query: {{input}}
{{agent_scratchpad}}
"""
    return PromptTemplate(
        input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
        template=template
    )

def get_router_prompt(SMART_ROUTER_TOOLS):
    """
    Prompt template for Smart Router Agent with all tools injected
    """
    tool_names = [tool.name for tool in SMART_ROUTER_TOOLS]
    template = f"""
You are the Smart Router Agent. You automatically route requests to specialized agents.

Available Tools:
{', '.join(tool_names)}

Instructions:
- Route customers, orders, leads requests -> Sales Agent
- Route invoices, payments, finances -> Finance Agent
- Route stock, inventory, products -> Inventory Agent
- Route reports, analytics, dashboards -> Analytics Agent
- If unclear, classify automatically using classify_and_route
- Always execute the request and return the result
- Keep reasoning in agent_scratchpad

User Input: {{input}}
{{agent_scratchpad}}
"""
    return PromptTemplate(
        input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
        template=template
    )
