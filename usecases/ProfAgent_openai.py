import logging

from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.openai import OpenAIModel
from openagi.tools.integrations.duckducksearch import DuckDuckGoSearchTool

if __name__ == "__main__":
    # Log program start
    logging.info("Program started")
    agent_list = [
        Agent(
            agentName="RESEARCHER",
            role="RESEARCH EXPERT",
            goal="search for latest trends in COVID-19 and Cancer treatment that includes medicines, physical exercises, overall management and prevention aspects",
            backstory="Has the capability to execute internet search tool",
            capability="search_executor",
            task="search internet for the goal for the trends after first half of 2023",
            output_consumer_agent=["WRITER"],
            tools_list=[DuckDuckGoSearchTool],
        ),
        Agent(
            agentName="WRITER",
            role="SUMMARISING EXPERT",
            goal="summarize input into presentable points",
            backstory="Expert in summarising the given text",
            capability="llm_task_executor",
            task="summarize points to present to health care professionals and general public separately",
            output_consumer_agent=["EMAILER"],
        ),
        Agent(
            agentName="EMAILER",
            role="EMAIL CREATOR",
            goal="composes the email based on the content",
            backstory="Good in composing precise emails",
            capability="llm_task_executor",
            task="composes email based on summary to doctors and general public separately into a file with subject-summary and details",
            output_consumer_agent=["HGI"],
        ),
    ]
    config = OpenAIModel.load_from_yaml_config()
    llm = OpenAIModel(config=config)
    for agent in agent_list:
        logging.info(f"Initializing agent: {agent.agentName}")
    kickOffAgents(agent_list, [agent_list[0]], llm=llm)
    logging.info("Program ended")
