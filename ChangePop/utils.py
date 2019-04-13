
def api_resp(code, mtype, msg):
    # TODO Doc
    r = {
        "code": str(code),
        "type": str(mtype),
        "message": str(msg)}
    return r
