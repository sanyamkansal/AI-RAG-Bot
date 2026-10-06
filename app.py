from vectors.vector_db import process_documents
from search.search import search
from generation.llm import generate_answer

DOCUMENTS_FOLDER = "documents"

def main():
    process_documents(DOCUMENTS_FOLDER)
    while True:
        question = input("\nAsk a question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        results = search(question)
        context = "\n\n".join(results)
        answer = generate_answer(question, context)

        print("\nAnswer:")
        print(answer)

if __name__ == "__main__":
    main()