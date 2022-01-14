from django.db.models import Manager, QuerySet

"""
    UserQuerySet class inherits the Queryset from db.models.
    By this we can query different types of users stored in a single table or model called User
    Normally while Querying the objects of a model we use User.objects.all(). The problem with this is that
    here we have 3 types of users teachers, students and staffs. Using the Queryset we can separately query
    different types of users. 
"""
class UserQuerySet(QuerySet):
    
    def teachers(self):
        return self.filter(user_role='T')

    def students(self):
        return self.filter(user_role='S')

    def staffs(self):
        return self.filter(user_role='St')


"""
    The UserManager class inherits the models.Manager. 
    Here the default get_queryset() method is overridden and returns the UserQueryset class we defined 
    earlier. The benfit of this method is that we donot have to create a separate manager object to each 
    type of user i.e teachers = Teachermanager(), students = StudentManager() and so on. Instead what it
    does is that we define only one Manager class and call the specific methods for querying different 
    user types.
    The teachers() method here returns the queryset which basically calls the teachers() method from the
    UserQueryset class such that users with only the user_role = 'T' is returned.
    Similar is the case with other user types methods.
"""

class UserManager(Manager):

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)
        # Overrides the get_queryset() of the UserQueryset class.
        # self.model means the current model we are working with in the instance.
        # using=self._db means use the current table in the database 

    def teachers(self):
        return self.get_queryset().teachers()

    def students(self):
        return self.get_queryset().students()

    def staffs(self):
        return self.get_queryset().staffs()
    