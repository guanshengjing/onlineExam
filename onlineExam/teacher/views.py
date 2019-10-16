from django.shortcuts import render
from teacher import models
from django.http import HttpResponse


def get_student_score():
    import pymysql
    try:
        conn39 = pymysql.connect(**{"host": "176.17.111.39",
                                    "database": "exam",
                                    "user": "root",
                                    "passwd": "123456",
                                    "charset": "utf8"})
        cur39 = conn39.cursor()
        cur39.execute(
            "SELECT student.name name,grade.subject subject,grade.grade grade FROM "
            "student,grade WHERE student.id = grade.sid_id")
        return cur39.fetchall()
    except:
        return None


def teacherLogin(request):
    if request.method == 'POST':
        info_dict = request.POST
        username = info_dict['username']
        password = info_dict['password']
        # user_type = info_dict['user_type']
        code = info_dict['code']
        # 获取验证码并且不区分大小写
        # 教师登录
        # if code.upper() == request.session['code'].upper():
        if code.upper() != request.session['code'].upper():
            try:
                grade = get_student_score()
                teacher = models.Teacher.objects.get(id=username)
                log = getOperate()
                # print(teacher)
                if password == teacher.password:  # 登录成功
                    return render(request, 'teacherLogin.html', {'teacher': teacher, 'grade': grade, 'log': log})
                return HttpResponse('密码不正确')
            except:
                return HttpResponse('用户名不正确')
        return HttpResponse('验证码不正确')
    return HttpResponse('404Error')


def exam_manager(request):
    """
    考试管理
    :param request:
    :return:
    """
    # 读取试题编号
    subjects = models.Paper.objects.all()
    print(subjects)
    return render(request, 'guideTest.html', {'subjects': subjects})


# 将使用原生sql语句查到的结果由tuple类型转换为dictionary(字典)类型
def dictfetchall(cursor):
    """
        将游标返回的结果保存到一个字典对象中
    """
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


# 查看学生日志
def getOperate():
    from django.db import connection
    cursor = connection.cursor()
    sql = "select log.luser,student.id,student.major,log.operate,log.ldate " \
          "from log inner join student on log.luser = student.name"
    cursor.execute(sql)
    # 将查找的数据转成字典[{},{}]
    result = dictfetchall(cursor)
    return result


# 教师退出
def logOut(request):
    del request.session['username']
    return HttpResponse('index.html')
