# Small sendtokodi Python CLI tool

This is a minimalistic little python script to send stuff to the great [sendtokodi](https://github.com/firsttris/plugin.video.sendtokodi). To use it, make sure you have the requests lib installed (`pip3 install requests`) create a file called `.stkpy` either in this directory, your home dir, `~/.config/` or even in `%LOCALAPPDATA/stkpy/` like this:

```
# example conf
kodi_url=http://kodi.local:8080/jsonrpc
kodi_user=kodi
kodi_pass=password-for-your-kodi
#ytdl_opts="f":"bestaudio"
```
You can put `--ytdl_opts=...` in your command line as well.

Then, just run something like `stkpy.py https://example.com/cool-video`. Intended for making shortcuts/macros/you name it.


