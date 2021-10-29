#!/usr/bin/python37all

import cgi
import json

data = cgi.FieldStorage()
if("new" in data):
  angle = data.getvalue('angle')
else:
  angle = -1

data = {"angle":angle}
with open('angle.txt', 'w') as f:
  json.dump(data,f)

print('Content-type: text/html\n\n')
print('<html>')
print('<form action="/cgi-bin/stepper_control.cgi" method="POST">')
print('Input Angle:<br>')
print('<input type="text" name="angle"><br>')
print('<input type="submit" value="Submit" name="new">')
print('<input type="submit" value="Zero Angle" name = "zero">')
print('</form>')
print('Angle = %s' %r1)
print('</html>')








