import logging

from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from sign_in.models import LoginValue


from sign_in.models import LoginValue, Cards
import urllib.request
from random import randint
from django.contrib.auth import logout
from django.contrib import sessions

def index_sign_up(request):
    return render(request, 'sign_in/sign_up_page.html')


def forgot_pass(request):
    return render(request, 'sign_in/forgot_pass_page.html')


def personal_cabinet(request):
    return render(request, 'sign_in/personal_cabinet.html')


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
        # urllib.request.urlopen(mobizon_link)
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
    if request.method == 'POST':
        name = request.POST.get('owner_name')
        month = request.POST.get('month')
        year = request.POST.get('year')
        cvv = request.POST.get('cvv')
        cardNumber = request.POST.get('cardNumber')
        toTrans = request.POST.get('card_number_to_trans')
        money = int(request.POST.get('amount_of_money'))
    i, n, b = 0, 0, 0
    f = open('text.txt', 'w')
    while i < len(all_cards):
        if all_cards[i].number == cardNumber:
            n = i
            # f.write(str(n))
            break
        i = i + 1
    i = 0
    while i < len(all_cards):
        if all_cards[i].number == toTrans:
            b = i
            # f.write(str(b))
            break
        i = i + 1
    # f.write(money)
    # f.close()
    i = 0
    all_cards[b].balance = int(all_cards[b].balance) + money
    all_cards[n].balance = int(all_cards[n].balance) - money
    all_cards[b].save()
    all_cards[n].save()
    return render(request, 'home/homePage.html')


def transfers_confirm(request):
    all_cards = Cards.objects.all()
    f = open('text.txt')
    b = int(f.read(1))
    n = int(f.read(2))
    money = int(f.read(3))
    all_cards[b].balance = all_cards[b].balance + money
    all_cards[n].balance = all_cards[n].balance - money
    all_cards[b].save()
    all_cards[n].save()
    return HttpResponse("Successful")


def add_user(request):
    all_users = LoginValue.objects.all()

    if request.method == 'POST':
        login1 = request.POST.get('login')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        phone1 = request.POST.get('phone')
        iin = request.POST.get('iin')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        temp = 0
        for i in all_users:
            if i.login == login1:
                temp = 1
            if i.phone_number == phone1:
                temp = 2
            print(i)
        if pass1 != pass2:
            return HttpResponse("Password is not similar")
        else:
            if temp == 0:
                if len(phone1) == 11:
                    new_user = LoginValue.objects.create(login=login1,
                                                         phone_number=phone1,
                                                         iin=iin,
                                                         name=name,
                                                         surname=surname,
                                                         is_staff=False,
                                                         is_active=False)
                    # В чем трабла
                    new_user.set_password(pass1)
                    new_user.save()
                    return render(request, 'home/homePage.html')
                else:
                    return HttpResponse("INVALID NUMBER OF PHONE")

            elif temp == 2:
                temp = 0
                return HttpResponse("This phone has been already used")
            else:
                temp = 0
                return HttpResponse("This login has been already used")


def login_user(request):
    all_users = LoginValue.objects.all()
    login1 = ''
    pass1 = ''
    controller = 0
    a1 = {}
    session_key = 0
    request.session.set_expiry(10)
    if request.method == 'POST':
        login1 = request.POST.get('login')
        pass1 = request.POST.get('pass')
    try:
        lenth = len(all_users)
        for i in range(lenth):
            if all_users[i].login == login1 and all_users[i].check_password(pass1):
                request.session[0] = all_users[i].sys_id
                a1 = {'user': all_users[i]}
                all_users[i].is_active = True
                all_users[i].save()
                controller = 1
                request.session['user_id'] = all_users[i].id
                request.session.set_expiry(300)

    except LoginValue.DoesNotExist:
        logging.getLogger("error_logger").error("user with login %s does not exists " % login)
        return None
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))
        return None
    if controller == 1:
        return render(request, 'home/homePage.html', context=a1)
    else:
        return HttpResponse('Your login or password is incorrect')


def get_user(self, user_id):
    try:
        user = LoginValue.objects.get(sys_id=user_id)
        if user.is_active:
            return user
        return None
    except LoginValue.DoesNotExist:
        logging.getLogger("error_logger").error("user with %(user_id)d not found")
        return None
