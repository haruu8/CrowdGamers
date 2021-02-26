from django.db import models
import uuid



""" よくある質問モデル """

class Question(models.Model):
    class Meta():
        db_table = 't_question'
        verbose_name = 'よくある質問'
        verbose_name_plural = 'よくある質問'

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    question = models.CharField(max_length=255, null=False, blank=False)
    awnser = models.CharField(max_length=1000, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
