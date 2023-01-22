from django.core.mail import send_mail
from mysite.settings import EMAIL_FROM

def send_hello(request):
# 用户注册完成后自动发送
# 此视图只在内部使用，不需要为其配置路由
    recipient = request.user

    send_mail(
        "欢迎加入网站",
        # 主题
        "我们期待与您共同成长",
        # 内容
        EMAIL_FROM,
        # 发件人
        [recipient.email],
        # 收件人列表
        fail_silently = False,
        # 如果发生错误，则会抛出异常
    )

def send_auth_code(request):
    pass