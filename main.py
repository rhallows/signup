#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

signup_form = """
<html>
 <head>
 <title> Signup </title>
 <style type="text/css">
  .label {text-align:right}
  .error {color:red}
  </style>

 <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
            %(error_username)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
            %(error_password)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verifypw" value="">
          </td>
          <td class="error">
            %(error_verify)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(error_email)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>
"""

welcome_form = """
<html>
    <head><title>Welcome!</title></head>
    <body>
    <h1>Welcome %(username)s!</h1>
    </body>
</html>
"""


user_regex = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and user_regex.match(username)

pw_regex = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and pw_regex.match(password)

email_regex = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or email_regex.match(email)

class SignUp(webapp2.RequestHandler):

    def initial_form(self, username='username', error_username='', error_password='', error_verify='', email='email', error_email=''):
        self.response.write(signup_form % {'username': username,'error_username': error_username,'error_password': error_password,'error_verify': error_verify,'email': email,'error_email': error_email})
    def get(self):
        self.initial_form()


    #TODO defines a post function to write variables to the server and validate the data entered
    def post(self):
        have_error = False
        username=self.request.get('username')
        password=self.request.get('password')
        verify=self.request.get('verifypw')
        email=self.request.get('email')
        error_username, error_email, error_password, error_verify = "", "", "", ""



        if not valid_username(username):
            have_error = True
            error_username = 'Error: That is an invalid username'

        if not valid_password(password):
            have_error = True
            error_password = 'Error: That is an invalid password'

        if verify != password:
            have_error = True
            error_verify = 'Error: The passwords do not match'

        if not valid_email(email):
            have_error = True
            error_email = 'Error: That is an invalid e-mail address'

        if have_error:
            self.response.write(signup_form % {'username': username,'error_username': error_username,'error_password': error_password,'error_verify': error_verify,'email': email,'error_email': error_email})
        else:
            self.redirect('/welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.response.write(welcome_form % {'username': username})

app = webapp2.WSGIApplication([('/', SignUp), ('/welcome', Welcome)], debug=True)
