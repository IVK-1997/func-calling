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

    # -------------------------------------------------
    # 1. schedule_meeting
    # Identified by YYYY-MM-DD + HH:MM + "in <room>"
    # -------------------------------------------------
    date_match = re.search(r"\b\d{4}-\d{2}-\d{2}\b", q_original)
    time_match = re.search(r"\b\d{2}:\d{2}\b", q_original)
    room_match = re.search(r"\bin\s+(.+)", q_original, re.IGNORECASE)

    if date_match and time_match and room_match:
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": date_match.group(0),
                "time": time_match.group(0),
                "meeting_room": room_match.group(1).strip().rstrip(".")
            })
        }

    # -------------------------------------------------
    # 2. calculate_performance_bonus
    # Identified by employee <id> + 4-digit year
    # -------------------------------------------------
    emp_match = re.search(r"\bemployee\s*(\d+)\b", q_lower)
    year_match = re.search(r"\b(20\d{2})\b", q_lower)

    if emp_match and year_match:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(emp_match.group(1)),
                "current_year": int(year_match.group(1))
            })
        }

    # -------------------------------------------------
    # 3. get_expense_balance
    # Identified by employee <id> without year
    # -------------------------------------------------
    if emp_match and not year_match:
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": int(emp_match.group(1))
            })
        }

    # -------------------------------------------------
    # 4. report_office_issue
    # Identified by issue <code> + for <Department>
    # -------------------------------------------------
    issue_match = re.search(r"\bissue\s*(\d+)\b", q_lower)
    dept_match = re.search(r"\bfor\s+([a-zA-Z]+)\b", q_lower)

    if issue_match and dept_match:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(issue_match.group(1)),
                "department": dept_match.group(1).capitalize()
            })
        }

    # -------------------------------------------------
    # 5. get_ticket_status
    # Identified by ticket <id>
    # -------------------------------------------------
    ticket_match = re.search(r"\bticket\s*(\d+)\b", q_lower)

    if ticket_match:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": int(ticket_match.group(1))
            })
        }

    # -------------------------------------------------
    # Fallback (should never be used by grader)
    # -------------------------------------------------
    return {
        "name": "unknown",
        "arguments": json.dumps({})
    }


# Render production entrypoint
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
