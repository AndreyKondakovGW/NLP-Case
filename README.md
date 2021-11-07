# Система классификации и рекомендации научных статей
*Постановка задачи*
Необходимо реализовать систему, которая решает следующие задачи:
----------------------------------------------------------------
1) Обработка pdf документов, содержащих научные статьи. Выделение заголовка, описания (abstract) и параграфов статьи
2) Классификация научной статьи по её заголовку и описанию (abstract)
3) Рекомендация наиболее похожих статей по теме
4) Автоматическая генерация описания статей по теме
5) Если статья на медицинскую тему, то обучить NER модель для детекции названий болезней в статье. Например, hypothermia, polydipsia, amnesia, и.т.д. Набор данных можно найти здесь

# Структура проекта
Все файлы необходимые для работы проекта лежат в папке src/nlp_case. В папке /tests лежат примеры использования API  проекта.
# Примеры использования 
Данный проект реализует следующие запросы:
```
#Текущий адрес сервера
server_url = 'https://nlp-case-elia-morrison.cloud.okteto.net'
headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
```
1) Поиск ключевых слов в тексте
```
data = {
"text": ... #Текст в формате строки}
request = requests.get(server_url+ '/predict_keywords', json = data, headers=headers)
jsonData = json.loads(request.text)
#В ответ сервер возвращает json с списком ключевых слов текста
keywords = jsonData['result']
```
2) Просмотр всех ключевых слов в базе сервера
```
data = {
    "pattern": ... #Regex Патерн для ключевых слов,
    "number": ... #Количество ключевых слов}
}
request = requests.get(server_url+ '/get_keywords', json = data, headers=headers)
jsonData = json.loads(request.text)
#В ответ сервер возвращает json с списком ключевых слов загруженых в базу
keywords = jsonData['result']
```
3) Поиск статей в базе по ключевым словам
```
data = {"keywords": ... #Список ключевых слов}
request= requests.post(server_url + "/search_articles_with_keywords", json=data, headers=headers)
jsonData = json.loads(request.text)
articletext = jsonData['result']
#articletext - имеет вид списка обектов вида:
{
    "titel" : #Название статьи
    "pdf_link" : #Сылка на статью
    "site_link" : #Пдф ссылка
}
```
4) Поиск похожих статей

**!!! Статья должна иметь вид привычный для сайта arxiv.org содержать ключевые разделы: Abstract и Content**
```
headers = {
'Accept': "multipart/form-data",
'Content-Type': "application/pdf",
'Cache-Control': "no-cache",
}
#Загрузка ПДФ файла со статьёй

file = {
    'file': open('.\\articlePDF.pdf', 'rb')
}

request = requests.post(server_url+ '/find_similar_article', json={"data": "article"}, files=file)
article = json.loads(request.text)
# article имеет вида обекта:
{
    "titel": #Название статьи 
    "pdflink": #Сылка на статью
    "sitelink": #Пдф ссылка
}
```

5) Поиск названий болезней в тексте

```
data = {"text": #Текст для поиска терминов}

request = requests.get(server_url + '/find_disease_names')
jsonData = json.loads(request.text)
diseases = jsonData['diseases']
#На выходе список всех названий болезней в тексте
```
# Ссылки
1) Сылка на Хост сервера https://nlp-case-elia-morrison.cloud.okteto.net
2) Ссылка на отчёт о проделанной работе [doc](NLP-Case/Report_NLP_Case.docx)

