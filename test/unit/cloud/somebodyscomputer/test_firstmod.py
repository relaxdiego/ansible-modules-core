import mock
from StringIO import StringIO

from cloud.somebodyscomputer import firstmod


class TestFirstMod:

    @mock.patch("cloud.somebodyscomputer.firstmod.write_data", autospec=True)
    @mock.patch("cloud.somebodyscomputer.firstmod.fetch_data", autospec=True)
    @mock.patch("cloud.somebodyscomputer.firstmod.AnsibleModule", autospec=True)
    def test__main__success(self, ansible_mod_cls, fetch_data, write_data):
        # Prepare mocks
        ansible_mod_obj = ansible_mod_cls.return_value
        args = {
            "url": "https://www.google.com",
            "dest": "/tmp/somelocation.txt"
        }
        ansible_mod_obj.params = args

        html = "<html><head></head><body></body></html>"
        data = StringIO(html)
        fetch_data.return_value = data

        write_data.return_value = True

        # Exercise code
        firstmod.main()

        # Assert results
        expected_arguments_spec = dict(
            url=dict(required=True),
            dest=dict(required=False, default="/tmp/firstmod")
        )
        assert(mock.call(argument_spec=expected_arguments_spec) ==
               ansible_mod_cls.call_args)

        assert(mock.call(ansible_mod_obj, args["url"]) == fetch_data.call_args)

        assert(mock.call(ansible_mod_obj, data, args["dest"]) ==
               write_data.call_args)

        expected_args = dict(
            msg="Retrieved the resource successfully",
            changed=True
        )
        assert(mock.call(**expected_args) == ansible_mod_obj.exit_json.call_args)

    @mock.patch("cloud.somebodyscomputer.firstmod.fetch_url", autospec=True)
    @mock.patch("cloud.somebodyscomputer.firstmod.AnsibleModule", autospec=True)
    def test__fetch_data__success(self, ansible_mod_cls, fetch_url):
        # Mock objects
        url = "https://www.google.com"
        ansible_mod_obj = ansible_mod_cls.return_value

        html = "<html><head></head><body></body></html>"
        data = StringIO(html)
        info = {
            'status': 200
        }
        fetch_url.return_value = (data, info)

        # Exercise the code
        data = firstmod.fetch_data(ansible_mod_obj, url)

        # Assert the results
        expected_args = dict(module=ansible_mod_obj, url=url)
        assert(mock.call(**expected_args) == fetch_url.call_args)

        assert(html == data)

    @mock.patch("cloud.somebodyscomputer.firstmod.AnsibleModule", autospec=True)
    def test_save_file(self, ansible_mod_cls):
        dest = "/tmp/somelocation.txt"
        ansible_mod_obj = ansible_mod_cls.return_value

        html = "<html><head></head><body></body></html>"

        o_open = "cloud.somebodyscomputer.firstmod.open"
        m_open = mock.mock_open()
        with mock.patch(o_open, m_open, create=True):
            firstmod.write_data(ansible_mod_obj, html, dest)

        assert(mock.call(dest, "w") == m_open.mock_calls[0])
        assert(mock.call().write(html) == m_open.mock_calls[2])
