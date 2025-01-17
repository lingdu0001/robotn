# // Copyright 2016 The go-vgo Project Developers. See the COPYRIGHT
# // file at the top-level directory of this distribution and at
# // https://github.com/go-vgo/robotgo/blob/master/LICENSE
# //
# // Licensed under the Apache License, Version 2.0 <LICENSE-APACHE or
# // http://www.apache.org/licenses/LICENSE-2.0> or the MIT license
# // <LICENSE-MIT or http://opensource.org/licenses/MIT>, at your
# // option. This file may not be copied, modified, or distributed
# // except according to those terms.

from __future__ import print_function
import sys
import os
from cffi import FFI

is_64b = sys.maxsize > 2**32

ffi = FFI()
if is_64b:
    ffi.cdef("typedef long GoInt;\n")
else:
    ffi.cdef("typedef int GoInt;\n")

ffi.cdef("""
    typedef struct {
		GoInt x;
		GoInt y;
	} GoRInt;

	typedef struct {
		char* arr;
		char* err;
	} GoStr;

	char* GetVersion();
	void Sleep(GoInt tm);
	void MSleep(double tm);

	char* GetPixelColor(GoInt x, GoInt y);
	char* GetMouseColor();
    GoRInt GetScreenSize();
	GoRInt GetScaleSize();

    void MoveMose(GoInt x, GoInt y);
	void DargMose(GoInt x, GoInt y, char* btn);
	void MoveSmooth(GoInt x, GoInt y, double low, double high);
	GoRInt GetMousePos();
	void Click(char* btn, bool double_c);
	void MoseToggle(char* key, char* btn);
	void Scroll(GoInt x, GoInt y);

    char* KeyTap(char* key, char* vals);
    char* KeyToggle(char* key, char* vals);
    void TypeStr(char* str, double args);
	GoStr ReadAll();
    void WriteAll(char* str);
	void PasteStr(char* str);

	bool AddEvent(char* p0);
	void StopEvent();
	bool AddEvents(char* p0, char* p1);
	void End();
	bool AddMouse(char* p0, GoInt p1, GoInt p2);
	bool AddMousePos(GoInt p0, GoInt p1);

    char* GetTitle(GoInt pid);
    GoStr FindIds(char* name);
    GoStr FindName(GoInt pid);
	GoStr FindNames();
	char* ActivePID(GoInt pid);
	char* ActiveName(char* name);
    char* Kill(GoInt pid);
""")

dir = os.path.dirname(__file__)
bin = os.path.join(dir, "../robotgo")
lib = ffi.dlopen(bin)


def ch(s):
    return s.encode('utf-8')


def f_str(cs):
    return ffi.string(cs)


def getVersion():
    ver = lib.GetVersion()
    return f_str(ver)


def sleep(tm):
    lib.Sleep(tm)


def MSleep(tm):
    lib.MSleep(tm)

# /*
#       _______.  ______ .______       _______  _______ .__   __.
#     /       | /      ||   _  \     |   ____||   ____||  \ |  |
#    |   (----`|  ,----'|  |_)  |    |  |__   |  |__   |   \|  |
#     \   \    |  |     |      /     |   __|  |   __|  |  . `  |
# .----)   |   |  `----.|  |\  \----.|  |____ |  |____ |  |\   |
# |_______/     \______|| _| `._____||_______||_______||__| \__|
# */


def getPixelColor(x, y):
    color = lib.GetPixelColor(x, y)
    return f_str(color)


def getMouseColor():
    color = lib.GetMouseColor()
    return f_str(color)


def getScreenSize():
    s = lib.GetScreenSize()
    return s.x, s.y


def getScaleSize():
    s = lib.GetScaleSize()
    return s.x, s.y

# /*
# .___  ___.   ______    __    __       _______. _______
# |   \/   |  /  __  \  |  |  |  |     /       ||   ____|
# |  \  /  | |  |  |  | |  |  |  |    |   (----`|  |__
# |  |\/|  | |  |  |  | |  |  |  |     \   \    |   __|
# |  |  |  | |  `--'  | |  `--'  | .----)   |   |  |____
# |__|  |__|  \______/   \______/  |_______/    |_______|

# */


def moveMose(x, y):
    lib.MoveMose(x, y)


def dargMose(x, y, btn="left"):
    lib.dargMose(x, y, ch(btn))


def moveSmooth(x, y, low=1.0, high=3.0):
    lib.MoveSmooth(x, y, low, high)


