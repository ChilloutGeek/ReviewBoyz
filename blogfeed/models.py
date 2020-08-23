from django.db import models

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index

from modelcluster.fields import ParentalKey
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        #Update context to include only published post, ordered by reverse
        context = super().get_context(request)
        blogpages  = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context 
      
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]



class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    content_panels = Page.content_panels +[
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

class BlogGalleryImages(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image',blank=True,null=True, on_delete=models.SET_NULL, related_name = '+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
    