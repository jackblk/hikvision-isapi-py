# hikvision-isapi-py

Simple client to interact with Hikvision devices using the ISAPI protocol.

Source code: <https://github.com/jackblk/hikvision-isapi-py>

## Ignore SSL verification

Can be useful if you are using self-signed certificates or the web server
certificate is not trusted by your client.

Set the environment variable `VERIFY_SSL` to `false` (anything but `true` will skip the check)
