from django import forms
from django.db import models


from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


from wagtail.wagtailsnippets.models import register_snippet

import datetime
from wagtailmedia.blocks import AbstractMediaChooserBlock

            
class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(BlogIndexPage, self).get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        monthblogs = []
        currentdate = "%s-%s" % (datetime.datetime.now().year,
                                 datetime.datetime.now().month)
        if request.path != "dairy": 
            print(request.path)
            print(request.path[1:-1].split("/"))
            
        monthcal = {}
        monthdraw = {}
        for blog in blogpages:
            bdate = "%s-%s" % (blog.specific.date.year,
                               blog.specific.date.month)
            if bdate == currentdate: 
                monthblogs.append(blog)
                monthcal[blog.specific.date.day] = blog
                monthdraw[blog.specific.date.day] = (blog.specific.date.isocalendar()[1],
                                                     blog.specific.date.isocalendar()[2])
        context['blogpages'] = monthblogs
        context['count'] = len(monthblogs)
        context['date'] = datetime.datetime.now()
        context['monthcal'] = monthcal
        context['monthdraw'] = monthdraw
        print(monthdraw)

        return context
    
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', related_name='tagged_items')


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)



    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
#            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
#        InlinePanel('media',label="Videos"),
    ]


class BlogMediaBlock(AbstractMediaChooserBlock):
    page = ParentalKey(BlogPage, related_name='media')
    
    def render_basic(self, value, context=None):
        if not value:
            return ''

        if value.type == 'video':
            player_code = '''
            <div>
                <video width="320" height="240" controls>
                    <source src="{0}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            </div>
            '''
        else:
            player_code = '''
            <div>
                <audio controls>
                    <source src="{0}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            </div>
            '''
        return format_html(player_code, value.file.url)
    
class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
    
class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super(BlogTagIndexPage, self).get_context(request)
        context['blogpages'] = blogpages
        return context
    
@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'