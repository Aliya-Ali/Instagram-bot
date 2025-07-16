from flask import Flask, render_template, request
from bot.google_sheets import connect_to_sheet, get_vertical_business_data, update_submission
from bot.instagram import  update_full_profile, get_profile_url, post_image
from bot.drive_fetcher import authenticate_drive
from bot.image import get_random_image_from_folder
import os
from instagrapi import Client
from bot.instagram import get_instagram_client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

SESSION_FILE = "session.json"
USERNAME = "AliyasDream"
PASSWORD = os.getenv("password1")





@app.route("/", methods=["GET", "POST"])
def index():
    message = "Click a button to update your profile or post on Instagram."
    profile_url = ""
    last_action = None
    username = USERNAME
    password = PASSWORD

    if request.method == "POST":
        action = request.form.get("action")
        last_action = action

        try:
            message = "📄 Connecting to Google Sheet..."
            sheet = connect_to_sheet("Cut Cost Roofing Info")
            data = get_vertical_business_data(sheet)

            message = "🔐 Logging into Instagram..."
            cl = get_instagram_client(username, password)
            if not cl:
                return render_template("index.html", message="❌ Login failed", profile_url="", last_action=action)

            image_path = get_random_image_from_folder("images")
            if not image_path:
                return render_template("index.html", message="❌ No image found", profile_url="", last_action=action)

            if action == "update_profile":
                message = "✏️ Updating profile..."
                update_full_profile(cl, data, image_path)
                profile_url = get_profile_url(USERNAME)
                update_submission(sheet, 1, profile_url)
                message = "✅ Profile updated successfully!"

            elif action == "post_feed":
                message = "📤 Posting to Instagram..."
                caption = f"{data['Name']}\n{data['Address']}\n📞 {data['Phone Number']}\n🌐 {data.get('Website', '')}"
                post_url = post_image(cl, image_path, caption)
                if post_url:
                    profile_url = post_url
                    update_submission(sheet, 1, post_url)
                    message = "✅ Post uploaded successfully!"
                else:
                    message = "❌ Failed to post image."

        except Exception as e:
            message = f"❌ Error: {str(e)}"

    return render_template("index.html", message=message, profile_url=profile_url, last_action=last_action)


if __name__ == "__main__":
    app.run(debug=True)
