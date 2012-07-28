# -*- coding:utf-8 -*-

from kay.utils import forms

class SitemapForm(forms.Form):
    article_id = forms.LineSeparated(forms.TextField(),required=True,widget=forms.Textarea)
    mode=forms.ChoiceField(choices=[u'追加', u'更新'])

