import sys

import frida


# hook回调函数
def on_message(message, data):
    if message['type'] == 'send':
        print("[*] Hooked function:", message['payload'])
    else:
        print("[-] Error:", message['description'])


script_code = '''

console.log("ApiResolver Started");
var resolver = new ApiResolver('objc');
//objc为要过滤的类
resolver.enumerateMatches('+[NSURL *URLWithString*]', {
   onMatch: function(match) {
      var method = match['name'];
      var implementation = match['address'];
      console.log("method_name = " + match['name']);
      // 过滤需要拦截的方法 URLWithString
      if ((method.indexOf("+[NSURL URLWithString:]") != -1)) {
  
         console.log("hooked : " + match['name'] + " " + match['address']);
         try {
            Interceptor.attach(implementation, {
               onEnter: function(args) {
                  //参数打印
                  var className = ObjC.Object(args[0]);
                  var methodName = args[1];
                  var arg_info = ObjC.Object(args[2]);
  
                  console.log("className: " + className.toString());
                  console.log("methodName: " + methodName.readUtf8String());
                  console.log("arg_info: " + arg_info.toString());
                  send(args)
  
               },
               onLeave: function(retval) {
  
               }
            });
         } catch (err) {
            console.log("[!] Exception: " + err.message);
         }
      }
  
   },
   onComplete: function() {
   }
});  
'''

# 加载JavaScript脚本
# with open('hook.js', 'r') as f:
#     script_code = f.read()

# 连接到目标进程,attach传入进程名称（字符串）或者进程号（整数）
session = frida.attach("devutils")
# 创建并注入JavaScript脚本
script = session.create_script(script_code)
script.on('message', on_message)
script.load()
sys.stdin.read()

# python3 hook.py
if __name__ == '__main__':
    print("")