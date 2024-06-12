from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    imie = models.CharField(max_length=30, default='Nieznane')
    nazwisko = models.CharField(max_length=30, default='Nieznane')
    wiek = models.PositiveIntegerField(default=0)

class Post(models.Model):
    autor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_("Autor"))
    tytul = models.CharField(max_length=60, verbose_name=_("Tytuł"))
    tresc = models.TextField(max_length=200, verbose_name=_("Treść"))
    data_publikacji = models.DateTimeField(auto_now_add=True, verbose_name=_("Data publikacji"))

    def __str__(self):
        return self.tytul

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posty")
        permissions = [
            ("can_add_post", _("Może dodać wpis")),
            ("can_change_post", _("Może zmienić wpis")),
            ("can_delete_post", _("Może usunąć wpis")),
        ]

class Komentarz(models.Model):
    post = models.ForeignKey(Post, related_name='komentarze', on_delete=models.CASCADE, verbose_name=_("Wpis"))
    autor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_("Autor"))
    tresc = models.TextField(verbose_name=_("Treść"))
    data_publikacji = models.DateTimeField(auto_now_add=True, verbose_name=_("Data publikacji"))

    def __str__(self):
        return f'Komentarz {self.autor} na {self.post}'

    class Meta:
        verbose_name = _("Komentarz")
        verbose_name_plural = _("Komentarze")
        permissions = [
            ("can_add_komentarz", _("Może dodać komentarz")),
            ("can_change_komentarz", _("Może zmienić komentarz")),
            ("can_delete_komentarz", _("Może usunąć komentarz")),
        ]