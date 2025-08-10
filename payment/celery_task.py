from celery import shared_task
from .models import FileUpload
from activity_log.models import ActivityLog
from docx import Document


@shared_task
def process_file_word_count(file_id):
    """
    """
    try:
        file = FileUpload.objects.get(id=file_id)
        # File Path
        file_path = file.file.path
        print('---- file patha ', file_path)
        # Read file content based on file extension
        # update file obj in case of extension mismatch
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='urf-8') as f:
                text = f.read()
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        else:
            file.status = 'failed'
            file.save()
            return
        print('------ txt ', text)
        # Count word & update file object
        word_count = len(text.split())
        file.word_count = word_count
        file.status = 'completed'
        file.save()
    except:
        file.status = 'failed'
        file.save()