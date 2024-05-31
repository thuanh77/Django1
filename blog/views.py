from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, FormView

from .models import Post, Result
from .forms import RegisterUserForm, LoginUserForm


class BlogList(ListView):
    paginate_by = 3
    model = Post
    template_name = 'home.html'
    ordering = ['-id']

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reg_form'] = RegisterUserForm()
        context['login_form'] = LoginUserForm()
        return context

class BlogDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'


class AboutPageView(TemplateView):
    template_name = 'about.html'


class RegisterUserView(FormView):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']

            # Создаем пользователя
            user = User.objects.create_user(username=username, email=email, password=password)

            # Авторизуем пользователя
            user = authenticate(username=username, password=password)
            login(request, user)

            # Перенаправляем пользователя на нужную страницу
            return redirect('home')
        return render(request, 'register.html', {'form': form})


class LoginUser(View):
    def get(self, request):
        form1 = LoginUserForm()
        return render(request, 'login.html', {'form': form1})

    def post(self, request):
        form1 = LoginUserForm(data=request.POST)
        if form1.is_valid():
            user = form1.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'form': form1})

def logout_user(request):
    logout(request)
    return redirect('home')


class PageView(TemplateView):
    template_name = 'page.html'


class TrainingView(TemplateView):
    template_name = 'page.html'

    def post(self, request):
        metrics = training_rgr()
        sms_rgr = "Training model regression complete!!!"
        sms_bst = "Training model gradient regression complete!!!"
        sms_rnn = "Training model recurrent neural network complete!!!"
        text_out = [sms_rgr, sms_bst, sms_rnn]
        return render(request, "page.html", {'text_out': text_out, 'metrics': metrics})


class TestingView(TemplateView):
    template_name = 'page.html'

    def post(self, request):
        table_name = 'datatesting'
        x_test, y_test = read_data(table_name)
        poly_features = preprocessing(x_test)

        model_rgr = pickle.load(open("static/polymodel.pkl", "rb"))
        y_pred_rgr = model_rgr.predict(poly_features)  # the result of the prediction by using regression

        model_bst = pickle.load(open("static/gb_model.pkl", "rb"))
        y_pred_bst = model_bst.predict(poly_features)

        model_rnn = keras.models.load_model("static/rnn_model.h5")
        y_pred_rnn = model_rnn.predict(x_test).flatten()

        # save data to sql
        db_process(y_test, y_pred_rgr, y_pred_bst, y_pred_rnn)
        # message save data successfully
        mss = "# Save data successfully"
        return render(request, "page.html", {'mss': mss})

class ResultView(TemplateView):
    template_name = 'page.html'

    def post(self, request):
        results = Result.objects.all()  # the query all data in the table
        return render(request, "page.html", {'results': results})



