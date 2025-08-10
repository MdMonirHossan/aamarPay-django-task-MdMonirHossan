import logging
from django.forms.models import model_to_dict
from celery import shared_task
from .models import FileUpload
from activity_log.models import ActivityLog
from docx import Document

logger = logging.getLogger(__name__)

@shared_task
def process_file_word_count(file_id):
    """
    """
    try:
        file_obj = FileUpload.objects.get(id=file_id)
        # File Path
        file_path = file_obj.file.path
        
        # Read file content based on file extension
        # update file obj in case of extension mismatch
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        else:
            file_obj.status = 'failed'
            file_obj.save()
            return
        
        # Count word & update file object
        word_count = len(text.split())
        file_obj.word_count = word_count
        file_obj.status = 'completed'
        file_obj.save()

        # Create activity log for file update
        act = ActivityLog.objects.create(
            user = file_obj.user,
            action = 'File Processed',
            description = f"Processed file {file_obj.filename} and count word as well as update FileUpload model",
            metadata = {
                "id": file_obj.id,
                "file_path": file_obj.file.path,
                "filename": file_obj.filename,
                "status": file_obj.status,
                "word_count": file_obj.word_count,
                "upload_time": str(file_obj.upload_time)
            }
        )
    except Exception as e:
        file_obj.status = 'failed'
        file_obj.save()