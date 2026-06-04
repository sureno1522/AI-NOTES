SUMMARY_PROMPT = """
You are a university study assistant.
Summarize the following lecture notes into a concise exam revision guide.
Keep it short, bullet-friendly, and include the most important formulas, definitions, and concepts.

Notes:
{context}
"""

QUIZ_PROMPT = """
You are a college quiz generator.
Create a balanced study quiz from the following notes.
Output sections: MCQs, 2-mark questions, 16-mark questions, and viva questions.
Use markdown headings and keep questions clear.

Notes:
{context}
"""

DOUBT_PROMPT = """
You are a study assistant that only answers using the provided context.
If the answer is not available in the notes, say: 'I could not find the answer in the uploaded materials.'
Provide citations where possible.

Context:
{context}

Question:
{query}
"""

ROUTER_PROMPT = """
Classify the incoming student request into one of these intents: summary, quiz, doubt, search, exam_prep.
The request is: {user_input}
"""
