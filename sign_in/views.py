import logging
import urllib
from random import randint
from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from sign_in.forms import RegisterForm
from sign_in.models import LoginValue, Cards
from django.contrib import messages


def index_sign_up(request):
    return render(request, 'sign_in/sign_up_page.html')


def forgot_pass(request):
    return render(request, 'sign_in/forgot_pass_page.html')


def personal_cabinet(request):
    return render(request, 'sign_in/personal_cabinet.html')


def change_pass_index(request):
    return render(request, 'sign_in/change_pass.html')


def recovery_code(request):
    all_users = LoginValue.objects.all()
    random_code = str(randint(100000, 999999))
    phone = ''
    if request.method == 'POST':
        phone = request.POST.get('phone')

    temp = 0
    for i in all_users:
        if i.phone_number == phone:
            temp = 1
    if temp == 1:
        mobizon = 'https://api.mobizon.kz/service/message/sendsmsmessage?recipient=' + phone + '&from&text=Your+recovery+code+is+' + random_code + '&apiKey=kz8e497f591b5d08f4a21f78bb8791f60e62118479e62d3954e7c6c2613efa3ca96d67'
        mobizon_link = mobizon
        urllib.request.urlopen(mobizon_link)
        f = open('recovery_data.txt', 'w')
        f.write(random_code + '\n' + phone)
        f.close()
        return render(request, 'sign_in/new_password.html')

    else:
        if phone[0] != '7' and phone[1] != 7 and len(phone) != 11:
            return HttpResponse(phone + "  Incorrect format")
        else:
            return HttpResponse(phone + "  This phone has not registered")


def new_pass(request):
    all_users = LoginValue.objects.all()
    r_code = ''
    pass1 = ''
    pass2 = ''
    f = open('C:/Users/User/Desktop/Study/1 simestr 2year/Python_Projects/Online_Banking/recovery_data.txt', 'r')
    ls = [line.strip() for line in f]
    f.close()
    random_code = ls[0]
    phone = ls[1]
    print(ls[0], ls[1])
    f = open('C:/Users/User/Desktop/Study/1 simestr 2year/Python_Projects/Online_Banking/recovery_data.txt', 'w')
    f.write(' ')
    f.close()
    if request.method == 'POST':
        r_code = request.POST.get('r_code')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
    if r_code == random_code:
        if pass1 == pass2:
            for i in all_users:
                if i.phone_number == phone:
                    i.set_password(pass1)
                    i.save()
                    return render(request, 'home/homePage.html')
        else:
            return HttpResponse("Passwords have no equals")
    else:
        return HttpResponse("Recovery code is wrong")


def transfers(request):
    all_cards = Cards.objects.all()
    a = request.session.get('user_id')
    user = LoginValue.objects.get(sys_id=a)
    a1 = {'user': user}
    for i in all_cards:
        if i.login == user.login:
            a1.update({'card': i})
    if request.method == 'POST':
        name = request.POST.get('owner_name')
        name_owner = request.POST.get('owner')
        cvv = request.POST.get('cvv')
        cardNumber = request.POST.get('cardNumber')
        toTrans = request.POST.get('card_number_to_trans')
        money = int(request.POST.get('amount_of_money'))
    i, n, b = 0, 0, 0
    f = open('text.txt', 'w')
    while i < len(all_cards):
        if all_cards[i].number == cardNumber:
            if all_cards[i].cvv == cvv:
                if all_cards[i].name == name:
                    n = i
                    break
        i = i + 1
    i = 0
    while i < len(all_cards):
        if all_cards[i].number == toTrans:
            if all_cards[i].name == name_owner:
                b = i
                break
        i = i + 1
    i = 0
    all_cards[b].balance = int(all_cards[b].balance) + money
    all_cards[n].balance = int(all_cards[n].balance) - money
    all_cards[b].save()
    all_cards[n].save()
    return render(request, 'home/homePage.html', context=a1)


