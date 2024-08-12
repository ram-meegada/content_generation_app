from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import textwrap

def image_processing_assignment_solution(image_link, query):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    # example
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": query,
            },
            {"type": "image_url", "image_url": str(image_link)},
        ]
    )
    response = llm.invoke([message])
    result_qu = to_markdown(response.content)
    return result_qu


def to_markdown(text):
    text = text.replace('*', '').replace('#', '').replace("-", "")
    intent_text = (textwrap.indent(text, '', predicate=lambda _: True))
    return intent_text
