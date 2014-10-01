from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import View
from django.shortcuts import render_to_response, redirect, get_object_or_404

from models import Quiz, QuizUser, QuizGame
from forms import QuizForm
from core.ui import register_sidebar_block


class QuizView(View):
    def dispatch(self, request, *args, **kwargs):
        if QuizGame.disabled():
            return redirect('wouso.interface.views.homepage')

        profile = request.user.get_profile()
        self.quiz_user = profile.get_extension(QuizUser)
        self.quiz = get_object_or_404(Quiz, pk=kwargs['id'])

        Quiz.create('lesson_one', False)

        return super(QuizView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = QuizForm(self.quiz)
        return render_to_response('quiz/quiz.html',
                                  {'quiz': self.quiz, 'form': form},
                                  context_instance=RequestContext(request))


quiz = login_required(QuizView.as_view())


def sidebar_widget(context):
    user = context.get('user', None)
    if not user or not user.is_authenticated():
        return ''

    quiz_user = user.get_profile().get_extension(QuizUser)

    return render_to_string('quiz/sidebar.html',
                            {'quser': quiz_user,
                             'quiz': QuizGame,
                             'id': 'quiz'})


register_sidebar_block('quiz', sidebar_widget)
