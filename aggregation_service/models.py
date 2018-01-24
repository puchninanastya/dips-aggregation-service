from django.db import models

class Token(models.Model):
    app_id = models.CharField(max_length=40)
    app_secret = models.CharField(max_length=128)
    token = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = "AppToken"
        verbose_name_plural = "AppTokens"

    def __str__(self):
        return "Toker for app {} is {}".format(self.app_id, self.token)
