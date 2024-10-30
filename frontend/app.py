import boto3
import streamlit as st
from botocore.exceptions import ClientError

client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"


def generate_response(prompt):
    try:
        # Send the message to the model, using a basic inference configuration.
        response = client.converse(
            modelId=model_id,
            messages=prompt,
            inferenceConfig={"maxTokens": 2000, "temperature": 0},
            additionalModelRequestFields={"top_k": 3}
        )

        response_text = response["output"]["message"]["content"][0]["text"]
    except (ClientError, Exception) as e:
        response_text = f"ERROR: Can't invoke '{model_id}'.\nReason: {e}"
        print(response_text)
    return response_text


def main():
    st.title("Kenya Law Gazettes")
    st.subheader("Ask me anything about Kenya law gazettes from 2020 to date")

    user_input = st.text_input("Enter your question:")

    if user_input:
        response = generate_response(user_input)
        st.text_area("Response:", response)

if __name__ == '__main__':
    main()
