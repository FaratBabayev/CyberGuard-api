"""HTML greeting page: GET /api/v1/greeting"""
from html import escape

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/api/v1", tags=["greeting"])

PROJECT_NAME = "CyberGuard"
PROJECT_DESCRIPTION = (
    "CyberGuard is an AI-powered security log analyzer. Students and junior analysts "
    "upload Linux SSH authentication logs, and the system detects suspicious activity "
    "such as brute-force logins and records it as incidents."
)
API_VERSION = "v1"

# TODO: replace with your real names, student IDs and what each person built.
TEAM = [
    ("Babayev Farat", "22781", "Greeting page and incident read endpoints"),
    ("Guliyev Farid", "21464", "Incident create, update and delete with validation"),
    ("Atayev Elgun", "20561", "Authentication, role checks and documentation"),
]

ENDPOINTS = [
    ("GET", "/api/v1/greeting", "This HTML welcome page"),
    ("GET", "/api/v1/incidents", "List incidents (supports page, perPage, status, severity)"),
    ("GET", "/api/v1/incidents/{id}", "Get one incident"),
    ("POST", "/api/v1/incidents", "Create an incident"),
    ("PUT", "/api/v1/incidents/{id}", "Update an incident"),
    ("DELETE", "/api/v1/incidents/{id}", "Delete an incident"),
]

TOKENS = [
    ("user-a-token", "User A: manages only their own incidents"),
    ("user-b-token", "User B: manages only their own incidents"),
    ("admin-token", "Administrator: manages all incidents"),
]

CSS = """
:root { --bg:#f4f6fa; --card:#ffffff; --text:#1c2333; --muted:#5b6478;
        --accent:#1d4ed8; --border:#dde2ec; }
* { box-sizing: border-box; }
body { margin:0; font-family:-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
       background:var(--bg); color:var(--text); line-height:1.6; }
.container { max-width:900px; margin:0 auto; padding:24px 16px 48px; }
header { margin-bottom:24px; }
h1 { margin:0 0 8px; font-size:2rem; }
h2 { margin:0 0 12px; font-size:1.2rem; }
p { margin:0; color:var(--muted); }
.badge { display:inline-block; margin-top:12px; padding:4px 12px; border-radius:999px;
         background:#dcfce7; color:#166534; font-size:.9rem; font-weight:600; }
section { background:var(--card); border:1px solid var(--border); border-radius:12px;
          padding:20px; margin-bottom:16px; }
.table-wrap { overflow-x:auto; }
table { width:100%; border-collapse:collapse; font-size:.95rem; }
th, td { text-align:left; padding:8px 10px; border-bottom:1px solid var(--border);
         vertical-align:top; }
th { color:var(--muted); font-weight:600; }
code { font-family:Menlo,Consolas,monospace; font-size:.9rem; background:#eef1f7;
       padding:2px 6px; border-radius:6px; white-space:nowrap; }
.method { font-weight:700; color:var(--accent); }
@media (max-width:600px) { h1 { font-size:1.6rem; } section { padding:16px; } }
"""


def _rows(rows, code_columns=()):
    out = []
    for row in rows:
        cells = []
        for i, value in enumerate(row):
            text = escape(value)
            if i in code_columns:
                text = f"<code>{text}</code>"
            cells.append(f"<td>{text}</td>")
        out.append("<tr>" + "".join(cells) + "</tr>")
    return "\n".join(out)


def build_page() -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(PROJECT_NAME)} API</title>
  <style>{CSS}</style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Welcome to {escape(PROJECT_NAME)}</h1>
      <p>{escape(PROJECT_DESCRIPTION)}</p>
      <span class="badge">API is running &middot; version {escape(API_VERSION)}</span>
    </header>

    <section>
      <h2>Team members</h2>
      <div class="table-wrap"><table>
        <tr><th>Name</th><th>Student ID</th><th>What they built</th></tr>
        {_rows(TEAM)}
      </table></div>
    </section>

    <section>
      <h2>Available endpoints</h2>
      <div class="table-wrap"><table>
        <tr><th>Method</th><th>Path</th><th>Description</th></tr>
        {_rows(ENDPOINTS, code_columns=(1,))}
      </table></div>
    </section>

    <section>
      <h2>Mock tokens for testing</h2>
      <p>Send as <code>Authorization: Bearer &lt;token&gt;</code></p>
      <div class="table-wrap"><table>
        <tr><th>Token</th><th>Access</th></tr>
        {_rows(TOKENS, code_columns=(0,))}
      </table></div>
    </section>
  </div>
</body>
</html>"""


@router.get("/greeting", response_class=HTMLResponse)
async def greeting():
    return HTMLResponse(content=build_page(), media_type="text/html; charset=utf-8")
