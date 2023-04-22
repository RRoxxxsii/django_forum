from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render

from main.models import Post


class DeleteEditMixin:
    def get(self, request, *args, **kwargs):
        user_id_from_request = request.user.id
        post_id = kwargs.get('pk')

        try:
            post = Post.objects.get(pk=post_id)
        except ObjectDoesNotExist:
            raise Http404

        title, text = post.title, post.text
        self.initial['title'] = title
        self.initial['text'] = text
        form = self.form_class(initial=self.initial)

        if user_id_from_request != post.author_id:                 # Prevents URL injection
            raise Http404

        return render(request, self.template_name, {"form": form})