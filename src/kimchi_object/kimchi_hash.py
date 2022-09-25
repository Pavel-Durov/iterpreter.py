

def kimchi_hash(obj):
  return 1
  h = ""
  if type(obj) is int:
      return int(obj)
  else:
    for s in str(obj):
        # h = ord(str(s)) + (h << 6) + (h << 16) - h
        h = ord(str(s))
  # print("@@ hash of " + str(obj) + " is " + str(h))
  # print("@@ hash of " + str(obj) + " is " + str(hash(obj)))
  return int(h)
  # return hash(obj)