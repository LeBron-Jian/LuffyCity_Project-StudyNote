from django.shortcuts import render, HttpResponse

# Create your views here.
from django import forms
from app01 import models
from django.forms import formset_factory


class MultiPermissionForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '------------')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '------------')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    # 重新构造初始化函数
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')


class MultiUpdatePermissionForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '------------')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '------------')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
    )

    # 重新构造初始化函数
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')


def multi_add(request):
    '''
    批量添加
    :param request:
    :return:
    '''
    formset_class = formset_factory(MultiUpdatePermissionForm, extra=2)

    if request.method == 'GET':
        formset = formset_class()
        return render(request, 'multi_add.html', {'formset': formset})

    formset = formset_class(data=request.POST)
    if formset.is_valid():
        flag = True
        # 如果写一个，报错，如果一个都不写就可以提交成功
        # print(formset.cleaned_data)
        # 如果formset中没有错误信息，将用户提交的数据获取到
        post_row_list = formset.cleaned_data
        for i in range(0, formset.total_form_count()):
            # J检查formset中没有错误信息，则将用户提交到的数据获取到
            row = post_row_list[i]  # 这就算每一行的数据
            # formset.errors[i]
            # 如果提交空的数据，我们给数据库不添加，让他直接过
            if not row:
                continue
            try:
                obj = models.Permission(**row)
                # 检查当前对象在数据库是否存在唯一的异常
                obj.validate_unique()
                obj.save()
            except Exception as e:
                # 如果捕获到异常，我们需要将错误信息放在那里呢？

                formset.errors[i].update(e)
                flag = False
        # for row in formset.cleaned_data:
        # models.Permission.objects.create(**row)
        # obj = models.Permission(**row)
        # obj.save()
        # 如何捕获异常信息，在这里报错，不让在页面报错
        # try:
        #     obj = models.Permission(**row)
        #     # 检查当前对象在数据库是否存在唯一的异常
        #     obj.validate_unique()
        #     obj.save()
        # except Exception as e:
        #     # 如果捕获到异常，我们需要将错误信息放在那里呢？
        #     pass

        if flag:
            return HttpResponse("提交成功")
        else:
            return render(request, 'multi_add.html', {'formset': formset})
    return render(request, 'multi_add.html', {'formset': formset})


def multi_edit(request):
    '''
    批量编辑，我们希望有些有默认值
    :param request:
    :return:
    '''
    # 当我们默认不写的时候，表格为1个，如果我们添加了表格，不想让写，则让extra=0即可
    formset_class = formset_factory(MultiPermissionForm, extra=0)
    if request.method == 'GET':
        #
        formset = formset_class(
            # initial=[
            #     {'id': 1, 'title': 'x1', 'url': 'xxx', 'name': 123},
            #     {'id': 2, 'title': 'x2', 'url': 'ooo', 'name': 1234}])

            # 如果要放数据库里
            initial=models.Permission.objects.all().values(
                'id', 'title', 'name', 'url', 'menu_id', 'pid_id'))
        return render(request, 'multi_edit.html', {'formset': formset})

    formset = formset_class(data=request.POST)
    if formset.is_valid():
        # 检查formset中没有错误信息，则将用户提交的数据获取到
        post_row_list = formset.cleaned_data
        flag = True
        for i in range(0, formset.total_form_count()):
            row = post_row_list[i]
            if not row:
                continue
            # print(row)  # 提交的是页面的数据
            permission_id = row.pop('id')
            try:
                permission_object = models.Permission.objects.filter(id=permission_id).first()
                # permission_object.title = row['title']
                # permission_object.url = row['url']
                # permission_object.menu_id = row['menu_id']
                # permission_object.pid_id = row['pid_id']

                # 可以修改，这里使用反射
                for key,value in row.items():
                    setattr(permission_object, key, value)
                permission_object.validate_unique()
                permission_object.save()
            except Exception as e:
                formset.errors[i].update(e)
                flag = False
            # models.Permission.objects.filter(id=permission_id).update(**row)
        if not flag:
            return HttpResponse("提交成功")
        else:
            return render(request, 'multi_edit.html', {'formset': formset})
    return render(request, 'multi_edit.html', {'formset': formset})
