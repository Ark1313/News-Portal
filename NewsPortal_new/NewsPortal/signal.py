from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post
from django.core.mail import EmailMultiAlternatives


@receiver(m2m_changed, sender=Post.p_category.through)
def post_p_category_changed(sender, instance, **kwargs):
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
