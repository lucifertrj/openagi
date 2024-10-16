import logging
from langchain_community.llms import Ollama
from openagi.agent import Agent
from openagi.init_agent import kickOffAgents
from openagi.llms.base import LLMBaseModel, LLMConfigModel
from openagi.llms.openai import OpenAIModel
from openagi.tools.integrations import DuckDuckGoSearchTool
from openagi.utils.yamlParse import read_yaml_config

class OllamaConfigModel(LLMConfigModel):
    """Configuration model for OLLAMA."""
    model_name: str

class OllamaModel(LLMBaseModel):
    """Ollama implementation of the LLMBaseModel.
    This class implements the specific logic required to work with Ollama.
    """
    def __init__(self, config: OllamaConfigModel):
        super().__init__(config)

    def load(self):
        """Initializes the Ollama instance with configurations."""
        ollama_model = "llama2"
        print(f">>> {ollama_model=}")
        self.llm = Ollama(model=ollama_model)
        return self.llm

    def run(self, input_text: str):
        """Runs the Ollama model with the provided input text.
        Args:
            input_text: The input text to process.
        Returns:
            The response from Azure's OpenAI service.
        """
        if not self.llm:
            self.load()
        print("ollma ...")
        resp = "dummy result - planner is not supported with local LLM"
        print(f"ollma is working...{resp}")
        return resp

    @staticmethod
    def load_from_yaml_config():
        return OllamaConfigModel(model_name=read_yaml_config("OLLAMA_MODEL_NAME") or "llama2")


def onResultHGI(agentName, result, consumerAgent):
    feedback = "Pass"
    action = "None"
    logging.debug(f"{agentName}:TO:{consumerAgent}-> {result}")
    return result, feedback, action

# Example Usage:
if __name__ == "__main__":
    config = OllamaModel.load_from_yaml_config()
    llm = OllamaModel(config=config)
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
            task="summarize points to present to health care professionals and general public separately on covid-19 latest trends",
            output_consumer_agent=["EMAILER"],
            llm=llm,
        ),
        Agent(
            agentName="EMAILER",
            role="EMAIL CREATOR",
            goal="composes the email based on the content",
            backstory="Good in composing precise emails",
            capability="llm_task_executor",
            task="composes email based on summary to doctors and general public separately into a file with subject-summary and details",
            output_consumer_agent=["HGI"],
            llm=llm,
        ),
    ]
    config_openai = OpenAIModel.load_from_yaml_config()
    llm_openai = OpenAIModel(config=config_openai)
    kickOffAgents(agent_list, [agent_list[0]], llm=llm_openai)
