from quart import *
import os
import json
import time
import datetime
import random

import config
app = Quart(__name__)
text_200 = """# 欢迎使用 `CodePaste` 代码剪贴板
只需要选中并删除这段文字，在这里粘贴您的代码，然后在上方输入语言（如 md/py/c++等），然后点击**贴出当前代码**就可以了。

===

CodePaste
Version: 2.0
Author: zsh2517

===
"""
text_404 = "# 错误\n未找到该页面\n可能是该页面已过期或不存在\n请检查有效期和URL是否正确"
text_401 = "# 需要密码验证\n请刷新本页面，在弹出的密码框中输入密码以查看文件"

hosturl = config.host_url


def randstr(length, dic="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    while True:
        dic = list(dic)
        ret = ""
        for i in range(0, length):
            ret = ret + random.choice(dic)
        if not os.path.exists("./data/" + ret + ".json"):
            break
    return "cp" + ret


async def return_302():
    resp = await make_response("302 TO /PASTE")
    resp.headers["Location"] = "/paste"
    resp.status_code = 302
    return resp


async def return_404(data):
    d = {
        "language": "markdown",
        "code": text_404,
        "pwd": "false",
        "author": "None",
        "bgntime": "None",
        "exptime": "None",
        "desc": "本页面可能已过期或者未找到",
        "notfound": "true",
        "fname": "401 Page NOT FOUND"
    }
    resp = await make_response(await render_template("paste.html", **d))
    resp.status_code = 404
    return resp


async def return_401(data):
    # 上面 check401 判断是否有密码了
    d = {
        "language": "markdown",
        "code": text_401,
        "pwd": "true",
        "author": "[Hide]",
        "bgntime": "[Hide]",
        "exptime": "[Hide]",
        "desc": "本页面需要密码访问，请重新加载页面",
        "notfound": "false",
        "fname": "401 Page Need Password"
    }
    resp = await make_response(await render_template("paste.html", **d))
    resp.status_code = 401
    return resp


async def check_status(pageid, methods="GET"):
    if pageid == "":
        return 302
    if os.path.exists("./data/" + pageid + ".json"):
        f = open("./data/" + pageid + ".json", "r", encoding="utf-8")
        data = json.load(f)
        f.close()
        if int(data["exp"]) != 0: # 存在过期时间
            now = time.time()
            if int(data["bgn"]) + int(data["exp"]) > now:
                return 403  # 过期
        if data["pwd"] != "":
            return 401 # 需要密码
            pass
        return 200 # 成功
    else:
        return 404 # 未找到

async def return_default():
    d = {
        "language": "markdown",
        "code": text_200,
        "pwd": "false",
        "notfound": "false"
    }
    resp = await make_response(await render_template("paste.html", **d))
    resp.status_code = 200
    return resp

async def return_200(data):
    d = {
        "language": data["lang"],
        "code": data["code"],
        "pwd": "false",
        "notfound": "false",
        "fname": data["fname"],
        "author": data["user"],
        "exptime": data["exp"],
        "desc": data["desc"],
        "bgntime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data["bgn"])))
    }
    if d["exptime"] == "0":
        d["exptime"] = "永久"
    else:
        now = time.localtime(int(data["bgn"]))
        now = datetime.datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(data["bgn"]))), "%Y-%m-%d %H:%M:%S")
        now = now + datetime.timedelta(seconds=int(d["exptime"]))
        # d["exptime"] = time.strftime("%Y-%m-%d %H:%M:%S", now)
        d["exptime"] = now
    resp = await make_response(await render_template("paste.html", **d))
    resp.status_code = 200
    return resp

# BUG 当一个页面被路由的时候，处于post情况下不会检测 过期

# TODO

# NOTE

err = """
sorry,<br>
Due to some reasons, I changed some of the JavaScript, and it didn't work.<br>
However, I didn't make a backup, and new bugs came out when I fix the old ones.<br>
So please wait, the website will be reopen in 2020/06/14<br>
"""
err = """
因为一些原因，网站前段时间临时改了一些内容<br>
由于没有备份，昨天在改回去的时候，出了一些问题<br>
解决这些问题的时候，又出现了新的BUG<br>
目前可能在一定程度上影响访问<br>
所以暂时关闭。预计1~2天恢复<br>
2020-06-12
"""
@app.route("/", methods=["GET"])
async def index():
    # return err
    resp = await make_response("302 TO /PASTE")
    resp.headers["Location"] = "/paste"
    resp.status_code = 302
    return resp


# GET 方式显示请求
@app.route("/paste", methods=["GET"])
@app.route("/paste/", methods=["GET"])
async def pastemain():
    # return err
    d = {
        "language": "markdown",
        "code": text_200,
        "pwd": "false",
        "notfound": "false"
    }
    resp = await make_response(await render_template("paste.html", **d))
    return resp


# POST 方式提交数据
@app.route("/paste", methods=["POST"])
async def postdata():
    ret = await request.form
    code = ret.get('code', default='No Code')
    desc = ret.get('desc', default='no description')
    if desc == "":
        desc = "No Description"
    bgn = round(time.time(), 0)
    exp = ret.get('exp', default='0')
    if exp == "":
        exp = "0"
    user = ret.get('user', default='annoymous')
    if user == "":
        user = "annoymous"
    lang = ret.get('lang', default='')
    fname = ret.get('fname', default='code_file')
    if fname == "":
        fname = "code_file"
    pwd = ret.get('pwd', default='')
    pageid = randstr(6, "123456789")
    print("write to file ./data/{0}.json".format(pageid))
    f = open("./data/" + pageid + ".json", "w", encoding="utf-8")
    data = {
        "code": code,
        "desc": desc,
        "bgn": bgn,
        "exp": exp,
        "user": user,
        "lang": lang,
        "fname": fname,
        "pwd": pwd
    }
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.close()
    data = {
        "url": hosturl + "/paste/" + pageid,
        "id": pageid
    }
    return await make_response(json.dumps(data, ensure_ascii=False))


# GET 方式请求页面
@app.route("/paste/<pageid>", methods=["GET"])
async def getpaste(pageid):
    # return err
    if pageid == "":
        print("QWQ")
        return await index()
    if pageid != pageid.lower():
        pageid = pageid.lower()
    if os.path.exists("./data/" + pageid + ".json"):
        f = open("./data/" + pageid + ".json", "r", encoding="utf-8")
        data = json.load(f)
        f.close()
        if int(data["exp"]) != 0:
            now = time.time()
            if int(data["bgn"]) + int(data["exp"]) < now:
                print(int(data["bgn"]), int(data["exp"]), now)
                return await return_404(data)
        if data["pwd"] != "":
            return await return_401(data)
        return await return_200(data)
    else:
        return await return_404(None)
    pass

# POST 方式提交密码
@app.route("/paste/<pageid>", methods=["POST"])
async def verify(pageid):
    form = await request.form
    f = open("./data/" + pageid + ".json", "r", encoding="utf-8")
    data = json.load(f)
    f.close()
    if form.get('pwd', default='') == data["pwd"]:
        return await return_200(data)
    else:
        # 进入的时候直接走form全局刷新
        # 密码错误的话，返回这个页面
        return await getpaste(pageid)
    pass

app.run(host="0.0.0.0", port=5010, debug=True)
