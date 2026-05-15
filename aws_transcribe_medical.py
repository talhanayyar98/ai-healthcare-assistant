import os
import time
import uuid
from typing import Any

import requests
from dotenv import load_dotenv

try:
    import boto3
except ImportError:  # pragma: no cover
    boto3 = None

load_dotenv()


def transcribe_medical_audio(uploaded_file) -> dict[str, Any]:
    if uploaded_file is None:
        return {
            "status": "skipped",
            "provider": "Amazon Transcribe Medical",
            "transcript": None,
            "job_name": None,
            "errors": [],
        }

    if boto3 is None:
        return _unavailable("boto3 is not installed.")

    bucket = os.getenv("AWS_TRANSCRIBE_INPUT_BUCKET")
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    language_code = os.getenv("AWS_TRANSCRIBE_LANGUAGE_CODE", "en-US")
    specialty = os.getenv("AWS_TRANSCRIBE_MEDICAL_SPECIALTY", "PRIMARYCARE")
    transcription_type = os.getenv("AWS_TRANSCRIBE_TYPE", "DICTATION")

    if not bucket:
        return _unavailable("AWS_TRANSCRIBE_INPUT_BUCKET is not configured.")

    try:
        session = boto3.Session(region_name=region)
        s3_client = session.client("s3")
        transcribe_client = session.client("transcribe")
    except Exception as exc:
        return _unavailable(str(exc))

    extension = _guess_extension(uploaded_file)
    media_format = extension.replace(".", "")
    object_key = f"symptom-audio/{uuid.uuid4().hex}{extension}"
    file_bytes = uploaded_file.getvalue()

    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=object_key,
            Body=file_bytes,
            ContentType=getattr(uploaded_file, "type", "application/octet-stream"),
        )
    except Exception as exc:
        return _unavailable(f"S3 upload failed: {exc}")

    media_uri = f"s3://{bucket}/{object_key}"
    job_name = f"symptom-medical-{uuid.uuid4().hex[:24]}"

    try:
        transcribe_client.start_medical_transcription_job(
            MedicalTranscriptionJobName=job_name,
            LanguageCode=language_code,
            MedicalSpecialty=specialty,
            Type=transcription_type,
            OutputBucketName=bucket,
            MediaFormat=media_format,
            Media={"MediaFileUri": media_uri},
        )
    except Exception as exc:
        return _unavailable(f"StartMedicalTranscriptionJob failed: {exc}")

    deadline = time.time() + int(os.getenv("AWS_TRANSCRIBE_TIMEOUT_SECONDS", "180"))
    while time.time() < deadline:
        try:
            response = transcribe_client.get_medical_transcription_job(
                MedicalTranscriptionJobName=job_name
            )
        except Exception as exc:
            return _unavailable(f"GetMedicalTranscriptionJob failed: {exc}")

        job = response["MedicalTranscriptionJob"]
        status = job["TranscriptionJobStatus"]

        if status == "COMPLETED":
            transcript_uri = job["Transcript"]["TranscriptFileUri"]
            try:
                transcript_json = requests.get(transcript_uri, timeout=60).json()
                transcript = transcript_json["results"]["transcripts"][0]["transcript"].strip()
            except Exception as exc:
                return _unavailable(f"Transcript fetch failed: {exc}")

            return {
                "status": "ok",
                "provider": "Amazon Transcribe Medical",
                "transcript": transcript,
                "job_name": job_name,
                "errors": [],
            }

        if status == "FAILED":
            return {
                "status": "error",
                "provider": "Amazon Transcribe Medical",
                "transcript": None,
                "job_name": job_name,
                "errors": [job.get("FailureReason", "Medical transcription failed.")],
            }

        time.sleep(5)

    return {
        "status": "error",
        "provider": "Amazon Transcribe Medical",
        "transcript": None,
        "job_name": job_name,
        "errors": ["Timed out while waiting for transcription job completion."],
    }


def _guess_extension(uploaded_file) -> str:
    filename = getattr(uploaded_file, "name", "") or ""
    if "." in filename:
        return "." + filename.rsplit(".", 1)[1].lower()

    content_type = getattr(uploaded_file, "type", "") or ""
    mapping = {
        "audio/wav": ".wav",
        "audio/x-wav": ".wav",
        "audio/mpeg": ".mp3",
        "audio/mp3": ".mp3",
        "audio/mp4": ".mp4",
        "audio/x-m4a": ".m4a",
    }
    return mapping.get(content_type, ".wav")


def _unavailable(message: str) -> dict[str, Any]:
    return {
        "status": "unavailable",
        "provider": "Amazon Transcribe Medical",
        "transcript": None,
        "job_name": None,
        "errors": [message],
    }