def click(btn="left", double_c=False):
    lib.Click(ch(btn), double_c)


def moseToggle(key, btn):
    lib.moseToggle(ch(key), ch(btn))


def scroll(x, y):
    lib.Scroll(x, y)

# /*
#  __  ___  ___________    ____ .______     ______        ___      .______       _______
# |  |/  / |   ____\   \  /   / |   _  \   /  __  \      /   \     |   _  \     |       \
# |  '  /  |  |__   \   \/   /  |  |_)  | |  |  |  |    /  ^  \    |  |_)  |    |  .--.  |
# |    <   |   __|   \_    _/   |   _  <  |  |  |  |   /  /_\  \   |      /     |  |  |  |
# |  .  \  |  |____    |  |     |  |_)  | |  `--'  |  /  _____  \  |  |\  \----.|  '--'  |
# |__|\__\ |_______|   |__|     |______/   \______/  /__/     \__\ | _| `._____||_______/

# */


def arr_add(args):
    arr = ""
    for i in range(len(args)):
        if i < len(args)-1:
            arr += args[i] + ","
        else:
            arr += args[i]

    return arr


def keyTap(key, *vals):
    arr = arr_add(vals)
    s = lib.KeyTap(ch(key), ch(arr))
    return f_str(s)


def KeyToggle(key, *vals):
    arr = arr_add(vals)
    s = lib.KeyToggle(ch(key), ch(arr))
    return f_str(s)


def typeStr(s, args=3.0):
    lib.TypeStr(ch(s), args)


def writeAll(s):
    lib.WriteAll(ch(s))


def pasteStr(s):
    lib.pasteStr(ch(s))

# /*
# .______    __  .___________..___  ___.      ___      .______
# |   _  \  |  | |           ||   \/   |     /   \     |   _  \
# |  |_)  | |  | `---|  |----`|  \  /  |    /  ^  \    |  |_)  |
# |   _  <  |  |     |  |     |  |\/|  |   /  /_\  \   |   ___/
# |  |_)  | |  |     |  |     |  |  |  |  /  _____  \  |  |
# |______/  |__|     |__|     |__|  |__| /__/     \__\ | _|
# */


# /*
#  ___________    ____  _______ .__   __. .___________.
# |   ____\   \  /   / |   ____||  \ |  | |           |
# |  |__   \   \/   /  |  |__   |   \|  | `---|  |----`
# |   __|   \      /   |   __|  |  . `  |     |  |
# |  |____   \    /    |  |____ |  |\   |     |  |
# |_______|   \__/     |_______||__| \__|     |__|
# */

def addEvent(key):
    return lib.AddEvent(ch(key))


def end():
    lib.End()


def addEvents(key, *vals):
    arr = arr_add(vals)
    return lib.AddEvents(ch(key), ch(arr))


def end():
    lib.End()


def addMouse(btn, x=-1, y=-1):
    return lib.AddMouse(ch(btn), x, y)


def addMousePos(x, y):
    return lib.AddMousePos(x, y)

# /*
# ____    __    ____  __  .__   __.  _______   ______   ____    __    ____
# \   \  /  \  /   / |  | |  \ |  | |       \ /  __  \  \   \  /  \  /   /
#  \   \/    \/   /  |  | |   \|  | |  .--.  |  |  |  |  \   \/    \/   /
#   \            /   |  | |  . `  | |  |  |  |  |  |  |   \            /
#    \    /\    /    |  | |  |\   | |  '--'  |  `--'  |    \    /\    /
#     \__/  \__/     |__| |__| \__| |_______/ \______/      \__/  \__/

# */


def arr(s):
    st = bytes.decode(f_str(s))
    return st.split(' ')


def getTitle(pid=-1):
    s = lib.GetTitle(pid)
    return f_str(s)


def findIds(name):
    s = lib.FindIds(ch(name))

    err = str(f_str(s.err))
    if err == "b''":
        return arr(s.arr)

    return err


def findName(pid):
    s = lib.FindName(pid)
    return f_str(s)


def findNames():
    s = lib.FindNames()

    err = str(f_str(s.err))
    if err == "b''":
        return arr(s.arr)

    return err


def activePID(pid):
    err = lib.ActivePID(pid)
    return f_str(err)


def activeName(name):
    err = lib.ActiveName(ch(name))
    return f_str(err)


def kill(pid):
    lib.Kill(pid)
