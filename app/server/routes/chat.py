from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
import os
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import create_pandas_dataframe_agent
import pandas as pd
from decouple import config

router = APIRouter()


OPENAI_API_KEY = config('OPENAI_API_KEY')
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

# Load dataframe with projects information
# Make sure your data CSV file is in the appropriate directory
df = pd.read_csv("feed.csv", sep=",")

agent = create_pandas_dataframe_agent(
    ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)


class ChatInput(BaseModel):
    prompt: str


@router.post("/chat")
async def chat_endpoint(chat_input: ChatInput):
    try:
        response = agent.run(chat_input.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
