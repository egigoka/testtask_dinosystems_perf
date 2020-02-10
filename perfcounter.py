import sys
import psutil
import time
from commands import *

try:
    subfolder = sys.argv[1]
    if not Dir.exist(subfolder):
        Dir.create(subfolder)
except IndexError:
    print("Pass a subfolder name as arg")
    sys.exit(1)

results = {}

def capture_results():
    while True:
        b = Bench(quiet=False)
        for p in psutil.process_iter():
            time.sleep(0.001)
            pdict = p.as_dict(attrs=['pid', 'name', 'username', 'memory_info', 'cmdline', 'num_threads', "cpu_percent"])
            if not pdict["cmdline"]:
                continue
            if pdict['cmdline'][0].startswith("/System/Library/PrivateFrameworks/"):
                continue
            if pdict['cmdline'][0].startswith('/System/Library/CoreServices'):
                continue
            if pdict['cmdline'][0].startswith('/System/Library/Frameworks/'):
                continue
            if pdict["name"] in ['cfprefsd', 'UserEventAgent', 'distnoted', 'lsd', 'trustd', 'secd', 'nsurlsessiond',
                                     'rapportd', 'usernoted', 'routined', 'pboard', 'nsurlstoraged', 'garcon', 'sharingd',
                                     'PAH_Extension', 'sh', 'dmd', 'bash', 'icdd', 'iStatMenusAgent', 'NotificationAgent',
                                     'iStat Menus Status', 'LuLu Helper', 'dwagent', 'AppleSpell', 'USBAgent',
                                     'com.apple.iTunesLibraryService', 'siriknowledged', 'cDock Helper', 'pycharm',
                                     'fsnotifier', 'AdobeIPCBroker', 'prl_deskctl_agent', 'avconferenced',
                                     'ckkeyrolld', 'ipcserver', 'silhouette', 'loginitemregisterd', 'pkd', 'secinitd',
                                     'com.apple.Safari.History', 'fmfd', 'node', 'TextEdit', 'nano', 'knowledge-agent',
                                     'keyboardservicesd', 'videosubscriptionsd', 'networkserviceproxy', 'swcd',
                                     'spindump_agent', 'ssh-agent', 'ParallelsIM']:
                continue
            else:
                pdict["friendly_name"] = pdict["cmdline"][-1].split("/")[-1]  # last file of last cmd art

                name = f'{pdict["name"]}:{pdict["friendly_name"]}:{pdict["pid"]}'
                cpu = f'{round(pdict["cpu_percent"], 2)}%'
                mem = f'{round(pdict["memory_info"].rss/1024/1024, 2)}Mb'
                thr = f'{pdict["num_threads"]}'
                time_ = Time.dotted()
                try:
                    results[name]
                except KeyError:
                    results[name] = {}
                results[name][time_] = {}
                results[name][time_]["cpu"] = cpu
                results[name][time_]["mem"] = mem
                results[name][time_]["thr"] = thr
        b.end()
        time.sleep(10)
        CLI.wait_update()

thr = MyThread(capture_results)
thr.start(wait_for_keyboard_interrupt=True)

results = Dict.sorted_by_key(results)

for name, times in Dict.iterable(results):
    times = Dict.sorted_by_key(times)
    for time, values in Dict.iterable(times):
        filepath = Path.combine(Path.working(), subfolder, f"{name}_load.log")
        string = f"{time}>\tcpu:{values['cpu']}\tmem:{values['mem']}\tthr:{values['thr']}{newline}"
        File.write(filepath, string, mode="a")
