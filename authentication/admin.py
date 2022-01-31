from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Teacher, Student, Address

# Custom User model 
User = get_user_model()

# For customizing the django admin panel
class StudentAdmin(admin.ModelAdmin):
    model = Student

    # displays a table with following headers and the objects
    list_display = ('get_user', 'roll_number', 'faculty', 'year_joined')

    # For filtering the admin site. Filters the query results on the basis of faculty & joined year
    list_filter = ('faculty', 'year_joined')

    """
        The model Student inherits from the user model. So the username field cannot be directly
        accessed through the Student object. Therefore, a method is used to access the attributes 
        of the parent model .i.e User model
        The methods returns the username associated with the Student model via User model.
        
        Syntax: return <object>.<foreignKey_name>.<field_name>
    """
    def get_user(self, obj):
        return obj.user.username

    search_fields = ('faculty',)
    ordering = ('-year_joined', 'roll_number')



class TeacherAdmin(admin.ModelAdmin):
    model = Teacher
    list_display = ('user', 'designation', )
    list_filter = ('designation', )

    # def get_department(self, obj):
    #     if obj:
    #         return obj.departments.dep_name
    #     else:
    #         pass

    search_fields = ('year_joined', 'designation')
    ordering = ('-year_joined', )

class AddressInline(admin.StackedInline):
    model = Address

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [AddressInline]

# Register your models here.
# admin.site.register(User)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.site_header = 'Kakshya'