from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse

class Author(models.Model):
    author = models.OneToOneField(User, verbose_name="имя автора", on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        ratingP = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += ratingP.get('postRating')

        ratingC = self.author.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += ratingC.get('commentRating')

        self.rating = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f' {User.objects.get(id=self.author_id).username} (#{self.author_id})'

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Category(models.Model):
    category = models.CharField(max_length=64, verbose_name="Категория", unique=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):
    # pk = unique
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания (Mmm DD YYYY)')
    title = models.CharField(max_length=128, verbose_name="Заголовок")
    contents = models.TextField(verbose_name="Содержание")
    rating = models.SmallIntegerField(default=0)
    postType = models.CharField(max_length=16, verbose_name="Тип", choices=[('news', "Новость"), ('article', "Статья")],
                                default='article')
    author = models.ForeignKey(Author, verbose_name="Автор", on_delete=models.CASCADE)
    postCategory = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return f'{self.title} - {self.created.strftime("%d.%m.%Y, %H:%M:%S")}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.contents[:123] + '...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ['created']


class PostCategory(models.Model):
    post = models.ForeignKey(Post, verbose_name="Пост", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)

    def __str__(self):
        return f'{Post.objects.get(id=self.post_id)} (Категория {Category.objects.get(id=self.category_id)})'

    class Meta:
        verbose_name = "Связь"
        verbose_name_plural = "Связи"

class Comment(models.Model):
    CommentPost = models.ForeignKey(Post, verbose_name="Имеющиеся посты", on_delete=models.CASCADE)
    Commentator = models.ForeignKey(User, verbose_name="Комментаторы", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    contents = models.TextField(verbose_name="Текст комментария")
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.CommentPost} <- {self.contents[:32]}... - {self.created.strftime("%d.%m.%Y, %H:%M:%S")}'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
