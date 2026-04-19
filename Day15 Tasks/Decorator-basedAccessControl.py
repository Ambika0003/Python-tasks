users = {
    "ram": "admin",
    "sita": "user",
    "john": "guest"
}
def check_role(required_role):
    def decorator(func):
        def wrapper(username, *args, **kwargs):
            role = users.get(username)
 
            if role == required_role:
                return func(username, *args, **kwargs)
            else:
                print("Access Denied for", username)
        return wrapper
    return decorator
@check_role("admin")
def delete_data(username):
    print(username, "deleted the data")
 
@check_role("user")
def view_data(username):
    print(username, "viewed the data")
 
 
delete_data("ram")    
delete_data("sita")  
 
view_data("sita")    
view_data("john")    