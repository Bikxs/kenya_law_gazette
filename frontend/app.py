import json
import os
from pprint import pprint

import boto3
import streamlit as st

# aws_access_key_id = "ASIA4MTWMIH7BIWA46AN"
# aws_secret_access_key = "yR3XdcW+bdk6tF75w6T3DhU+n3N1DIVB8NXL8IFE"
# aws_session_token = "IQoJb3JpZ2luX2VjEC4aCXVzLWVhc3QtMSJIMEYCIQDmMWEM+bIhydGi6/i6s8cwBjLAYEz+27ENZ+GpLtpptgIhAIb4RkgLIPkmB5V+/g0PjoxPh7qO1f8C4QitVJFKTFAZKvoCCKf//////////wEQABoMODUxNzI1NTMzNjk0IgxD1FnyfPAxz8gTl34qzgJuYFlm71FYaMpJmu96j+kVnajJ89Q+9Lw76PIegw//UMw8i9hfSIs6R7Hq0CJa/LBqNVvuJJ4xGx26h1ln89f1p30cAq8JD7mK+pn2F7+5IIatIkFNZsbSucGjXqCBdCM9/HxkyJiihVbqzPjRjkJc/CcWVoJbT0sbdScXhAxTI2GErQ9oMhZSabnLZrxHMjkcdIlUfYHeaI+fj3fFlX+W/VuqaCg/NorCq5QikryeengdwmwJ5nQXbe+W17wGnmyU7bWk9joLUuEIkLiIbo9HPrErLmKjESv0/oPimCGmya6A0zh8jDyvaz9iCmMRGrf72MQXVL2pQpkMkfdjbZukW+EGwNXzD7HP2tIP6L+g6HqgswSCs4eaal6ez8jZs5Wx01Jd0XjPTKkpP1t2IRArAqdDhaNV0rjEVtjfAXjTTij6QDZaLlfZbP3yrTlfMK+1k7kGOqYBM5EDPvMH8oHvfV5nVYcON2J5K1AdYEBwCX02K6xG7olGFJDmXXPOlFt88/0BtEPcYcxnOxOBNRxCkjSgMIFJOhqzMLsXjV7quDdqM1BPqjagpyU1T6ACVZ/LrYM6yQLUrlsWd5aqaKfWi2ZyDzqK6oyHorHJKMbuG+tsGvXWuhrV35rQ1pG7WJTLLYgbr7wyH/rALo1gtA2fcjuZWmkG+8aRv3CYiQ=="

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.environ.get('AWS_REGION', 'eu-central-1')

# Set page config
st.set_page_config(
    page_title="Kenya Law Gazette Assistant",
    page_icon="📚",
    layout="wide"
)


def get_credentials():
    return {
        'aws_access_key_id': AWS_ACCESS_KEY_ID,
        'aws_secret_access_key': AWS_SECRET_ACCESS_KEY,
        'region_name': AWS_REGION
    }


def display_agent_overview():
    st.sidebar.header("Agent Overview")
    st.sidebar.write("""
    Agent Name: **agent-kenya-law-gazete**
    Agent ID: **XKPAEPA1WP**\n
    A legal professional skilled in navigating Kenyan law gazette notices, providing research and interpretation services for statutes and regulations.
    """)


def display_usage_instructions():
    st.sidebar.header("How to use")
    st.sidebar.write("""
    1. Type your question about Kenyan law gazette notices in the input field.\n
    2. Click 'Submit' to send your question to the agent.\n
    3. The agent's response and trace information will be displayed below.\n
    """)


def display_credentials_note():
    st.sidebar.header("Note: AWS Credentials")
    st.sidebar.write("""
    This application uses AWS credentials loaded from environment variables.\n
    Ensure that you have properly set the following environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_REGION (optional, defaults to 'eu-central-1')
    """)


def invoke_agent(bedrock_client, user_input):
    request = {'inputText': user_input}
    response = bedrock_client.invoke_agent(
        agentId='XKPAEPA1WP',
        agentAliasId='LOOOUK9JP4',
        sessionId='streamlit-session',
        inputText=json.dumps(request),
        enableTrace=True
    )
    return response


def extract_text_from_eventstream(response):
    completion_data = []
    for event in response['completion']:
        if event.get('chunk'):
            chunk_data = event['chunk'].get('bytes')
            if chunk_data:
                completion_data.append(chunk_data.decode('utf-8'))

    full_completion = ''.join(completion_data)
    return full_completion


def display_agent_response(completion):
    st.subheader("Answer:")
    st.write(completion)


def display_trace_information(trace):
    trace = json.loads(trace)
    st.subheader("Trace Information:")
    st.json(trace)


def main():
    st.title("Kenya Law Gazette")

    display_agent_overview()
    display_usage_instructions()
    credentials = get_credentials()
    bedrock_client = boto3.client('bedrock-agent-runtime', **credentials)

    user_input = st.text_input("Enter your question about Kenyan law gazette notices")

    if st.button("Submit"):
        if user_input:
            try:
                response = invoke_agent(bedrock_client, user_input)
                pprint(response)
                completion = extract_text_from_eventstream(response=response)
                display_agent_response(completion)
                if 'trace' in response:
                    display_trace_information(response['trace'])
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a question about Kenyan law gazette notices.")


if __name__ == "__main__":
    main()
