import os
import getpass
import pandas as pd
import streamlit as st

from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.agents import create_pandas_dataframe_agent


def main():

    apikey_input = st.text_input("Enter a OpenAI API Key.", type="password")
    if apikey_input:
        os.environ['OPENAI_API_KEY'] = apikey_input

        # Load dataframe with projects information.
        df = pd.read_csv("src/data/feed.csv", sep=",")

        agent = create_pandas_dataframe_agent(
            ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
            df,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
        )

        st.title("OpenCatalog")
        st.markdown("---")
        html_string = """
        <h2 style="font-weight:bold;">How can we help you today?</h2>

        """
        st.markdown(html_string, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([3, 5, 1])

        with col1:
            recomm = st.button('Project recommendations')
        with col2:
            info = st.button(
                'Information about an specific project or projects')
        with col3:
            other = st.button('Other')

        if recomm:
            # Project input
            input_prompt = st.text_input("Tell us what are your interests, and we will give you project recommendations",
                                         placeholder="Type here...")
            html_string = """
            <p style="font-size:11px;color:grey;">GPT-Powered AI Assistant</p>

            """
            st.markdown(html_string, unsafe_allow_html=True)

            submit = st.button("Send")

            if submit:
                st.write('click')
                if input_prompt:
                    st.write(input_prompt)
                    prompt_template = """Give me recommendations based on my projects interests and tell me what projects are related to my interests. 
                    If you don't know the answer, just say that you don't know, don't try to make up an answer.

                    My projects interests are the following:
                    {interests}

                    Answer here:"""

                    prompt = prompt_template.format(interests=input_prompt)

                    # My interests are in microplastics, or something related with aquatic species
                    with st.spinner('Thinking...'):
                        response = agent.run(prompt)
                    st.write(response)
            else:
                st.write('not click')

        elif info:
            # Project input
            input_prompt = st.text_input("What project or projects do you need information about? (please separate their names using a comma)",
                                         placeholder="Type here...")
            html_string = """
            <p style="font-size:11px;color:grey;">GPT-Powered AI Assistant</p>

            """
            st.markdown(html_string, unsafe_allow_html=True)

            submit = st.button("Send")

            if submit:
                if input_prompt:
                    prompt_template = """Give me the project description of each project name I will provide to you, each project description should be in a new line. 
                    If you don't know the answer, just say that you don't know, don't try to make up an answer.

                    The project names of which I need their descriptions are:
                    {project_names}

                    Answer here:"""

                    prompt = prompt_template.format(project_names=input_prompt)
                    # noaa nws skywarn, image detective, EcoCast
                    response = agent.run(prompt)
                    st.write(response)

        elif other:
            # Project input
            input_prompt = st.text_input("Tell us how can we help you today and we will do our best!",
                                         placeholder="Type here...")
            html_string = """
            <p style="font-size:11px;color:grey;">GPT-Powered AI Assistant</p>

            """
            st.markdown(html_string, unsafe_allow_html=True)

            submit = st.button("Send")

            if submit:
                if input_prompt:
                    prompt_template = """Based on the information in the dataset, answer the question at the end. 
                    If you don't know the answer, just say that you don't know, don't try to make up an answer.

                    Question: {question}

                    Answer here:"""

                    prompt = prompt_template.format(question=input_prompt)
                    # How many open science projects currently exist?
                    response = agent.run(prompt)
                    st.write(response)


if __name__ == "__main__":
    main()
