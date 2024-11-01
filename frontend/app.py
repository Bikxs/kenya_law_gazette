import json
from pprint import pprint

import boto3
import streamlit as st

# Set page config
st.set_page_config(
    page_title="Kenya Law Gazette Assistant",
    page_icon="📚",
    layout="wide"
)


def get_credentials():
    aws_access_key_id = 'ASIA4MTWMIH7NS4HQY3H'
    aws_secret_access_key = 'D3k2Y3RyOKa7LmRPgNy4lRC06sTIZkM4gb3RWSHn'
    aws_session_token = 'IQoJb3JpZ2luX2VjEDAaCXVzLWVhc3QtMSJHMEUCIHjHflgxRhgcKCyPrHwqOvYZHyPf0oYlghadSGrLowiXAiEA93Ew2EV1SQhhJPYfNcoXCda6rAn95rMfWS+xJTKxrmQq+gIIqf//////////ARAAGgw4NTE3MjU1MzM2OTQiDCXzyecMt1uV5tNxCirOAtqXMThCPK0qGu7l9S84EVD30gbwkNr2GSOyIgQFKgwb17LYBNnC9IA/LzcKyQtA7Vwy+zadCVsHR7dgEGTMj1+g8+Dizw8mNeHve+sLmNsPMuN2vlGQ8USg/nDHChM8Q5j0yC2CG0HpfdCT1JUTgxNmESQSaLmuOtnEQhviq81kqVeJ9WHr9iCJ/kjXpgajOClqAJc9NqOKtwdoCcVELMg9Qx3vuK5IuiF798JsWIgB3cBonHv1abiE5nRqeX5uXgdb00TH1mWPcTEMZysujTGecaF4l4TAN3CxfdwN/jgrvPnvy9QQL4uFg/JUnRAYpKAzmwaPmxEs5eF33rLqIhzYvsQnIUncp15wAef+Y+hg3jh2rFiI856Xi5fD6zabgdzgxPAMOVgLL4UDa+ov194kA5JR2ydj2pzDQdHZCkgda6siNRI+Qv8HWue026IwuOWTuQY6pwGnXIccsm5Z5MM8kKuRtIK+beb9C1GOTdBLOL3fYgF0KGnkxl9/fn/R/DGcV439wgGhYL+nrQ6YEAC+W7sWtyPQorpwWiSrfl5WUkiaBPiRjvYRE5RxwloTZV05h+X43rHwCobgJF3Pysh15+iJ1pq3DMJTrDBBSp418Hjv6h/+Hy43NbolE26okuJI+aPGYCBfppS3lsj9CP5vyzxW4pztUNAmGlHkzA=='
    return {
        'aws_access_key_id': aws_access_key_id,
        'aws_secret_access_key': aws_secret_access_key,
        'aws_session_token': aws_session_token,
        'region_name': "eu-central-1"
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
    # credentials = get_credentials()
    bedrock_client = boto3.client('bedrock-agent-runtime',region_name= "eu-central-1")

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
