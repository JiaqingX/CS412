from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from .forms import VoterFilterForm
from plotly.offline import plot
import plotly.graph_objs as go

class VoterListView(ListView):
    model = Voter
    paginate_by = 100
    template_name = 'voter_analytics/voter_list.html'

    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():

            party = form.cleaned_data.get('party_affiliation')
            if party:
                queryset = queryset.filter(party_affiliation=party)

            score = form.cleaned_data.get('voter_score')
            if score is not None:
                queryset = queryset.filter(voter_score=score)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'

def voter_graphs(request):
    voters = Voter.objects.all()
    birth_years = [voter.dob.year for voter in voters]

    birth_year_counts = {}
    for year in birth_years:
        birth_year_counts[year] = birth_year_counts.get(year, 0) + 1

    data = [go.Bar(x=list(birth_year_counts.keys()), y=list(birth_year_counts.values()))]
    fig = go.Figure(data=data)
    fig.update_layout(title="Distribution of Voters by Birth Year",
                      xaxis_title="Birth Year",
                      yaxis_title="Number of Voters")

    plot_div = plot(fig, output_type='div')
    return render(request, 'voter_analytics/graphs.html', {'plot_div': plot_div})
