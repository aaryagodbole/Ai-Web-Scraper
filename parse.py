from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

TEMPLATE = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully:\n\n"
    "1. Extract Information: Only extract the information that directly matches the provided description: {parse_description}.\n"
    "2. No Extra Content: Do not include any additional text, comments, or explanations in your response.\n"
    "3. Empty Response: If no information matches the description, return an empty string ('').\n"
    "4. Direct Data Only: Your output should contain only the data that is explicitly requested, with no other text."
)

prompt = ChatPromptTemplate.from_template(TEMPLATE)
model = OllamaLLM(model="phi")  # <-- you're using 'phi' model

chain = prompt | model

def parse_with_langchain(dom_chunks, parse_description, show_spinner=None):
    parsed_results = []

    for i, chunk in enumerate(dom_chunks):
        if show_spinner:
            with show_spinner(f"Parsing chunk {i+1} of {len(dom_chunks)}..."):
                result = chain.invoke({
                    "dom_content": chunk,
                    "parse_description": parse_description
                })
        else:
            result = chain.invoke({
                "dom_content": chunk,
                "parse_description": parse_description
            })
        parsed_results.append(result)

    return "\n".join(parsed_results)
