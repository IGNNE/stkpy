#!/bin/python3

from pathlib import Path
from os import getenv
from argparse import ArgumentParser
import requests


kodi_url = 'http://kodi.local:8080/jsonrpc'
kodi_user = 'kodi'
kodi_pass = 'kodi'
config_file_path = None
ytdl_opts_str = ''
config_file_paths = [
                      Path('.stkpy'),
                      Path.home() / '.stkpy',
                      Path.home() / '.config/' '.stkpy',
                    ]
has_appdata = getenv('LOCALAPPDATA')
if has_appdata is not None:
    config_file_paths.append(Path(has_appdata) / 'stkpy' / '.stkpy')
for p in config_file_paths:
    if p.is_file():
        config_file_path = p
        break
if config_file_path is not None:
    with open(str(config_file_path), mode='r') as f:
        for l in f:
            if l.lower().startswith('kodi_url'):
                kodi_url = l.split('=')[1].strip()
            elif l.lower().startswith('ytdl_opts'):
                ytdl_opts_str = l.split('=')[1].strip()
            elif l.lower().startswith('kodi_user'):
                kodi_user = l.split('=')[1].strip()
            elif l.lower().startswith('kodi_pass'):
                kodi_pass = l.split('=')[1].strip()


parser = ArgumentParser()
parser.add_argument('url_to_send')
parser.add_argument('--verbose', '-v', action='store_true')
parser.add_argument('--ytdl_opts', '-o', help='add additional ytdl options in the format' +
                    '"key":"value" (will be appended to the ones found in the config file)')
args = parser.parse_args()
if args.ytdl_opts is not None:
    args.ytdl_opts.strip()
    # fix / add ""
    if not '"' in args.ytdl_opts:
        args.ytdl_opts = '"' + args.ytdl_opts + '"'
        args.ytdl_opts = args.ytdl_opts.replace(':', '":"')
        args.ytdl_opts = args.ytdl_opts.replace(',', '","')
    if ytdl_opts_str is not None:
        ytdl_opts_str += ',' + args.ytdl_opts
    else:
        ytdl_opts_str += args.ytdl_opts

# and get us into the format of
# ' {\"ydlOpts\":{\"username\":\"user@email.com\",\"password\":\"password with spaces\"}}'
if ytdl_opts_str is not None:
    ytdl_opts_str = ytdl_opts_str.replace('"', '\\"')
    ytdl_opts_str = ' {\\"ydlOpts\\":{' + ytdl_opts_str + '}}'

# a bit clumsy, probably smarter to use python json, but heh, strings work fine
request_str = """{
	"jsonrpc": "2.0",
	"method": "Player.Open",
	"params": {
		"item": {
			"file": "plugin://plugin.video.sendtokodi/?""" +  args.url_to_send + ytdl_opts_str + """"
		}
	},
	"id": 1
}
"""

if args.verbose:
    print(f"Attempting to send:\n{request_str}\nto {kodi_url}\nwith user: {kodi_user} pass: {kodi_pass}")

req = requests.post(kodi_url, data=request_str, auth=(kodi_user, kodi_pass))
if args.verbose: 
    print(f"Got status {req.status_code} data {req.text}")
