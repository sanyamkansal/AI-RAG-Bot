def chunk_text(text, chunk_size=500, overlap=50):
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""

    for paragraph in paragraphs:
        if len(current) + len(paragraph) <= chunk_size:
            current += paragraph + "\n\n"
        else:
            if current.strip():
                chunks.append(current.strip())

            current = paragraph + "\n\n"

    if current.strip():
        chunks.append(current.strip())

    return chunks