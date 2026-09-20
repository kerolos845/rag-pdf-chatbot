import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END

load_dotenv()


class AgentState(TypedDict):
    topic: str
    research_notes: str
    final_report: str


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    reasoning_format="hidden"
)


def researcher_node(state: AgentState):
    topic = state["topic"]
    prompt = (
        f"Conduct technical research on the following topic and extract "
        f"key concepts, technical mechanisms, and dynamic architectures: {topic}"
    )
    try:
        response = llm.invoke([
            SystemMessage(content="You are an expert technical researcher."),
            HumanMessage(content=prompt)
        ])
        notes = response.content
        print(f"[DEBUG] research_notes length: {len(notes)}")  # سطر تشخيصي مؤقت
        return {"research_notes": notes}
    except Exception as e:
        return {"research_notes": f"[ERROR: research failed - {e}]"}


def writer_node(state: AgentState):
    notes = state["research_notes"]

    # لو الـ researcher فشل، مفيش داعي نضيع API call على الكاتب
    if notes.startswith("[ERROR"):
        return {"final_report": f"Report generation skipped due to research failure.\n\n{notes}"}

    prompt = f"Using these research notes, write a structured, clear technical report in Markdown:\n\n{notes}"
    try:
        response = llm.invoke([
            SystemMessage(content="You are a professional technical writer."),
            HumanMessage(content=prompt)
        ])
        return {"final_report": response.content}
    except Exception as e:
        return {"final_report": f"[ERROR: report generation failed - {e}]"}


workflow = StateGraph(AgentState)
workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)

workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", END)

app = workflow.compile()

if __name__ == "__main__":
    initial_state = {
        "topic": "Multi-Agent Systems with LangGraph",
        "research_notes": "",
        "final_report": ""
    }
    output = app.invoke(initial_state)
    print("--- Final Generated Report ---")
    print(output["final_report"])
