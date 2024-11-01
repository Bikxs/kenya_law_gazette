import json
import os

import boto3
import streamlit as st

aws_access_key_id = "ASIA4MTWMIH7JPHUBGDJ"
aws_secret_access_key = "AUzlsaSUJ9uCV2+C6bGy4Juuk6KwEHjXVxgGGNIR"

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', aws_access_key_id)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', aws_secret_access_key)
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
    st.sidebar.markdown("""
    **Name:** agent-kenya-law-gazete
    **ID:** XKPAEPA1WP
    **Description:** A legal professional skilled in navigating Kenyan law gazette notices, providing research and interpretation services for statutes and regulations.
    """)


def display_usage_instructions():
    st.sidebar.header("How to use")
    st.sidebar.write("""
    1. Type your question about Kenyan law gazette notices in the input field.<br>
    2. Click 'Submit' to send your question to the agent.<br>
    3. The agent's response and trace information will be displayed below.<br>
    """)


def display_credentials_note():
    st.sidebar.header("Note: AWS Credentials")
    st.sidebar.write("""
    This application uses AWS credentials loaded from environment variables.<br>
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
        inputText=json.dumps(request)
    )
    return response


def display_agent_response(response):
    completion = json.loads(response['completion'])
    st.subheader("Agent Response:")
    st.write(completion['text'])


def display_trace_information(response):
    trace = json.loads(response['trace'])
    st.subheader("Trace Information:")
    st.json(trace)


def main():
    st.title("Kenya Law Gazette Agent Interaction")

    display_agent_overview()
    display_usage_instructions()
    credentials = get_credentials()
    bedrock_client = boto3.client('bedrock-agent-runtime', **credentials)

    user_input = st.text_input("Enter your question about Kenyan law gazette notices")

    if st.button("Submit"):
        if user_input:
            try:
                response = invoke_agent(bedrock_client, user_input)
                display_agent_response(response)
                display_trace_information(response)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a question about Kenyan law gazette notices.")


if __name__ == "__main__":
    main()
