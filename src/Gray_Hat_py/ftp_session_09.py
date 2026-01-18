from boofuzz import *
# from requests import ftp   # <-- remove this, it breaks

def recuive_ftp_banner(sock):
    sock.recv(1024)

sess = sessions.session(session_filename="audit/audits/warftpd.session")
target = sessions.target("127.0.0.1", 21)   # local device -> localhost

# network sniffer and process monitor clients
target.netmon = pedrpc.client("127.0.0.1", 26001)
# debugger client listening on port 26002
target.procmon = pedrpc.client("127.0.0.1", 26002)
target.procmon_options = {"proc_name": "warftpd.exe"}

sess.add_target(target)
sess.pre_send = recuive_ftp_banner

sess.connect(s_get("usr"))
sess.connect(s_get("usr"), s_get("pass"))
sess.connect(s_get("pass"), s_get("cwd"))
sess.connect(s_get("pass"), s_get("dele"))
sess.connect(s_get("pass"), s_get("mdtm"))
sess.connect(s_get("pass"), s_get("mkd"))
sess.fuzz()
