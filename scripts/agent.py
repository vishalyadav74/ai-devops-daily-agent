import os
from datetime import datetime
from github import Github, Auth
from groq import Groq
import random

# ================= CONFIG =================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "vishalyadav74/ai-devops-daily-agent"

# ================= INIT =================
client = Groq(api_key=GROQ_API_KEY)

auth = Auth.Token(GITHUB_TOKEN)
g = Github(auth=auth)

repo = g.get_repo(REPO_NAME)

# ================= PATH SETUP =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
content_dir = os.path.join(BASE_DIR, "content")
os.makedirs(content_dir, exist_ok=True)

# ================= STEP 1: TOPIC =================
topics = [
    "AI in DevOps",
    "Kubernetes automation",
    "CI/CD with AI",
    "Cloud cost optimization",
    "DevSecOps trends",
    "Infrastructure as Code",
    "Future of Cloud"
]

topic = random.choice(topics)

# ================= STEP 2: GENERATE CONTENT =================
prompt = f"""
Write a LinkedIn-style post on: {topic}

Include:
- Hook
- Simple explanation
- Real-world example
- 3 bullet points
- Conclusion
- Hashtags
"""

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}]
)

content = response.choices[0].message.content

# ================= STEP 3: FILE =================
date = datetime.now().strftime("%Y-%m-%d-%H-%M")
file_path = f"content/{date}.md"

# ================= STEP 4: PUSH =================
try:
    repo.get_contents(file_path)
    print("⚠️ File already exists")
except:
    repo.create_file(
        file_path,
        f"Daily AI DevOps Post {date}",
        content
    )
    print("🚀 Groq AI content pushed successfully!")