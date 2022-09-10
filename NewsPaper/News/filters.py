from django_filters import FilterSet, ModelMultipleChoiceFilter
from .models import Post, Category

#Post.objects.filter(postcategory_category=)

class NewsFilter(FilterSet):
    category = ModelMultipleChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Категории (отдельно)',
            )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {

            'title': ['icontains'],

            'created': ['date__gt'],
        }
