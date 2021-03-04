from django.db import models



""" ジョブモデル """

class Job(models.Model):
    class Meta():
        db_table = 't_job'
        verbose_name = 'ジョブ'
        verbose_name_plural = 'ジョブ'

    id = models.AutoField(primary_key=True, editable=False)
    job = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.job
