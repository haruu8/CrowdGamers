from django.db import models



class Job(models.Model):
    """
    希望枠のモデル。
    アドミンページからの追加しかできない。
    """
    class Meta():
        db_table = 't_job'
        verbose_name = '希望枠'
        verbose_name_plural = '希望枠'

    id = models.AutoField(primary_key=True, editable=False)
    job = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.job
