from flask import Flask, render_template, request
from bot.google_sheets import connect_to_sheet, get_vertical_business_data, update_submission
from bot.instagram import login_instagram, update_full_profile, get_profile_url, post_image
from bot.drive_fetcher import authenticate_drive
import os
from bot.image import get_random_image_from_folder
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    message = "hi how can I help you"
    profile_url = ""
    action = "update_profile"
    if request.method == "POST":
        
        username = "AliyasDream"
        


        try:
            # Read sheet data
            sheet = connect_to_sheet("Cut Cost Roofing Info")
            print("✅ Connected to sheet")
            data = get_vertical_business_data(sheet)
            password = os.getenv("password1")
            print(password)
           

            # Login to Instagram
            cl = login_instagram(username, password)
            if not cl:
                return render_template("index.html", message="❌ Login failed", profile_url="")

            profile_url = get_profile_url(username)
            image_path = get_random_image_from_folder("images") # must exist

            if action == "update_profile":
                update_full_profile(cl, data, image_path)
                update_submission(sheet, 1, profile_url)
                message = "✅ Profile updated successfully!"
                bio_url = get_profile_url(username)
                profile_url = bio_url

            elif action == "post_feed":
                caption = f"{data['Name']}\n{data['Address']}\n📞 {data['Phone Number']}\n🌐 {data.get('Website', '')}"
                message = "✅ Posted successfully!"
                post_url = post_image(cl, image_path, caption)
                update_submission(sheet, 1, post_url)  # or to a separate column
                profile_url = post_url  # to display under button
                
        except Exception as e:
            # print("❌ Error:", e)
            message = f"Error: {e}"

    return render_template("index.html", message=message, profile_url=profile_url, last_action=action)

if __name__ == "__main__":
    app.run(debug=True)
