from django.contrib import admin

@admin.action(description='Recover selected items')
def recover_selected(modeladmin, request, queryset):
    # queryset.recover() # if not caring about signals
    for item in queryset:
        item.recover()

class BaseModelAdmin(admin.ModelAdmin):
    actions = [recover_selected]

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.everything()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
