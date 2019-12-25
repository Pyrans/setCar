from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View

from .models import *
import datetime, time


def get_time_second(input_time):
    return time.mktime(((datetime.datetime.strptime(input_time, "%Y-%m-%d %H:%M")).timetuple()))


def get_time_mysql(mysql_time):
    return time.mktime(time.strptime(mysql_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'))


def index(request):
    plans = PlanForCar.objects.filter(p_status=True)
    if plans:
        for plan in plans:
            now = get_time_mysql(datetime.datetime.now())
            p_time_end = get_time_mysql(plan.p_time_end)
            if int(p_time_end) < int(now):
                plan.p_status = False
                plan.save()
        plans = PlanForCar.objects.filter(p_status=True).order_by('p_time_begin')
    else:
        return HttpResponseRedirect('/bycar/addplan')
    data = {
        'title': '首页',
        'plans': plans
    }
    return render(request, 'planList.html', data)


class AddPlanAPI(View):

    def get(self, request):
        cars = CarMessage.objects.filter(c_status=True)
        data = {
            'title': '增加用车计划',
            'cars': cars
        }
        return render(request, 'addPlan.html', data)

    def post(self, request):
        person = request.POST.get('person')
        todo = request.POST.get('todo')
        begintime = request.POST.get('begintime').replace('T', ' ')
        endtime = request.POST.get('endtime')
        car = request.POST.get('car')
        plans = PlanForCar.objects.filter(p_status=True)
        for plan in plans:
            if get_time_second(begintime) < get_time_mysql(plan.p_time_end) and get_time_second(begintime) >get_time_mysql(plan.p_time_begin):
                return HttpResponse('<a href="http://yun.pyrans.xyz:8000/bycar/addplan" target="_self">时间冲突，点我返回</a>')
            elif get_time_mysql(datetime.datetime.now()) > get_time_second(begintime):
                return HttpResponse('<a href="http://yun.pyrans.xyz:8000/bycar/addplan" target="_self">使用日期须在本次时间之后，点我返回</a>')
            else:
                pass
        PlanForCar.objects.create(
            p_name=person,
            p_do=todo,
            p_time_begin=begintime,
            p_time_end=endtime,
            p_car=car
        )
        return HttpResponseRedirect('/bycar/index/')


class AddCarAPI(View):

    def get(self, request):
        data = {
            'title': '增加车辆信息'
        }
        return render(request, 'addCar.html', data)

    def post(self, request):
        name = request.POST.get('name')
        number = request.POST.get('number')
        CarMessage.objects.create(
            c_name=name,
            c_number=number
        )
        return HttpResponseRedirect('/bycar/index/')
