
from django.urls import reverse
from django.db import models
from graphapp import db

# Create your models here.
class NodeHandle(models.Model):
    handle_id = models.CharField(max_length=64, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return 'NodeHandle for node %d' % self.node()['handle_id']
    
    """ def create(self):
        new_handle_id=str(uuid.uuid4())
        return db.create_node(new_handle_id, self.name, self.description, self.__class__.__name__)
        return True
 """
    def node(self):
        return db.get_node(self.handle_id, self.__class__.__name__)

    def delete(self, **kwargs):
        """
                Delete that node handle and the handles node.
                """
        db.delete_node(self.handle_id, self.__class__.__name__)
        super(NodeHandle, self).delete()
        return True

    delete.alters_data = True

class Person(NodeHandle):

    def __str__(self):
        return self.name

    def _name(self):
        try:
            return self.node().properties.get('name', 'Missing name')
        except AttributeError:
            return 'Missing node?'
    name = property(_name)
    

    description = models.CharField(max_length=64, editable=True) 
    name = models.CharField(max_length=64, editable=True) 
    

    def get_absolute_url(self):
        return reverse('person-detail', args=[str(self.id)])

