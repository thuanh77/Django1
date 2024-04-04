from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=450) #Заголовок поста
    author = models.ForeignKey( #Автор поста
        'auth.User',
        on_delete=models.CASCADE, #Удаление поста
    )
    body = models.TextField() #Поле поста

    def __str__(self): #Метод
        return self.title


