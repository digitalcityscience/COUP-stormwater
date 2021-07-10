from celery import Celery

app = Celery('guineapig')
app.config_from_object('config')

if __name__ == '__main__':
    app.start()
