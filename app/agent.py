import datetime as dt
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from . import db
from .config import GROQ_API_KEY, BUSINESS, AGENT, SERVICES

@tool
def check_availability(date: str) -> str:
    """List free appointment hours (24h) for a date in YYYY-MM-DD format."""
    slots = db.free_slots(date)
    return f"Free hours on {date}: {slots}" if slots else f"No free slots on {date}."

@tool
def book_appointment(name: str, service: str, date: str, hour: int, config: RunnableConfig) -> str:
    """Book an appointment. date=YYYY-MM-DD, hour=24h integer. Call only after the caller confirms."""
    phone = config["configurable"]["thread_id"]
    return "Booked." if db.book(phone, name, service, date, hour) else "Slot taken. Offer other times."

@tool
def my_appointments(config: RunnableConfig) -> str:
    """List this caller's upcoming appointments with their ids."""
    return str(db.mine(config["configurable"]["thread_id"]) or "None")

@tool
def cancel_appointment(appointment_id: int, config: RunnableConfig) -> str:
    """Cancel one of this caller's appointments by id."""
    return "Cancelled." if db.cancel(config["configurable"]["thread_id"], appointment_id) else "Not found."

def system_prompt(_state) -> list:
    today = dt.datetime.now().strftime("%A %Y-%m-%d")
    msg = (f"You are {AGENT}, the receptionist of {BUSINESS}. Today is {today}. "
           f"Services: {', '.join(SERVICES)}. Reply in the caller's language (English, Hindi or Hinglish). "
           "Keep replies to 1-2 short sentences, spoken style, no markdown. "
           "Collect name, service, day and time, check availability with the tool, "
           "read the details back, and only book after the caller says yes. "
           "Never invent availability. Politely refuse unrelated requests.")
    return [("system", msg)] + _state["messages"]

llm = ChatGroq(api_key=GROQ_API_KEY, model="llama-3.3-70b-versatile", temperature=0.3)
graph = create_react_agent(
    llm, [check_availability, book_appointment, my_appointments, cancel_appointment],
    state_modifier=system_prompt, checkpointer=MemorySaver())

async def reply(phone: str, text: str) -> str:
    out = await graph.ainvoke({"messages": [("user", text)]},
                              config={"configurable": {"thread_id": phone}})
    return out["messages"][-1].content
