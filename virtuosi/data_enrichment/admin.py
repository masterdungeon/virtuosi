from django.contrib import admin

from . models import Rules, RuleCondition, GenericTags


class RuleConditionInline(admin.TabularInline):
    model = RuleCondition


class RuleAdmin(admin.ModelAdmin):
    inlines = [
        RuleConditionInline,
    ]


class GenericTagsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Rules, RuleAdmin)
admin.site.register(GenericTags, GenericTagsAdmin)
