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

    q_original = q.strip()
    q_lower = q_original.lower()

    # -----------------------------
    # 1. Ticket Status
    # -----------------------------
    ticket_match = re.search(r"ticket.*?(\d+)", q_lower)
    if ticket_match and "status" in q_lower:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": int(ticket_match.group(1))
            })
        }

    # -----------------------------
    # 2. Schedule Meeting
    # -----------------------------
    date_match = re.search(r"\d{4}-\d{2}-\d{2}", q_original)
    time_match = re.search(r"\d{2}:\d{2}", q_original)
    room_match = re.search(r"in\s+(.+)", q_original, re.IGNORECASE)

    if ("schedule" in q_lower or "meeting" in q_lower) and date_match and time_match and room_match:
        meeting_room = room_match.group(1).strip().rstrip(".")
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": date_match.group(0),
                "time": time_match.group(0),
                "meeting_room": meeting_room
            })
        }

    # -----------------------------
    # 3. Expense Balance
    # -----------------------------
    expense_match = re.search(r"employee.*?(\d+)", q_lower)
    if expense_match and "expense" in q_lower:
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": int(expense_match.group(1))
            })
        }

    # -----------------------------
    # 4. Performance Bonus
    # -----------------------------
    bonus_emp_match = re.search(r"employee.*?(\d+)", q_lower)
    year_match = re.search(r"\b(20\d{2})\b", q_lower)

    if bonus_emp_match and year_match and "bonus" in q_lower:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(bonus_emp_match.group(1)),
                "current_year": int(year_match.group(1))
            })
        }

    # -----------------------------
    # 5. Office Issue
    # -----------------------------
    issue_match = re.search(r"issue.*?(\d+)", q_lower)
    dept_match = re.search(r"department\s+([a-zA-Z]+)", q_lower)

    if issue_match and dept_match and "report" in q_lower:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(issue_match.group(1)),
                "department": dept_match.group(1).capitalize()
            })
        }

    # If nothing matched
    return {
        "name": "unknown",
        "arguments": json.dumps({})
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
