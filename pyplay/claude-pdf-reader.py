"""
Claude is asked to summarize a PDF file containing the first few pages of an essay by Leo Tolstoy.

Example output:

 $ python claude-pdf-reader.py 
This appears to be the beginning of Tolstoy's critical essay on Shakespeare. Here's a brief summary:

The text shows Tolstoy expressing his strong disagreement with the widely held view of Shakespeare's greatness. He
explains that after reading Shakespeare's most famous works like "King Lear," "Romeo and Juliet," "Hamlet," and
"Macbeth," he felt repulsion and boredom rather than the expected pleasure. Despite spending 50 years repeatedly trying
to appreciate Shakespeare in various translations (Russian, English, German), his negative reaction remained
consistent.

At age 75, Tolstoy reports reading Shakespeare's complete works again and becoming firmly convinced that Shakespeare's
unquestioned status as a genius is "a great evil, as is every untruth." He chooses to analyze "King Lear" as an example
to demonstrate why he believes Shakespeare cannot be considered either a great genius or even an average author,
despite knowing his view goes against the majority opinion.

The text then begins to contrast Tolstoy's view with those of other critics like Dr. Johnson and Hazlitt who praised
"King Lear" highly. This sets up what appears to be a detailed critique of the play to follow.

This passage represents the opening of what seems to be a thorough questioning of Shakespeare's literary reputation by
one of Russia's greatest authors.
"""

import base64
from pathlib import Path

import anthropic
from anthropic.types import Message

anthropic_client = anthropic.Anthropic()


def get_resp(pdf_base64_enc: bytes) -> Message:
    return anthropic_client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Attached is a snippet of a PDF file. Can you please summarize it to me in brief and basic terms?",
                    },
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_base64_enc,
                        },
                    },
                ],
            }
        ],
    )


def pdf_as_base64_str(filepath: Path) -> str:
    if not (filepath.exists() and filepath.is_file()):
        raise ValueError(f"Invalid file: {filepath}")
    with filepath.open("rb") as f:  # mode rb to prevent decoding as characters
        binary = f.read()  # raw binary for whole file
        # print(f"debug: {len(binary)=}")

        # `encoded` is still binary type, but with the bytes rearranged into base64 encoding: 3 bytes (256^3)
        # is rewritten into a representation using 4 base64 characters (a-z, A-Z, 0-9, + and /),
        # (64 characters), because 256^3 == 64^4. So it expands the length of the binary output
        # by a factor of 1/3.

        encoded = base64.standard_b64encode(binary)
        # print(f"debug: {len(encoded)=}")
        b64_str = encoded.decode("utf-8")
        return b64_str


pdf = Path("data") / "tolstoy-on-shakespeare-selection.pdf"
enc = pdf_as_base64_str(pdf)
resp = get_resp(enc)
# print(type(resp), resp)

for content in resp.content:
    if content.type == "text":
        print(content.text)
