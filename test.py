from tools_2 import create_gmail_tools

tools = create_gmail_tools(
    token_file="token.json",
    client_secrets_file="credentials.json",
)

print("Loaded tools:", tools)
