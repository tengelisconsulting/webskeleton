import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, call

from aiohttp import web
from box import Box
import jwt

from webskeleton import AuthConf, Req
import webskeleton.auth as auth


user_id = "test-user-id"


class AuthTest(IsolatedAsyncioTestCase):
    def test_issue_access_token(self):
        token = auth.issue_access_token(user_id)
        return

    def test_issue_and_parse_creds(self):
        token = auth.issue_access_token(user_id)
        bearer_creds = f"Bearer {token}"
        claims = auth.creds_parse_bearer(bearer_creds)
        self.assertEqual(claims["user_id"], user_id)
        return

    async def test_issue_refresh_token(self):
        import webskeleton.appredis as appredis
        appredis.set_str = AsyncMock()
        token = await auth.issue_refresh_token(user_id)
        save_call = appredis.set_str.call_args_list[0]
        self.assertEqual(save_call.args[0], token)
        self.assertEqual(save_call.args[1], user_id)
        return

    async def test_check_authorized_policy(self):
        import webskeleton.autheval as autheval
        request_objects = ["obj-1"]
        req = Req(wrapped = None)
        req.user_id = "test-user-id"
        auth_conf = AuthConf(
            policy = "user-owns",
            obj_ids = lambda _req: request_objects,
        )
        autheval.user_owns_all = AsyncMock(
            return_value=True
        )
        self.assertTrue(
            await auth.check_authorized_policy(
                req, auth_conf)
        )
        auth_eval_call = autheval.user_owns_all.call_args_list[0]
        self.assertEqual(
            auth_eval_call.args[0],
            req.user_id,
        )
        self.assertEqual(
            auth_eval_call.args[1],
            request_objects,
        )
        autheval.user_owns_all = AsyncMock(
            return_value=False
        )
        with self.assertRaises(web.HTTPForbidden):
            await auth.check_authorized_policy(
                req, auth_conf)
        return


if __name__ == '__main__':
    unittest.main()