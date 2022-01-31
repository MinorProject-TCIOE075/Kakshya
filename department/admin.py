from django.contrib import admin
from department.models import Department, Program


class DepartmentAdmin(admin.ModelAdmin):
    model = Department
    list_display = ('dep_name', 'dep_code')
    list_filter = ()

    search_fields = ('dep_name', )
    ordering = ('created_on', )


class ProgramAdmin(admin.ModelAdmin):
    model = Program
    list_display = ('pr_name', 'pr_code', 'created_on')
    list_filter = ('pr_code',)

    search_fields = ('pr_code', )
    ordering = ('pr_code', 'created_on')


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Program, ProgramAdmin)
