import pickle
from myvar          import      myVar   as  mv


class inputPickle():
  
  def read_input(self):
    try:
      with open("./ysparam.pk", "rb") as file:
        mv.USER_ID, mv.USER_PASSWORD = pickle.load(file) 
    except   Exception as e:
        mv.USER_ID, mv.USER_PASSWORD = "",  ""
    return 
  
    
  def save_input(self):
        myparam = (mv.USER_ID, mv.USER_PASSWORD)
        try:
          with open("./ysparam.pk", "wb") as file:
            pickle.dump(myparam, file) 
        except   Exception as e:
            pass
        return
