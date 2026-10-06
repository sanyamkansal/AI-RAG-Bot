import ollama

def generate_answer(question, context):
    prompt = f"""
Answer the user's question using ONLY the provided context.

Rules:
1. If the answer is present in the context, give the answer.
2. If the answer is NOT present in the context, say exactly:
   Information not found in the documents.
3. Never say "Information not found in the documents" when you have already found the answer.
4. Do not add unrelated information.
5. Use only information present in the context.
6. NEVER invent, complete, or reconstruct code.
7. If code is present, reproduce the relevant code exactly.
8. Do not create function names, variables, or syntax that are not present in the context.
9. Give a direct answer.

Context:
{context}

Question:
{question}

Answer:
"""
    response = ollama.generate(model="phi4-mini:latest", prompt=prompt, options={"temperature": 0})
    return response["response"]