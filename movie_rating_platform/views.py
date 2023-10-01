from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic
from django.views.decorators.cache import cache_page

from movie_rating_platform.forms import MovieSearchForm, VisitorCreationForm, VisitorSearchForm, VisitorUpdateForm, \
    CreateOrUpdateRatingForm
from movie_rating_platform.models import Movie, Rating, Genre, Visitor


def index(request: HttpRequest) -> HttpResponse:
    context = {
        "num_movies": Movie.objects.count(),
        "num_ratings": Rating.objects.count(),
        "num_genres": Genre.objects.count(),
        "num_users": get_user_model().objects.count()
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


class VisitorListView(generic.ListView):
    model = Visitor
    paginate_by = 5
    queryset = Visitor.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VisitorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = VisitorSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        form = VisitorSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return self.queryset


class VisitorDetailView(generic.DetailView):
    model = Visitor
    queryset = Visitor.objects.all().prefetch_related("wishlist")


class VisitorCreateView(generic.CreateView):
    model = Visitor
    success_url = reverse_lazy("movie_rating:visitor-list")
    form_class = VisitorCreationForm


class VisitorUpdateView(generic.UpdateView):
    model = Visitor
    form_class = VisitorUpdateForm
    success_url = reverse_lazy("movie_rating:visitor-list")


class VisitorDeleteView(generic.DeleteView):
    model = Visitor
    success_url = reverse_lazy("movie_rating:visitor-list")


def movie_detail_view(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    genres = movie.genres.all()
    max_value = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    movie.ratings.select_related("sender")
    context = {"movie": movie, "genres": genres, "max_value": max_value}
    return render(request, "movie_rating_platform/movie_detail.html", context=context)


def create_rating_view(request, pk):
    if request.method == 'POST':
        form = CreateOrUpdateRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.sender = request.user
            rating.create_time = timezone.now()
            rating.movie = Movie.objects.get(pk=pk)
            rating.save()
            return redirect('movie_rating:movie-detail', pk=pk)
    else:
        form = CreateOrUpdateRatingForm
    return render(request, "movie_rating_platform/rating_form.html", context={'form': form, "pk": pk})


class RatingUpdateView(generic.UpdateView):
    model = Rating
    form_class = CreateOrUpdateRatingForm
    success_url = reverse_lazy("movie_rating:movie-detail")


class RatingDeleteView(generic.DeleteView):
    model = Rating
    success_url = reverse_lazy("movie_rating:movie-detail", )


def toggle_assign_to_movie(request, pk):
    visitor = Visitor.objects.get(id=request.user.id)
    if (
        Movie.objects.get(id=pk) in visitor.wishlist.all()
    ):
        visitor.wishlist.remove(pk)
    else:
        visitor.wishlist.add(pk)
    return HttpResponseRedirect(reverse("movie_rating:movie-detail", args=[pk]))
