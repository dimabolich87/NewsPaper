from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def update_rating(self):
        # Получаем суммарный рейтинг автора на основе его статей
        # author_articles_rating = Post.objects.filter(author=self).aggregate(post_rating=Sum('rating_post'))
        author_articles_rating = self.post_set.all().aggregate(post_rating=Sum('rating_post'))
        # Получаем суммарный рейтинг автора на основе его комментариев
        author_comments_rating = self.user.comment_set.all().aggregate(com_rating=Sum('comment_rating'))
        # Получаем суммарный рейтинг автора на основе комментариев к его статьям
        all_comments_to_author_articles_rating = Comment.objects.filter(post__author=self.id)
        return author_articles_rating * 3 + author_comments_rating + all_comments_to_author_articles_rating


class Category(models.Model):
    name_category = models.CharField(max_length=255, unique=True)

class Post(models.Model):
    article = 'AR'
    news = 'NW'

    POST_TYPES = [
        (article, 'статья'),
        (news, 'новость'),
        ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_types = models.CharField(choices=POST_TYPES, max_length=2)
    date_time_post = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title_post = models.CharField(max_length=255)
    text_post = models.TextField()
    rating_post = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def like(self):
        self.likes +=1
        self.save()

    def dislike(self):
        self.dislikes +=1
        self.save()

    def preview(self):
        return self.text_post[:124] + '...' if len(self.text_post) > 124 else self.text_post

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    date_time_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like_comment(self):
        self.rating_comment +=1
        self.save()

    def dislike_comment(self):
        self.rating_comment -=1
        self.save()