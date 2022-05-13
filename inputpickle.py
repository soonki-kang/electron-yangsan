import pickle
from myvar          import      myVar   as  mv


class inputPickle():
  
  def read_input(self):
    try:
      with open("asparam.pk", "rb") as file:
        mv.USER_ID, mv.USER_PASSWORD, mv.USER_MEMBER = pickle.load(file) 
    except   Exception as e:
        mv.USER_ID, mv.USER_PASSWORD, mv.USER_MEMBER = "",  "", False
    return 
  
    
  def save_input(self):
        myparam = (mv.USER_ID, mv.USER_PASSWORD, mv.USER_MEMBER)
        try:
          with open("asparam.pk", "wb") as file:
            pickle.dump(myparam, file) 
        except   Exception as e:
            pass
        return
