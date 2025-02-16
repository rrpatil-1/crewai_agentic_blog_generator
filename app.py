from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
import os

from dotenv import load_dotenv

load_dotenv()

topic = "Medical Industry using Generative AI"
llm_model = os.environ.get('LLM_MODEL')
# Tools 1
llm=LLM(model=f"gemini/{llm_model}",api_key=os.getenv("GEMINI_API_KEY"))

# Tools 2
search_tool = SerperDevTool(n=10, api_key=os.getenv("SERP_API_KEY"))

#Agent 1
Sr_research_analyst = Agent(
    role="Sr_research_analyst",
    goal=f"Research, analyse and synthesize comprehensive information on {topic} from reliable web source",
    backstory= "You are a expert research analyst with advanced web research skill"
    "you excel at finding, analyzing, and synthesizing information"
    "from accross the internet using search and analysis tools. You are skill at"
    "distinguishing reliable web sources from unreliable ones,"
    "fact checking , cross referencing information and identifying key patterns and insights."
    "You provide well organized research brief with proper citation and source verification."
    "Your analysis includes both raw data and interpreted insights, making complex"
    "information accessible and actionable",
allow_delegation=False,
verbose=True,
tools=[search_tool],
llm=llm)

#Agent 2
content_writer = Agent(
    role="content_writer",
    goal=f"tranform research findings into engaging blog posts while maintaining accuracy and credibility",
    backstory="Your are skilled content writer with experience in writing engaging and informative blog posts"
    "you work closely with research analyst and excel at maintaining the perfect"
    "balance between informative and entertaining writing."
    "while ensuring all facts and ciations from the research"
    "are properly incorporated. you have talent for making "
    "complex topics approchable without oversimplifying them.",
allow_delegation=False,
verbose=True,
llm=llm
    )


# Research Task
research_task =Task(
    description=(f"""
    1. Conduct compresive research on {topic} including:
        - recent development and news
        - key industry trend and inovations
        - Expert opinion and analyses
        - Statistical data and market insights
    2. evaluate source credibility and fact-check all information
    3. Organize findings into structured research brief
    4. Include all relevant ciations and sources"""),
    expected_output=""" A detailed research report containing:
    -  Executive summary of key findings
    - Comprehensive analysis of current trends and developments
    - List all verified fact and statistics
    - All ciations and links to original sources
    - Clear categorization of theme and patterns
    Please format with clear section and bullet points for easy reference
""",
agent=Sr_research_analyst
)

# content writing task
writing_task = Task(
    description=("""Using research brief provided, create enagaging blog post
                 1. Transform technical information into accessible content
                 2. maintain  all factual accuracy and ciations from the research
                 3. Includes:
                    - Attention grabbing introduction
                    - well structured body with clear subheadings
                    - Compelling Conclusion
                 4. Preserve all source ciations in [source:url] format
                 5. include references section at the end
                 """),
    expected_output="""A polished blog post in Markdown format that:
        - Engage the Readers while maintaining factual accuracy
        - contains properly structured sections and subheadings
        - Includes Inline ciations hyperlinked to original source url
        - Present Information in an accessible yet informative way
        - follows proper Markdown formatting, Use H1 for title and H2 for H3 for sub-sections""",
    agent=content_writer
)


crew = Crew(
    agents=[Sr_research_analyst, content_writer],
    tasks=[research_task, writing_task],
    verbose=True

)

result = crew.kickoff(inputs={"topic":topic})

print(result)
