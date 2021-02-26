from django.db import models



""" よくある質問モデル """

class Question(models.Model):
    class Meta():
        db_table = 't_question'
        verbose_name = 'よくある質問'
        verbose_name_plural = 'よくある質問'

    id = models.AutoField(primary_key=True, editable=False)
    question = models.CharField(max_length=255, null=False, blank=False)
    awnser = models.CharField(max_length=1000, null=False, blank=False)

    def __str__(self):
        return self.question
