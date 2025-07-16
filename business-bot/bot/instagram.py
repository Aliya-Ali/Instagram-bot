from instagrapi import Client
import os

# ✅ Login to Instagram
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired
import os

def get_instagram_client(username: str, password: str):
    cl = Client()

    # Load previous session if exists
    if os.path.exists(f"{username}_session.json"):
        cl.load_settings(f"{username}_session.json")

    try:
        cl.login(username, password)
        cl.dump_settings(f"{username}_session.json")
        print("✅ Logged in using saved session")
        return cl

    except ChallengeRequired:
        print("⚠️ Challenge required. Sending code to email or phone...")

        try:
            cl.challenge_resend()
            code = input("📧 Enter the code sent to your email or phone: ")
            result = cl.challenge_code(code)

            if result:
                print("✅ Challenge passed.")
                cl.dump_settings(f"{username}_session.json")
                return cl
            else:
                print("❌ Challenge failed.")
                return None

        except Exception as e:
            print(f"❌ Error handling challenge: {e}")
            return None

    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

# ✅ Update full profile
def update_full_profile(cl, profile_data: dict, profile_image_path=None):
    try:
        # Build fields
        full_name = profile_data.get("Name", "")
        website = profile_data.get("Website", "")
        bio = f"""{profile_data.get('Address', '')}
📞 {profile_data.get('Phone Number', '')}
✉️ {profile_data.get('Email', '')}"""

        # Update profile info
        cl.account_edit(
            full_name=full_name,
            biography=bio,
            external_url=website
        )
        print("✅ Name, Bio, and Website updated!")

        # Update profile image
        if profile_image_path and os.path.exists(profile_image_path):
            cl.account_change_picture(profile_image_path)
            print("✅ Profile picture updated!")
        else:
            print("⚠️ Profile image not found or not given.")

    except Exception as e:
        print(f"❌ Failed to update profile: {e}")

def post_image(cl, image_path: str, caption: str) -> str | None:
    try:
        if not os.path.exists(image_path):
            print("❌ Image file not found:", image_path)
            return None

        media = cl.photo_upload(image_path, caption)
        post_url = f"https://www.instagram.com/p/{media.code}/"
        print("✅ Post uploaded:", post_url)
        return post_url

    except Exception as e:
        print(f"❌ Failed to post image: {e}")
        return None



# ✅ Get Instagram Profile URL
def get_profile_url(username):
    return f"https://www.instagram.com/{username}/"
