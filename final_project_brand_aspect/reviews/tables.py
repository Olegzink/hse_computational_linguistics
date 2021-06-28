import django_tables2 as tables
from django_tables2.export.views import ExportMixin
from .models import Reviews
import itertools

class ReviewsAll(tables.Table):
    # export_formats = ['csv',]

    counter = tables.Column(verbose_name= '№', empty_values=(), orderable=False, attrs={'td': {'class': 'brand_name'}})
    brand_name = tables.Column()
    review_text = tables.TemplateColumn('<a href="/reviews/{{record.review_id}}"> {{record.review_text}} </a>  ')
    overall_sentiment = tables.TemplateColumn("""

        {% if record.overall_sentiment == "pos" %}
            <div class='badge badge-success-table'>positive</div> 
        {% else %}
            <div class='badge badge-danger-table'>negative</div>      
        {% endif %}  

        """, attrs=dict(cell={'class': 'result'}), verbose_name="Overall sentiment")

    # making column with row counter
    def render_counter(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(start=1))
        return next(self.row_counter)

    class Meta:
        model = Reviews
        fields = ('counter', 'brand_name', 'review_text', 'review_id', 'overall_sentiment', 'timestamp')
        template_name = 'django_tables2/bootstrap.html'
