import asyncio
from contextlib import AsyncExitStack
from typing import Optional

from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class ShakespeareChatClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    async def connect_to_server(self):
        """
        Connect this client to the MCP server

        @param server_script_path: Full path of the server script
        """

        # Client "connects" to this server by just running the server process.
        server_params = StdioServerParameters(
            command="uv",
            args=[
                "--directory",
                "/Users/dale/home/learn/mcp_servers",
                "run",
                "saunit.py",
            ],
            env=None,
        )

        # exit_stack.aclose is called in a cleanup() method that's called in a finally block in runloop
        self.stdio, self.write = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

    async def cleanup(self):
        await self.exit_stack.aclose()

    async def process_q_using_tools(self, query: str):
        """
        Given a query:
         - get response from server, conditioned upon the query AND the knowledge of available tools
         - process the response: capture 'text' content to display to chat user, and process 'tool_use' content
           by actually reaching out to the MCP server (using self.session) to call the tool
         - get a new response from the server, with all of its own previous messages passed in as context,
           as well as the results of tool calls (which are scoped under the "user" message role). Capture
           the text content of that response to also display to chat user.
        """
        messages = [{
            "role": "user",
            "content": query
        }]

        # ask the MCP server which tools it has available, so this can be passed to LLM to tell it what's at its
        # disposal
        tools_list = [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
            for tool in (await self.session.list_tools()).tools
        ]

        # init response, given query and knowledge of what tools are available
        first_resp = self.anthropic.messages.create(
            messages=messages,
            tools=tools_list,
            max_tokens=1000,
            model="claude-3-5-sonnet-latest",
        )
        print(first_resp)

        content_list = first_resp.content

        # add the assistant's own messages back into message context to retain "conversation history"
        messages.append({"role": "assistant", "content": content_list})

        user_display_text = []
        for content in content_list:
            if content.type == "text":
                user_display_text.append(content.text)
            if content.type == "tool_use":
                tool_result = await self.session.call_tool(content.name, content.input)
                tool_text = tool_result.content[0].text
                user_display_text.append(
                    f"Called tool={content.name} with input={content.input}"
                )
                messages.append(
                    {
                        "role": "user",
                        # kind of important note: content may be either string or a list, but
                        # a 1-lengthed content list must still be a list and not a single object
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": content.id,  # from message response
                                "content": tool_text,
                            }
                        ],
                    }
                )

        # get second response, given tool result
        next_resp = self.anthropic.messages.create(
            messages=messages,
            tools=tools_list,
            max_tokens=1000,
            model="claude-3-5-sonnet-latest",
        )
        print(next_resp)

        user_display_text.extend(
            [content.text for content in next_resp.content if content.type == "text"]
        )

        return "\n\n".join(user_display_text)

    async def chat_loop(self):
        try:
            await self.connect_to_server()
            print("Welcome to ShAIkespeare Chat")
            while True:
                q = input("Ask about evaluating one of Shakespeare's sonnets: ")
                resp = await self.process_q_using_tools(q)
                print(f"\nThank you for your patience! Here is the response:\n\n{resp}")
        finally:
            await self.cleanup()


if __name__ == "__main__":
    client = ShakespeareChatClient()
    asyncio.run(client.chat_loop())

"""
# get response, tool use example
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
                    }
                },
                "required": ["location"]
            }
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "What's the weather like in San Francisco?"
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "<thinking>I need to use get_weather, and the user wants SF, which is likely San Francisco, CA.</thinking>"
                },
                {
                    "type": "tool_use",
                    "id": "toolu_01A09q90qw90lq917835lq9",
                    "name": "get_weather",
                    "input": {"location": "San Francisco, CA", "unit": "celsius"}
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "toolu_01A09q90qw90lq917835lq9", # from the API response
                    "content": "65 degrees" # from running your tool
                }
            ]
        }
    ]
)

# messages response example with tool use
first_resp = self.anthropic.messages.create(...)
print(first_rep)
Message(
    id='msg_01CFhqx9GcxZE9wocHD39rPx',
    content=[
        TextBlock(
            citations=None,
            text="I'll call the sonnet_opinion tool for Sonnet 18 and share the expert's opinion with you.",
            type='text'
        ),
        ToolUseBlock(
            id='toolu_01R7deF1uZAqjCEiZw4uTnP1',
            input={'sonnet_num': 18},
            name='sonnet_opinion',
            type='tool_use'
        )
    ],
    model='claude-3-5-sonnet-20241022',
    role='assistant', stop_reason='tool_use', stop_sequence=None, type='message', usage=Usage(cache_creation_input_tokens=0, cache_read_input_tokens=0, input_tokens=627, output_tokens=83))

# Tool use response from server

tool_result = await self.session.call_tool(content.name, content.input)
print(tool_result)
CallToolResult(
    meta=None,
    content=[
        TextContent(
            type='text',
            text="Pretty nifty! We like it, but it's not the best."
        )
    ],
    isError=False
)
"""
