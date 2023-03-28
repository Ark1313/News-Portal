from django_filters import FilterSet, ModelChoiceFilter, DateFilter, Filter
from .models import Post, Category

# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    datefilter = DateFilter(
        field_name='p_create_date',
        lookup_expr='gt',
    )

    pnamefilter = Filter(
        field_name='p_name',
        lookup_expr='icontains',
    )

    pcategoryfilter = ModelChoiceFilter(
        label='Выберите категорию :',
        field_name='postcategory__pc_category',
        queryset=Category.objects.all(),
        empty_label='Все категории',


    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            #'postcategory__pc_category':['exact']
            # поиск по названию
            #'p_name': ['icontains'],
            #'datefilter',
            # поиск по категории
            #'p_category__category': ['exact']
            #'p_create_date': [
            #    'date__gte',  # дата создания должна быть больше или равна указанной
            #],
        }