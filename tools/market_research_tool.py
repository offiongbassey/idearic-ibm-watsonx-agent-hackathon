from ibm_watsonx_orchestrate.agent_builder.tools import tool
from dotenv import load_dotenv
import requests
import os

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

@tool(name="research_idea", description="Searches the web for insights related to a business idea.")
def research_idea(idea: str) -> str:
    if not SERPER_API_KEY:
        return "Missing SERPER_API_KEY environment variable."

    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": idea
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        insights = []
        for result in data.get("organic", [])[:3]:
            insights.append(f"- {result['title']}: {result['snippet']} ({result['link']})")

        return "Here are some insights from the web:\n\n" + "\n".join(insights)

    except Exception as e:
        return f"Error fetching research insights: {str(e)}"