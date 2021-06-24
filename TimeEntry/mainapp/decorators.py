from django.shortcuts import redirect

def unauth_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated :
            return redirect('task')
        else:
            return view_func(request,*args,**kwargs)

    return wrapper_func

def auth_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated :
            return view_func(request,*args,**kwargs)
        else:
            return redirect('index')
        

    return wrapper_func