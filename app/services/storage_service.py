from supabase import create_client
from app.core.config import settings
import uuid

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

BUCKET_NAME = "materials"


def upload_file(file_bytes: bytes, filename: str, content_type: str) -> str:
    ext = filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"

    supabase.storage.from_(BUCKET_NAME).upload(
        path=unique_filename,
        file=file_bytes,
        file_options={"content-type": content_type}
    )

    url = supabase.storage.from_(BUCKET_NAME).get_public_url(unique_filename)
    return url


def delete_file(file_path: str) -> None:
    filename = file_path.split("/")[-1]
    supabase.storage.from_(BUCKET_NAME).remove([filename])