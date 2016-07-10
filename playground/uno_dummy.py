#!/usr/bin/env python3

import uno, time
import socket
import subprocess as sub

sub.Popen(['(','soffice','--calc','--accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"',')','&'])
time.sleep(5)
sub.Popen(['netstat','-nap','|','grep','soffice'])

'''
localContext = uno.getComponentContext()
resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",localContext)
ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
smgr = ctx.ServiceManager

desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop",ctx)

model = desktop.getCurrentComponent()
'''
