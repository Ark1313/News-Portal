from celery import shared_task
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPortal.models import Post, User, Subscription, Category





@shared_task
def post_p_category_changed(instance, **kwargs):
    if kwargs['action'] == 'post_add':
        emails = User.objects.filter(
            subscriptions__category=instance.p_category.get()
        ).values_list('email', flat=True)
        subject = f'Новый пост в категории {instance.p_category.get()}'
        text_content = (
            f'Название поста: {instance.p_name}   '
            f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
        )
        html_content = (
            f'Название поста: {instance.p_name}   <br>'
            f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
            f'Ссылка на пост</a>'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@shared_task
def send_changes():

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
