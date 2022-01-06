from django.contrib import admin
from .models import Platform, Market, OnePairArbitrage


@admin.register(Platform, Market, OnePairArbitrage)
class CustomAdmin(admin.ModelAdmin ):
	pass