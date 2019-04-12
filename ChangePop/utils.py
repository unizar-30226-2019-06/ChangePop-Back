
def api_resp(code, mtype, msg):
    r = {
        "code": str(code),
        "type": str(mtype),
        "message": str(msg)}
    return r
