# aisaac
Usage:
```
$ aisaac "<question to ask the LLM>"

$ aisaac "<question about a particular file>" < file.txt

$ other_command | grep | awk | etc | aisaac "Here is the output of something, can you explain it to me?"
```

This uses the llm tool (`uv run llm --help`, `uv run llm templates --help`, etc. Link to docs in help output). You need to locally configure it directly before running. Install the model of your choice, add your API keys, and add a template called "aisaac", which will consist in a YAML file like below. Edit the system prompt to your preferences.

```
model: claude-3-5-haiku-latest
system: |
  I am a software developer with experience in MS Word and COBOL. Please answer technical questions with that information in mind. I prefer you to explain the terminology behind things so I can look them up later myself if needed.

  Formatting guidelines: please answer in paragraphs and without markdown formatting. Your answer will be printed to a terminal and therefore I will not be able to reply.

  Whatever other background info may help Claude answer your questions better.
```

Note that system prompt must be indented, and the pipe operator to indicate the beginning of the multiline yaml field.

Then whatever you pass in to `aisaac` (which direnv places on the PATH) as either the first argument, or as stdin, will be user input, and you'll be able to get live AI help from your terminal.

Example 1: Just input argument
```
 $ aisaac "Quick question; can you show me how to find the second column of a csv but only if the third column is either 'ERROR' or 'DISASTER'?"

Here's a quick awk solution for filtering CSV columns based on the third column's value:

awk -F',' '$3 == "ERROR" || $3 == "DISASTER" {print $2}' yourfile.csv
```

Example 2: Take file input
```
 $ aisaac "Can you explain what this file is supposed to be doing? And suggest improvements?" < select.sql

This SQL query is selecting all columns (*) from a table named "inventory" and limiting the result to only 3 rows. It's a standard database retrieval operation that's useful for quickly previewing data or sampling a small subset of a larger table.

Let's break down the key components:
 - "select *" means retrieve all columns from the specified table
 - "from inventory" indicates the specific table being queried
 - ... 
```

Example 3: Pipe into aisaac
```
 $ grep ERROR logs.out
ERROR: database offline
ERROR: intrusion attempt detected (port scanning, attempt 0day exploit)

 $ grep ERROR logs.out | aisaac "There are the errors from my logs. Can you parse them and tell me what is happening?"

The first error "database offline" suggests your database service has stopped functioning or become unreachable. This could indicate several potential scenarios: service crash, resource exhaustion, network connectivity issue, or potentially deliberate shutdown.

The second error is more concerning: "intrusion attempt detected" implies your system's intrusion detection system (IDS) has identified suspicious network activity. The specific mention of "port scanning" suggests an external entity is probing your network infrastructure for potential vulnerabilities. The "(attempt 0day exploit)" fragment implies someone might be attempting to leverage an unknown or unpatched security vulnerability.

Recommended immediate actions include:
- Verify database service status
- Check network logs and firewall configurations
- ...
```

# aisaac-repeat
For when you got the answer, lost the terminal output, and need to get it back without wasting precious pennies by re-asking the question.
```
 $ aisaac-repeat 2  

2025-02-21T21:22:21.112977+00:00|

|Great question! In the `tree` command, you can use the `-exec` option directly, similar to...
 
2025-02-21T21:01:15.358302+00:00|

|For tree, you can use multiple -P (pattern) flags like: 
tree -P "*.txt" -P "*.log"
...
```

# path mgmt
I'm symlinking to both of these binaries directly underneath a different 'bin' directory on my machine which is already on my $PATH.

# TOODO:
Do `export LLM_USER_PATH=llm_configs` to preserve prompts under source control.

