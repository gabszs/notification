import pytest

from notification.schemas.file_schema import FileMetadata
from notification.schemas.file_schema import QueueMessage


def test_file_metadata_valid():
    metadata = FileMetadata(file_name="video.mp4", content_type="video/mp4")
    assert metadata.file_name == "video.mp4"
    assert metadata.content_type == "video/mp4"


def test_file_metadata_invalid_content_type():
    with pytest.raises(ValueError, match="File Type not allowed, please send a video file"):
        FileMetadata(file_name="video.mp4", content_type="application/pdf")


def test_queue_message_valid():
    message = QueueMessage(
        file_name="audio.mp3",
        content_type="video/mp4",  # Assume that QueueMessage accepts video types as content_type
        client_email="client@example.com",
        download_link="song.mp3",
    )
    assert message.file_name == "audio.mp3"
    assert message.content_type == "video/mp4"
    assert message.client_email == "client@example.com"
    assert message.download_link == "song.mp3"


def test_queue_message_invalid_content_type():
    with pytest.raises(ValueError, match="File Type not allowed, please send a video file"):
        QueueMessage(
            file_name="audio.mp3",
            content_type="application/pdf",  # Invalid content type
            client_email="client@example.com",
            donwload_link="song.mp3",
        )


def test_queue_message_missing_fields():
    with pytest.raises(ValueError):
        QueueMessage(
            file_name="",  # Invalid file_name (must have min_length=1)
            content_type="video/mp4",
            client_email="client@example.com",
            donwload_link="song.mp3",
        )
