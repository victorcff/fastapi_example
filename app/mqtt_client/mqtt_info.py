def is_float(value):
  if value is None:
    return False
  try:
    float(value)
    return True
  except:
    return False

class Mqtt_Info:
  weight: float = 0
  mac_address: str = ""
  
  def get_weight(self):
    return self.weight
  
  def set_weight(self, weight: str):
    if is_float(weight):
      self.weight = float(weight)
      return True
    else:
      return False
    
  def set_mac_address(self, mac_address: str):
    self.mac_address = mac_address
  
  def get_mac_address(self):
    return self.mac_address
