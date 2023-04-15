import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string

from NewsPortal.models import Post, User, Subscription, Category


logger = logging.getLogger(__name__)


def my_job():

    today = datetime.datetime.now()
    today_minus_7 = today - datetime.timedelta(days=7)
    subscribers = set(Subscription.objects.order_by('user').values_list('user', flat=True))
    subscribers_email = User.objects.filter(id__in=subscribers).values_list('id', 'username', 'email')
    for mail in subscribers_email:
        user_category = set(Subscription.objects.filter(user=mail[0]).values_list('category', flat=True))
        catname = set(Category.objects.filter(id__in=user_category).values_list('category', flat=True))
        postes = Post.objects.filter(p_create_date__gte=today_minus_7, p_category__in=user_category)
        html_content = render_to_string(
           'daily_post.html',
            {
                'catname': catname,
                'username': mail[1],
                'link': settings.LOGIN_REDIRECT_URL,
                'posts': postes,
            }
        )
        msg = EmailMultiAlternatives(
            subject='Новые статьи за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[mail],
            )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
