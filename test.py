


def validate_num(func):
  def wrapper(a,b):
    if a>0 and b>0:
      return func(a,b)
    else:
      print("Number should be gereater than zero")
  return wrapper
      
@validate_num
def sum(a,b):
  print(a+b)
    
sum(4,-7)

