
from pyramid_celery import celery_app as app
from niimanga.tasks.batoto import build_from_latest
from niimanga.sites.batoto import Batoto


site = Batoto()

@app.task
def build_from_latest_batoto(*args, **kwargs):
    try:
        for i, source in enumerate(site.search_latest()):
            # LOG.info(source)
            print(source)
            build_from_latest(site, source)
    except Exception as e:
        print(e.message);