from django.urls import path
from core.views import google_auth, google_auth_callback, upload_file_to_drive, list_drive_files, download_file, homepage

urlpatterns = [
    path('', homepage, name='homepage'), 
    path('auth/', google_auth, name="google-auth"),
    path('auth/callback/', google_auth_callback, name="google-auth-callback"),
    path('drive/upload/', upload_file_to_drive, name='upload-file'),
    path('drive/list/', list_drive_files, name='list-drive-files'),
    path("drive/download/<str:file_id>/", download_file, name="download-file"),
]
