from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        form_count = len([f for f in self.forms if f.cleaned_data])
        if form_count < 1:
            raise ValidationError('Укажите хотя бы один раздел')
        count_main = 0
        for form in self.forms:
            try:
                is_main = form.cleaned_data['is_main']
                is_del = form.cleaned_data['DELETE']
                print(is_main, is_del)
            except:
                raise ValidationError('Заполните пустующий раздел')    
            if is_main == True:
                count_main += 1
            if is_main == True and is_del == True:
                raise ValidationError('Нельзя удалять основной раздел')
        if count_main>1:
            raise ValidationError('Основным может быть только один раздел')
        if count_main<1:
            raise ValidationError('Укажите основной раздел')
        return super().clean() 


class RelationshipInline(admin.TabularInline):
    model = Scope
    extra = 0
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'published_at', 'image',]
    list_filter = ['title']
    inlines = [RelationshipInline]


@admin.register(Tag)
class ArticleAdmin(admin.ModelAdmin):
    pass