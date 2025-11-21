from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from kurs.models import Article, Author, Category, Tag


class ArticleAPITestCase(APITestCase):
    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        # Создаём вспомогательные объекты
        self.author = Author.objects.create(name="Назир Магомедов")
        self.category = Category.objects.create(name="Процессоры")
        self.tag1 = Tag.objects.create(name="AMD")
        self.tag2 = Tag.objects.create(name="Intel")

        # Создаём одну статью для проверки получения списков и деталей
        self.article = Article.objects.create(
            title="Существующая статья",
            content="Тестовый контент для проверки GET запросов",
            author=self.author,
            category=self.category,
            status="published"
        )
        self.article.tags.add(self.tag1)

        # URLs
        self.list_url = reverse('article-list')
        self.detail_url = reverse('article-detail', kwargs={'pk': self.article.pk})

    def test_list_articles(self):
        """GET /api/articles/ — получение списка статей"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Существующая статья")

    def test_retrieve_article(self):
        """GET /api/articles/{id}/ — получение одной статьи"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Существующая статья")

    def test_create_article_valid(self):
        """POST /api/articles/ — успешное создание статьи"""
        data = {
            "title": "Новая статья Ryzen 9 9950X",
            "content": "Обзор нового процессора...",
            "author": self.author.id,
            "category": self.category.id,
            "tags": [self.tag1.id, self.tag2.id],
            "status": "published"
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Article.objects.filter(title="Новая статья Ryzen 9 9950X").exists())

    def test_create_article_validation_error(self):
        """POST /api/articles/ — проверка валидации (отсутствует заголовок)"""
        data = {
            "title": "",  # Пустой заголовок недопустим
            "content": "Текст без заголовка",
            "author": self.author.id,
            "category": self.category.id,
            "tags": []
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_update_article(self):
        """PUT /api/articles/{id}/ — полное обновление статьи"""
        data = {
            "title": "Обновлённый заголовок",
            "content": "Новое содержание",
            "author": self.author.id,
            "category": self.category.id,
            "tags": [self.tag2.id],
            "status": "draft"
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.article.refresh_from_db()
        self.assertEqual(self.article.title, "Обновлённый заголовок")
        self.assertEqual(self.article.status, "draft")

    def test_delete_article(self):
        """DELETE /api/articles/{id}/ — удаление статьи"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Article.objects.filter(pk=self.article.pk).exists())

    def test_filter_articles(self):
        url = f"{self.list_url}?category={self.category.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['category'], self.category.id)