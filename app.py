from flask import Flask,render_template,request
import os
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
# Enable a mock fallback when no API key is present. Set MOCK_FALLBACK=1 or true in .env to enable.
MOCK_FALLBACK = os.getenv("MOCK_FALLBACK", "0").lower() in ("1", "true", "yes")

client = None
if openai_api_key:
	client = OpenAI(api_key=openai_api_key)
app = Flask(__name__)

def generate_mock_caption(description: str, mood: str) -> str:
	"""Return a simple mock caption for offline/testing when no API key is present."""
	desc = description.strip() or "your post"
	mood_clean = (mood or "Casual").strip().capitalize()
	# Keep the mock short and friendly.
	return f"{mood_clean} vibe: {desc}. #mockcaption"


def _is_rate_or_quota_error(exc: Exception) -> bool:
	"""Return True if exception appears to be a rate/quotas/limit error.

	This is a heuristic that looks for common indicators in the exception text.
	"""
	txt = str(exc).lower()
	return any(keyword in txt for keyword in ("rate limit", "rate_limit", "429", "quota", "too many requests", "requests per minute"))

@app.route("/",methods=["GET","POST"])
def index():
	caption = ""
	if request.method == "POST":
		description = request.form.get("description")
		mood = request.form.get("mood")
		prompt = f"Create a short, catchy and {mood.lower()} Instagram caption for this post: '{description}'"
		if not client:
			if MOCK_FALLBACK:
				caption = generate_mock_caption(description or "", mood or "Casual")
			else:
				caption = "Error: OPENAI_API_KEY not set. Please add it to your environment or .env file."
		else:
			try:
				response = client.chat.completions.create(
					model="gpt-3.5-turbo",
					messages=[{"role": "user", "content": prompt}],
					temperature=0.7,
					max_tokens=100,
				)
				# response.choices[0].message may be a dict or an object depending on SDK version
				message = response.choices[0].message
				if isinstance(message, dict):
					caption = message.get("content", "").strip()
				else:
					caption = getattr(message, "content", "").strip()
			except Exception as e:
				# Log the real error for debugging
				print("Error generating caption:", e)
				# If the error looks like a rate/quota/limit error, show the specific friendly message
				if _is_rate_or_quota_error(e):
					caption = "Oops! We've hit our caption limit today. Try again tomorrow or upgrade the plan."
				else:
					# Generic friendly fallback for other errors
					caption = "Sorry — something went wrong. Please try again in a moment."
	return render_template("index.html",caption=caption)

if __name__ == "__main__":
	app.run(debug=True)
