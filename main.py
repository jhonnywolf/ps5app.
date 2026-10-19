import ipaddress
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

# ============ CONFIGURE AQUI ============
HOSTS = [
    ("Prospero Manager", "http://{ip}:7070/"),
    ("Payload Manager", "http://{ip}:8084/"),
]
FALLBACK_TCP_PORTS = [9021, 9020, 9090, 9295]
# ========================================

BG = (0.043, 0.063, 0.125, 1)
BLUE = (0.145, 0.388, 0.922, 1)
GRAY = (0.153, 0.196, 0.322, 1)


def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except OSError:
        return "192.168.0.2"
    finally:
        s.close()


def discover_udp(my_ip):
    net = ipaddress.ip_network(f"{my_ip}/24", strict=False)
    msg = b"SRCH * HTTP/1.1\ndevice-discovery-protocol-version:00030010\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(0.5)
    found = []
    try:
        sock.bind((my_ip, 0))
        for t in ("255.255.255.255", str(net.broadcast_address)):
            sock.sendto(msg, (t, 987))
        end = time.time() + 3
        while time.time() < end:
            try:
                data, addr = sock.recvfrom(2048)
            except socket.timeout:
                continue
            if b"PS5" in data.upper() and addr[0] not in found:
                found.append(addr[0])
    finally:
        sock.close()
    return found


def probe(a):
    try:
        with socket.create_connection(a, timeout=0.4):
            return a[0]
    except OSError:
        return None


def discover_tcp(my_ip):
    net = ipaddress.ip_network(f"{my_ip}/24", strict=False)
    jobs = [(str(h), p) for h in net.hosts() for p in FALLBACK_TCP_PORTS]
    with ThreadPoolExecutor(150) as ex:
        return sorted({r for r in ex.map(probe, jobs) if r and r != my_ip})


def open_url(url):
    try:
        from jnius import autoclass
        Intent = autoclass("android.content.Intent")
        Uri = autoclass("android.net.Uri")
        Activity = autoclass("org.kivy.android.PythonActivity")
        intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        Activity.mActivity.startActivity(intent)
    except Exception:
        import webbrowser
        webbrowser.open(url)


def mkbtn(text, color=BLUE):
    return Button(text=text, font_size=sp(18), bold=True, size_hint_y=None,
                  height=dp(60), background_normal="", background_color=color)


class PS5App(App):
    title = "PS5 App"

    def build(self):
        Window.clearcolor = BG
        self.ip = None
        self.scanning = False
        root = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(12))
        root.add_widget(Label(text="PS5 App", font_size=sp(26), bold=True,
                              size_hint_y=None, height=dp(50)))
        self.ip_label = Label(text="-", font_size=sp(30), bold=True,
                              color=(0.35, 0.64, 1, 1), size_hint_y=None, height=dp(50))
        root.add_widget(self.ip_label)
        self.msg = Label(text="Toque em Buscar PS5", font_size=sp(15),
                         halign="center", valign="middle")
        self.msg.bind(size=lambda w, s: setattr(w, "text_size", s))
        root.add_widget(self.msg)
        self.scan_btn = mkbtn("Buscar PS5")
        self.scan_btn.bind(on_release=lambda *_: self.start_scan())
        root.add_widget(self.scan_btn)
        self.host_btns = []
        for name, url in HOSTS:
            b = mkbtn(name, GRAY)
            b.disabled = True
            b.bind(on_release=lambda _b, u=url: open_url(u.replace("{ip}", self.ip or "")))
            root.add_widget(b)
            self.host_btns.append(b)
        self.both_btn = mkbtn("Abrir os dois")
        self.both_btn.disabled = True
        self.both_btn.bind(on_release=lambda *_: self.open_both())
        root.add_widget(self.both_btn)
        return root

    def on_start(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.INTERNET])
        except Exception:
            pass

    def set_state(self, ip, msg, scanning):
        self.ip, self.scanning = ip, scanning
        self.ip_label.text = ip or "-"
        self.msg.text = msg
        self.scan_btn.disabled = scanning
        self.scan_btn.text = "Buscando..." if scanning else "Buscar PS5"
        for b in self.host_btns + [self.both_btn]:
            b.disabled = not ip

    def start_scan(self):
        if self.scanning:
            return
        self.set_state(None, "Procurando PS5 na rede...", True)
        threading.Thread(target=self._scan, daemon=True).start()

    def _scan(self):
        try:
            me = local_ip()
            found = discover_udp(me) or discover_tcp(me)
            if found:
                res = (found[0], f"PS5 encontrado: {found[0]}")
            else:
                res = (None, "PS5 não encontrado. Confira o Wi-Fi e se ele está ligado/em repouso.")
        except Exception as e:
            res = (None, f"Erro: {e}")
        Clock.schedule_once(lambda dt: self.set_state(res[0], res[1], False))

    def open_both(self):
        def run():
            for _, url in HOSTS:
                open_url(url.replace("{ip}", self.ip or ""))
                time.sleep(1.2)
        threading.Thread(target=run, daemon=True).start()


if __name__ == "__main__":
    PS5App().run()
