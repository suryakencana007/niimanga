"""
 # Copyright (c) 03 2015 | surya
 # 02/03/15 nanang.ask@kubuskotak.com
 # This program is free software; you can redistribute it and/or
 # modify it under the terms of the GNU General Public License
 # as published by the Free Software Foundation; either version 2
 # of the License, or (at your option) any later version.
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License
 # along with this program; if not, write to the Free Software
 # Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 #  auth.py
"""
from datetime import datetime
import logging

from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.security import remember
from pyramid.view import view_config
from niimanga.configs.view import ZHandler
from niimanga.libs.oauth.decoratorwrap import tokenizer
from niimanga.libs.utils import ResponseHTTP
from niimanga.models.auth import UserMgr, ActivationMgr
from sqlalchemy.exc import IntegrityError


LOG = logging.getLogger(__name__)


class Auth(ZHandler):
    @view_config(route_name="login", renderer="json")
    def login(self):
        """Login for API Mobile"""
        with ResponseHTTP(response=self.R.response) as t:
            if 'POST' in self.R.method:
                params = self.R.params
                login = params.get('email')
                password = params.get('password')
                data = {}

                auth = UserMgr.get(email=login)
                if auth and auth.validate_password(password) and auth.is_activated:
                    auth.last_login = datetime.utcnow()

                    code, status = ResponseHTTP.OK
                    _in = u'success'
                    message = "Login is successfully."
                    data = {
                        'key': auth.api_key,
                        'secret': auth.secret,
                        'client_id': auth.id
                    }
                else:
                    _in = u'failed'

                    message = "Failed login"
                    # log the right level of problem
                    if auth and not auth.validate_password(password):

                        # AuthLog.login(login, False, password=password)
                        message = 'Your login attempt has failed.'
                        code, status = ResponseHTTP.NOT_AUTHORIZED

                    elif auth and not auth.is_activated:

                        message = "User account deactivated. Please check your email."
                        code, status = ResponseHTTP.NOT_AUTHORIZED
                        # AuthLog.login(login, False, password=password)
                        # AuthLog.disabled(login)

                    elif auth is None:

                        message = "Failed login"
                        code, status = ResponseHTTP.NOT_AUTHORIZED
                        # AuthLog.login(login, False, password=password)

        return t.to_json(_in,
                         data=data,
                         message=message,
                         code=code, status=status)

    @view_config(route_name="signup_process", renderer="json")
    def signup_process(self):
        """Process the signup request

        If there are any errors drop to the same template with the error
        information.

        """
        with ResponseHTTP(response=self.R.response) as t:
            # request.response.status_code = 401
            params = self.R.params
            email = params.get('email', None)
            password = params.get('password', None)
            _in = u'Failed'

            if not email:
                # if still no email, I give up!
                message = 'Please supply an email address to sign up.'
                code, status = ResponseHTTP.NOT_AUTHORIZED

            elif UserMgr.get(email=email):
                message = 'The user has already signed up.'
                code, status = ResponseHTTP.NOT_AUTHORIZED

            elif not UserMgr.acceptable_password(password):
                # @Surya
                # Custom case exception for not use email activation
                # Set an error message to the template.
                message = 'Come on, pick a real password please.'
                code, status = ResponseHTTP.NOT_AUTHORIZED

            else:
                _in = u'success'
                # set default allowed scopes untuk client / member
                new_user = UserMgr.signup_user(email, 'signup', ['member:basic'])
                activation = new_user.activation.code
                res = ActivationMgr.activate_user(new_user.username, activation, password)

                if new_user:
                    code, status = ResponseHTTP.OK
                    # then this user is able to invite someone
                    # log it
                    # AuthLog.reactivate(new_user.username)

                    # and then send an email notification
                    # @todo the email side of things
                    # settings = self.R.registry.settings

                    # Add a queue job to send the user a notification email.
                    # tasks.email_signup_user.delay(
                    #     new_user.email,
                    #     "Enable your Bookie account",
                    #     settings,
                    #     request.route_url(
                    #         'reset',
                    #         username=new_user.username,
                    #         reset_key=new_user.activation.code
                    #     )
                    # )

                    # And let the user know they're signed up.
                    message = 'Thank you for signing up from: ' + new_user.email
                else:
                    code, status = ResponseHTTP.BAD_REQUEST
                    message = 'There was an unknown error signing up.'

        return t.to_json(_in,
                         message=message,
                         code=code, status=status)

    @view_config(route_name="reset", renderer="/auth/reset.mako")
    def reset(self):
        """Once deactivated, allow for changing the password via activation key"""
        rdict = self.R.matchdict
        params = self.R.params

        # This is an initial request to show the activation form.
        username = rdict.get('username', None)
        activation_key = rdict.get('reset_key', None)
        user = ActivationMgr.get_user(username, activation_key)

        if user is None:
            # just 404 if we don't have an activation code for this user
            raise HTTPNotFound()

        if 'code' in params:
            # This is a posted form with the activation, attempt to unlock the
            # user's account.
            username = params.get('username', None)
            activation = params.get('code', None)
            password = params.get('new_password', None)
            new_username = params.get('new_username', None)
            error = None

            if not UserMgr.acceptable_password(password):
                # Set an error message to the template.
                error = "Come on, pick a real password please."
            else:
                res = ActivationMgr.activate_user(username, activation, password)
                if res:
                    # success so respond nicely
                    # AuthLog.reactivate(username, success=True, code=activation)

                    # if there's a new username and it's not the same as our current
                    # username, update it
                    if new_username and new_username != username:
                        try:
                            user = UserMgr.get(username=username)
                            user.username = new_username
                        except IntegrityError, exc:
                            error = 'There was an issue setting your new username'
                else:
                    # AuthLog.reactivate(username, success=False, code=activation)
                    error = 'There was an issue attempting to activate this account.'

            if error:
                return {
                    'message': error,
                    'user': user
                }
            else:
                # Log the user in and move along.
                headers = remember(self.R, user.id, max_age=60 * 60 * 24 * 30)
                user.last_login = datetime.utcnow()

                # log the successful login
                # AuthLog.login(user.username, True)

                # we're always going to return a user to their own /recent after a
                # login
                return HTTPFound(
                    location=self.R.route_url(
                        'user_bmark_recent',
                        username=user.username),
                    headers=headers)

        else:
            LOG.error("CHECKING")
            LOG.error(username)

            if user is None:
                # just 404 if we don't have an activation code for this user
                raise HTTPNotFound()

            LOG.error(user.username)
            LOG.error(user.email)
            return dict(user=user)

    @view_config(route_name="api_header", renderer="json")
    @tokenizer('token', UserMgr.get, allowed_scopes="member:basic")
    def test_header(self, **kwargs):
        request = self.R
        context = kwargs.pop('oauth_context', None)

        # LOG.debug(context.scopes)
        if not hasattr(request, 'authorization') or request.authorization is None:
            return None

        try:
            auth_method, information = request.authorization
        except ValueError: # not enough values to unpack
            return None
        LOG.debug(u'84b56af69b59333957bbf927ee65be0560536513:Aa7M6n~BD.uMUFGtRqQB'.encode('base64'))
        LOG.debug(u'QjNUNnVjRU01bm5oU2ZwYkNyNkpjZnJGLU1RfmtjUk4='.decode('base64'))
        print(dict(type=auth_method, token=information.strip()))
        return dict(type=auth_method, token=information.strip())