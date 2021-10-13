from django.db import models

class Tag(models.Model):
    name = models.CharField(verbose_name = "название ключевого слова", max_length = 150)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    class Meta:
        verbose_name        = u"Ключевое слово"
        verbose_name_plural = u"Ключевые слова"

class News(models.Model):
    name = models.CharField(verbose_name = "название новости", max_length = 150)
    publication_date = models.DateTimeField(verbose_name = 'дата публикации', auto_now_add = True)
    tags = models.ForeignKey('home_page.Tag', on_delete = models.DO_NOTHING, related_name = "tagged_news")
    description = models.TextField("описание")

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name

    class Meta:
        verbose_name        = u"Новость"
        verbose_name_plural = u"Новости"
