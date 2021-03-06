from django.conf import settings
from django.db import models

from embed_video.fields import EmbedVideoField
from polymorphic.models import PolymorphicModel
from taggit.managers import TaggableManager

from rlp.projects.models import Project


class Document(PolymorphicModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project)
    date_added = models.DateTimeField(auto_now_add=True, db_index=True)
    date_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    tags = TaggableManager()

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('projects:document_detail', kwargs={
            'pk': self.project.pk,
            'slug': self.project.slug,
            'doc_pk': self.pk
        })

    def get_edit_url(self):
        from django.core.urlresolvers import reverse
        return reverse('projects:document_edit', kwargs={
            'pk': self.project.pk,
            'slug': self.project.slug,
            'doc_pk': self.pk,
            'doc_type': self.polymorphic_ctype.model,
        })

    def get_delete_url(self):
        from django.core.urlresolvers import reverse
        return reverse('projects:document_delete', kwargs={
            'pk': self.project.pk,
            'slug': self.project.slug,
            'doc_pk': self.pk
        })

    @property
    def display_type(self):
        if hasattr(self, 'upload'):
            if self.upload.path.endswith(('.doc', '.docx')):
                return "Document (Word)"
            elif self.upload.path.endswith(('.pdf',)):
                return "Document (pdf)"
            elif self.upload.path.endswith(('.ppt', '.pptx')):
                return "Slideshow (ppt)"
            elif self.upload.path.endswith(('.key',)):
                return "Slideshow (Keynote)"
            elif self.upload.path.endswith(('.txt',)):
                return "Document (txt)"
            elif self.upload.path.endswith(('.rtf',)):
                return "Document (rtf)"
            elif self.upload.path.endswith(('.xls', '.xlsx')):
                return "Spreadsheet (xls)"
            elif self.upload.path.endswith(('.csv',)):
                return "Spreadsheet (csv)"
            elif self.upload.path.endswith(('.jpg', '.jpeg')):
                return "Image (jpg)"
            elif self.upload.path.endswith(('.png',)):
                return "Image (png)"
            elif self.upload.path.endswith(('.gif',)):
                return "Image (gif)"
            elif self.upload.path.endswith(('.avi',)):
                return "Video (avi)"
            elif self.upload.path.endswith(('.mov',)):
                return "Video (mov)"
            elif self.upload.path.endswith(('.zip',)):
                return "Compressed File (zip)"
            return 'Document'


class File(Document):
    upload = models.FileField(upload_to="docs/%Y/%m/%d")
    working_document = models.BooleanField(default=False,
                                           verbose_name="Core Project Document (will appear as top-listed document)")


class Image(Document):
    upload = models.ImageField(upload_to="docs/images/%Y/%m/%d", max_length=255,
                             height_field='height', width_field='width')
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()


class Video(Document):
    share_link = EmbedVideoField(help_text='Should be a Youtube or Vimeo share link e.g. https://youtu.be/xyz123')

    @property
    def display_type(self):
        return 'Video'


class Link(Document):
    url = models.URLField()

    @property
    def display_type(self):
        return 'Link'
