from django.db import models
from entities.models import Agent

class Commission(models.Model):
	total_commission_lifetime = models.PositiveIntegerField(blank=True, null=True)
	total_commission_today = models.PositiveIntegerField(blank=True, null=True)
	agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, to_field="agent_cid")
	is_delete = models.BooleanField(default=False)

	def __str__(self):
		return self.agent.agent_name