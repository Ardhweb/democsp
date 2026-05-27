from django.db import models

# Create your models h
# Create your models here.
class Agent(models.Model):
	agent_cid = models.PositiveIntegerField(blank=False,null=False, unique=True)
	agent_name = models.CharField(max_length=155, blank=True,null=True)
	agent_activation_date = models.CharField(max_length=50, blank=True, null=True, editable=False)


	def __str__(self):
		return self.agent_name