from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from movie_rating_platform.forms import MovieSearchForm
from movie_rating_platform.models import Movie, Rating, Genre


def index(request: HttpRequest):
    context = {
        "num_movies": Movie.objects.count(),
        "num_ratings": Rating.objects.count(),
        "num_genres": Genre.objects.count(),
        "num_visitors": get_user_model().objects.count()
    }
    return render(
        request,
        template_name="movie_rating_platform/index.html",
        context=context
    )


class MovieListView(generic.ListView):
    model = Movie
    paginate_by = 5
    queryset = Movie.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MovieListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = MovieSearchForm(
            initial={"title": title}
        )
        return context

    def get_queryset(self):
        form = MovieSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                title__icontains=form.cleaned_data["title"]
            )
        return self.queryset


class MovieDetailView(generic.DetailView):
    model = Movie
    queryset = Movie.objects.all().prefetch_related("genres")


class MovieCreateView(generic.CreateView):
    model = Movie
    fields = "__all__"
    success_url = reverse_lazy("movie_rating:movie-list")


class MovieUpdateView(generic.UpdateView):
    model = Movie
    fields = "__all__"
    success_url = reverse_lazy("movie_rating:movie-list")


class MovieDeleteView(generic.DeleteView):
    model = Movie
    success_url = reverse_lazy("movie_rating:movie-list")