def add_user(request):
    all_users = LoginValue.objects.all()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            login1 = form.cleaned_data.get('login')
            phone1 = form.cleaned_data.get('phone')
            iin = form.cleaned_data.get('iin')
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            pass1 = form.cleaned_data.get('pass1')
            pass2 = form.cleaned_data.get('pass2')
            if pass1 == pass2:
                temp = 0
                for i in all_users:
                    if i.login == login1:
                        temp = 1
                    if i.phone_number == phone1:
                        temp = 2
                if temp == 0:
                    new_user = LoginValue.objects.create(login=login1,
                                                         phone_number=phone1,
                                                         iin=iin,
                                                         name=name,
                                                         surname=surname,
                                                         is_staff=False,
                                                         is_active=False)
                    new_user.set_password(pass1)
                    new_user.save()
                    return render(request, 'home/homePage.html')
                elif temp == 2:
                    return HttpResponse("This phone has been already used")
                else:
                    return HttpResponse("This login has been already used")
            else:
                return HttpResponse("Password is not similar")
        else:
            return HttpResponse("Yor data is incorrect")


def login_user(request):
    all_users = LoginValue.objects.all()
    all_cards = Cards.objects.all()
    controller = 0
    a1 = {}
    if request.method == 'POST':
        login1 = request.POST.get('login1')
        pass1 = request.POST.get('pass1')
        lenth = len(all_users)
        for i in range(lenth):
            if all_users[i].login == login1 and all_users[i].check_password(pass1):
                # keys = request.session.keys()
                #                 # print(keys)
                #                 # if str(all_users[i].sys_id) in keys:
                #                 # print("vrode robit")
                #                 # return HttpResponse("This user already auth")
                #                 # else:
                a1 = {'user': all_users[i]}
                all_users[i].is_active = True
                all_users[i].save()
                controller = 1

                request.session['user_id'] = all_users[i].sys_id
                request.session.set_expiry(300)
                print(request.session)

                for i in all_cards:
                    if i.login == login1:
                        a1.update({'card': i})
    if controller == 1:
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            return render(request, 'home/homePage.html', context=a1)
        request.session.set_test_cookie()
        return render(request, 'home/homePage.html', context=a1)
    else:
        return HttpResponse('Your login or password is incorrect')


def logout1(request):
    try:
        request.session.flush()
        request.user = AnonymousUser()
    except KeyError:
        pass
    return HttpResponseRedirect('home/homePage.html')


def payments(request):
    all_cards = Cards.objects.all()
    a = request.session.get('user_id')
    user = LoginValue.objects.get(sys_id=a)
    a1 = {'user': user}
    for i in all_cards:
        if i.login == user.login:
            a1.update({'card': i})
    if request.method == 'POST':
        cardNumber = request.POST.get('cardNumber')
        money = int(request.POST.get('amount_of_money'))
    i, n, b = 0, 0, 0

    f = open('amount.txt', 'w')
    while i < len(all_cards):
        if all_cards[i].number == cardNumber:
            n = i
            # f.write(str(n))
            break
        i = i + 1
    i = 0

    all_cards[b].balance = int(all_cards[b].balance) + money
    all_cards[n].balance = int(all_cards[n].balance) - money
    all_cards[b].save()
    all_cards[n].save()
    return render(request, 'home/homePage.html', context=a1)


def get_user(request, user_id):
    try:
        user = LoginValue.objects.get(sys_id=user_id)
        if user.is_active:
            return user
        return None
    except LoginValue.DoesNotExist:
        logging.getLogger("error_logger").error("user with %(user_id)d not found")
        return None


def change_pass(request):
    all_users = LoginValue.objects.all()
    a = request.session.get('user_id')
    user = LoginValue.objects.get(sys_id=a)
    a1 = {'user': user}
    pass1 = ''
    pass2 = ''
    if request.method == 'POST':
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
    if pass1 == pass2:
        for i in all_users:
            if i.login == user.login:
                i.set_password(pass1)
                i.save()
        # for i in all_users:
        # i.save()
        return HttpResponseRedirect('home/homePage.html')
    else:
        return HttpResponse("Passwords have no equals")
