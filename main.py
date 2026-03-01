from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str = Query(...)):
    q = q.strip()

    # 1. Ticket Status
    ticket_match = re.search(r"ticket\s+(\d+)", q, re.IGNORECASE)
    if "status" in q.lower() and ticket_match:
        ticket_id = int(ticket_match.group(1))
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": ticket_id
            })
        }

    # 2. Schedule Meeting
    meeting_match = re.search(
        r"on\s+(\d{4}-\d{2}-\d{2})\s+at\s+(\d{2}:\d{2})\s+in\s+(.+)",
        q,
        re.IGNORECASE
    )
    if "schedule" in q.lower() and meeting_match:
        date = meeting_match.group(1)
        time = meeting_match.group(2)
        meeting_room = meeting_match.group(3).strip().rstrip(".")
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": date,
                "time": time,
                "meeting_room": meeting_room
            })
        }

    # 3. Expense Balance
    expense_match = re.search(r"employee\s+(\d+)", q, re.IGNORECASE)
    if "expense" in q.lower() and expense_match:
        employee_id = int(expense_match.group(1))
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": employee_id
            })
        }

    # 4. Performance Bonus
    bonus_match = re.search(
        r"employee\s+(\d+).*?for\s+(\d{4})",
        q,
        re.IGNORECASE
    )
    if "bonus" in q.lower() and bonus_match:
        employee_id = int(bonus_match.group(1))
        current_year = int(bonus_match.group(2))
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": employee_id,
                "current_year": current_year
            })
        }

    # 5. Office Issue
    issue_match = re.search(
        r"issue\s+(\d+).*?for\s+the\s+(.+?)\s+department",
        q,
        re.IGNORECASE
    )
    if "report" in q.lower() and issue_match:
        issue_code = int(issue_match.group(1))
        department = issue_match.group(2).strip()
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": issue_code,
                "department": department
            })
        }

    return {"error": "Query not recognized"}


# -------- Render Production Block --------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
