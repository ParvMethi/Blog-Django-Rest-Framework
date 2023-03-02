from rest_framework import serializers

from home.models import Blog

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ['created_at', 'updated_at']
        # fields = '__all__'