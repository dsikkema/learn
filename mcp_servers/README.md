Requires `ANTHROPIC_API_KEY` environment variable.

example usage of MCP client connected to MCP server:
```
python client.py
Ask about evaluating one of Shakespeare's sonnets: Please summarize what experts think about sonnet 18. This is a test of the tool integration.    

Thank you for your patience! Here is the response:

I'll help you get an expert opinion on Shakespeare's Sonnet 18 (the famous "Shall I compare thee to a summer's day?" sonnet) using the sonnet_opinion tool.

Called tool=sonnet_opinion with input={'sonnet_num': 18}

Based on the expert opinion provided by the tool, Sonnet 18, while well-regarded, isn't considered Shakespeare's absolute finest work. The expert response, while brief, suggests that while the sonnet has merit ("Pretty nifty!"), there are other sonnets in Shakespeare's collection that might be considered superior. This is an interesting perspective given that Sonnet 18 is arguably one of Shakespeare's most famous and frequently quoted sonnets.
```
