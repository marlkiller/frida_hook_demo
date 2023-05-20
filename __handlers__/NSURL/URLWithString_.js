{

    onEnter(log, args, state)
    {
        log("+[NSURL URLWithString:" + args[2] + "]");
        var objcHttpUrl = ObjC.Object(args[2]);  //获取 Objective-C 对象 NSString
        var strHttpUrl = objcHttpUrl.UTF8String();
        log("httpURL: " + strHttpUrl);
    }
,

    onLeave(log, retval, state)
    {
    }
}
