"""create_agent() -> Tools are passsed as function defn in API call iteslf - the LLMs sees them natively LLM returns structured tool_call objects - no text to parse
LangGraph state machine handles the loop -> LLM responds naturally
"""


from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search,scrape_url
import os
from dotenv import load_dotenv
load_dotenv()


# model setup
llm=ChatGroq(model="llama-3.3-70b-versatile",temperature=0)

# first agent
def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )


#another agent  -> reader agent
def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )
    
# writer chain -> LECL
writer_prompt=ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Title
- Abstract
- Introduction
- Literature Review
- Methodology
- Key Findings (minimum 3 well-explained points)
- Discussion
- Conclusion
- Sources/References (list all URLs found in the research properly)

Be detailed, factual and professional."""),
])

writer_chain=writer_prompt | llm | StrOutputParser()


#critic_chain 
critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])


critic_chain=critic_prompt | llm | StrOutputParser()