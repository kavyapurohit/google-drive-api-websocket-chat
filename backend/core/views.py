from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os
import json
import io

# ✅ Allow insecure transport for development (Remove this in production)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def homepage(request):
    return JsonResponse({"message": "Welcome to the API!"})
    # ✅ Home View (Check if User is Authenticated)
def home(request):
    if "credentials" in request.session:
        return JsonResponse({"message": "User authenticated!", "status": "success"})
    else:
        return JsonResponse({"error": "User not authenticated. Please log in again."}, status=401)

# ✅ Upload File to Google Drive
def upload_file_to_drive(request):
    if "credentials" not in request.session:
        return JsonResponse({"error": "User is not authenticated with Google Drive"}, status=401)

    try:
        creds_data = json.loads(request.session["credentials"]) if isinstance(request.session["credentials"], str) else request.session["credentials"]
        creds = Credentials.from_authorized_user_info(creds_data)
        service = build("drive", "v3", credentials=creds)

        file_metadata = {"name": "sample.txt"}
        media = MediaFileUpload("sample.txt", mimetype="text/plain")
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()

        return JsonResponse({"file_id": file.get("id")})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ✅ List Google Drive Files
def list_drive_files(request):
    if "credentials" not in request.session:
        return JsonResponse({"error": "User is not authenticated with Google Drive"}, status=401)

    try:
        creds_data = json.loads(request.session["credentials"]) if isinstance(request.session["credentials"], str) else request.session["credentials"]
        creds = Credentials.from_authorized_user_info(creds_data)
        service = build("drive", "v3", credentials=creds)

        results = service.files().list(pageSize=10, fields="files(id, name)").execute()
        return JsonResponse(results)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ✅ OAuth Configuration (Updated to Match Google Console)
CLIENT_CONFIG = {
    "web": {
        "client_id": "1073951443197-j1un7a1ghbm8urigsgn676053eu0t8g7.apps.googleusercontent.com",
        "project_id": "YOUR_PROJECT_ID",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_secret": "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",
        "redirect_uris": [
            "https://google-drive-api-websocket-chat.onrender.com/auth/callback/"
        ]
    }
}

# ✅ Google API Scopes
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/drive.file"
]

# ✅ Start Google OAuth Flow
def google_auth(request):
    flow = Flow.from_client_config(CLIENT_CONFIG, scopes=SCOPES)
    flow.redirect_uri = CLIENT_CONFIG["web"]["redirect_uris"][0]  # Use correct redirect URI

    auth_url, state = flow.authorization_url(prompt="consent")
    request.session["state"] = state  # Store state in session for security
    return HttpResponseRedirect(auth_url)

# ✅ OAuth Callback (Handles User Authentication)
def google_auth_callback(request):
    flow = Flow.from_client_config(CLIENT_CONFIG, scopes=SCOPES)
    flow.redirect_uri = CLIENT_CONFIG["web"]["redirect_uris"][0]
    
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials  # Get authenticated credentials
    credentials_json = credentials.to_json()  # Convert credentials to JSON
    
    request.session["credentials"] = credentials_json  # Store in session
    request.session.modified = True  # Ensure session is saved

    print("Session ID:", request.session.session_key)
    print("Stored Credentials:", credentials_json)  # Debugging

    # ✅ Redirect to authenticated page instead of login
    return redirect("https://google-drive-api-websocket-chat.onrender.com/home/")

# ✅ Check if user is authenticated (For debugging)
def home(request):
    if "credentials" in request.session:
        return JsonResponse({"message": "User authenticated!", "status": "success"})
    else:
        return JsonResponse({"error": "User not authenticated. Please log in again."}, status=401)

# ✅ Download File from Google Drive
def download_file(request, file_id):
    if "credentials" not in request.session:
        return JsonResponse({"error": "User is not authenticated with Google Drive"}, status=401)

    try:
        creds_data = json.loads(request.session["credentials"]) if isinstance(request.session["credentials"], str) else request.session["credentials"]
        creds = Credentials.from_authorized_user_info(creds_data)
        service = build("drive", "v3", credentials=creds)

        request_file = service.files().get_media(fileId=file_id)
        file_path = f"{file_id}.pdf"

        with open(file_path, "wb") as file:
            downloader = MediaIoBaseDownload(file, request_file)
            done = False
            while not done:
                status, done = downloader.next_chunk()

        return JsonResponse({"message": f"File {file_id} downloaded successfully!", "file_path": file_path})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
