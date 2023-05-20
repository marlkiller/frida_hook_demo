import frida
import sys

jscode = """
Java.perform(function(){
    var Adconfig = Java.use('com.bytedance.sdk.openadsdk.TTAdConfig');
    Adconfig.getAppId.implementation = function(){
        return 0
    }
});

"""


def on_message(message, data):
    print(message)


process = frida.get_usb_device().attach('学小易')
script = process.create_script(jscode)
script.on('message', on_message)
script.load()
sys.stdin.read()
