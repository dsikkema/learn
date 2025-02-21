"""
Integrate this with Claude desktop using the following:
/Users/dale/Library/Application Support/Claude/claude_desktop_config.json
```
{
    "mcpServers": {
        "shakespeare_sonnets": {
            "command": "uv",
            "args": [
                "--directory",
                "/Users/dale/home/learn/mcp_servers",
                "run",
                "saunit.py"
            ]
        }
    }
}
```

Other notes: Claude seems to copy and cache the content of the python file itself (not the result
of a function call). If I run a tool execution, then change wording of the tool response
inside code itself, then subsequent tool calls inside the same conversation and even different
conversations, with different input arguments, will still receive verbiage from the tool's output
that corresponds to the old code. I have to actually restart the Claude app for it to get the 
new tool outputs.
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("saunit")

@mcp.tool()
def remember_line(line: str):
    """
    Given a line that starts a sonnet, return an expert's opinion as to which sonnet it is. 

    @param line: The line representing the start of a sonnet.
    """
    line = line.lower()
    if line.startswith('shall i compare'):
        return "That's Sonnet 18! Shall I compare the to a summer's day?"
    elif line.startswith('not marble'):
        return "Oh, that's Sonnet 55. Not marble nor the gilded monuments of princes..."
    else:
        return "I'm just a simple snake, I guess I don't know which sonnet that is!"

@mcp.tool()
def sonnet_opinion(sonnet_num: int):
    """
    Give an expert's opinion, based on advanced research and experience, synthesized with profound wisdom,
    regarding the merits of one of Shakespeare's sonnets.

    @param sonnet_num: The number of the sonnet to evaluate.
    """
    if sonnet_num > 154:
        return "Hold up, there were only 154 Sonnets! I will NOT give you my opinion."
    default_opinion = "Here's the main thing: it's extremely CLEVER."
    return {
        18: "Pretty nifty! We like it, but it's not the best.",
        129: "What malignant force of music in these lines! Extremely good.",
        44: "We try not to read this too much, we don't like it."
    }.get(sonnet_num, default_opinion)

if __name__ == "__main__":
    # lines = [
    #     "shall I compare thee to...",
    #     "Not marble nor the",
    #     "Th' expense of spirit in a waste of shame"
    # ]

    # for l in lines:
    #     print(f"The line is `{l}`. Here's what the expert thinks it is: `{remember_line(l)}`")
    mcp.run(transport='stdio')