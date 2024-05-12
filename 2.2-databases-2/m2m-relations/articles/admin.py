from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        number_main_sections = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main', False):
                number_main_sections += 1
        if number_main_sections != 1:
            raise ValidationError('У каждой статьи должен быть обязательно'
                                  ' один (и только один) ОСНОВНОЙ раздел!')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    inlines = [ScopeInline,]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
