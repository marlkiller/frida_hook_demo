import frida


def on_message(message, data):
    print("[on_message] message:", message, "data:", data)


session = frida.attach("main")

script = session.create_script("""'use strict';

    rpc.exports.enumerateModules = function () {
    return Process.enumerateModulesSync();
    };
    """)


# android 获取所有方法
"""
Java.perform(function () {
    Java.use('类名').class.getDeclaredMethods().forEach(function (method) {
      var methodName = method.toString();
      console.log("method name = " + methodName);
      try {
        // .. hook here
      } catch (e) { 
        console.error(methodName, e);
      }
    });
});
"""
# android 获取所有类名
"""
for (var className in ObjC.classes)
    {
        if (ObjC.classes.hasOwnProperty(className))
        {
            console.log(className);
        }
}
"""

script.on("message", on_message)
script.load()

print([m["name"] for m in script.exports.enumerate_modules()])

"""
python3 enumerate_modules.py
[
    'main', 'libc++.1.dylib', 'libSystem.B.dylib', 'libc++abi.dylib', 
    'libcache.dylib', 'libcommonCrypto.dylib', 'libcompiler_rt.dylib', 
    'libcopyfile.dylib', 'libcorecrypto.dylib', 'libdispatch.dylib',
    'libdyld.dylib', 'libkeymgr.dylib', 'libmacho.dylib', 'libquarantine.dylib',
    'libremovefile.dylib', 'libsystem_asl.dylib', 'libsystem_blocks.dylib', 
    'libsystem_c.dylib', 'libsystem_collections.dylib', 'libsystem_configuration.dylib', 
    'libsystem_containermanager.dylib', 'libsystem_coreservices.dylib', 'libsystem_darwin.dylib',
    'libsystem_dnssd.dylib', 'libsystem_featureflags.dylib', 'libsystem_info.dylib', 
    'libsystem_m.dylib', 'libsystem_malloc.dylib', 'libsystem_networkextension.dylib',
    'libsystem_notify.dylib', 'libsystem_sandbox.dylib', 'libsystem_secinit.dylib',
    'libsystem_kernel.dylib', 'libsystem_platform.dylib', 'libsystem_pthread.dylib',
    'libsystem_symptoms.dylib', 'libsystem_trace.dylib', 'libunwind.dylib', 'libxpc.dylib',
    'libobjc.A.dylib', 'liboah.dylib', 'dyld'
]

"""
