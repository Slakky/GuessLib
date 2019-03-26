from django.db import models
from django.contrib.auth.models import User


class RefGenome(models.Model):
    name = models.CharField(max_length=100, default=None)
    path = models.CharField(max_length=100, default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class Result(models.Model):
    title = models.CharField(max_length=100)
    date_submit = models.DateTimeField(auto_now_add=True)
    nr_of_seqs_fout = models.IntegerField(default=None, null=True)
    fout_avg_quality = models.FloatField(default=None, null=True)
    fin_avg_quality = models.FloatField(default=None, null=True)
    collected_pairs = models.IntegerField(default=None, null=True)
    analysis_time = models.FloatField(default=None, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    refgenome = models.ForeignKey(RefGenome, on_delete=models.CASCADE)
    libtype = models.CharField(max_length=10, default=None, null=True)
    inwfwd = models.IntegerField(default=None, null=True)
    inwrvs = models.IntegerField(default=None, null=True)
    outfwd = models.IntegerField(default=None, null=True)
    outrvs = models.IntegerField(default=None, null=True)
    single = models.BooleanField(default=None)
<<<<<<< HEAD
=======
    progress = models.IntegerField(default = 0, null=True)
>>>>>>> f54b90092c6a6fb9f26da8faad07ddf5460a4828

    def __str__(self):
        return self.title


# post that user created user.result_set.all()
