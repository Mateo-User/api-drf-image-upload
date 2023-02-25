from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'images/{0}/'.format(filename)

class Plan(models.Model):
    name = models.CharField(max_length=100)
    thumbnail_sizes = models.CharField(max_length=255, help_text="Comma-separated list of thumbnail sizes, in pixels.")
    original_file_link = models.BooleanField(default=False, help_text="Include link to the original file.")
    expiring_link = models.BooleanField(default=False, help_text="Enable generation of expiring links.")
    expiring_link_duration = models.PositiveIntegerField(default=0, help_text="Duration of the expiring link, in seconds.")

class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='images')

class ImageSerializer(serializers.ModelSerializer):
    thumbnail_200px = serializers.SerializerMethodField()
    thumbnail_400px = serializers.SerializerMethodField()
    original_image = serializers.SerializerMethodField()
    expiring_link = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'user', 'image', 'thumbnail_200px', 'thumbnail_400px', 'original_image', 'expiring_link']

    def get_thumbnail_200px(self, obj):
        if obj.plan and '200' in obj.plan.thumbnail_sizes:
            return obj.image.url + '?height=200'
        return None

    def get_thumbnail_400px(self, obj):
        if obj.plan and '400' in obj.plan.thumbnail_sizes:
            return obj.image.url + '?height=400'
        return None

    def get_original_image(self, obj):
        if obj.plan and obj.plan.original_file_link:
            return obj.image.url
        return None

    def get_expiring_link(self, obj):
        if obj.plan and obj.plan.expiring_link:
            duration = obj.plan.expiring_link_duration
            return reverse('image_expiring_link', kwargs={'pk': obj.pk, 'duration': duration}, request=self.context['request'])
        return None




