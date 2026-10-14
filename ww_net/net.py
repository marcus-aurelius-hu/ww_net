from socket import gaierror, gethostbyname, socket, AF_INET, SOCK_STREAM
from time import sleep, time, strftime
from urllib.parse import urlparse
from arin_log import log_notes
from random import choice
from sys import _getframe

br = chr(10)
prgnm = "ww_net"
LOG_THRESHOLD = 2.5

class CheckNet:
    def __init__(self, timeout=1.5, wait=3600, logloc=None):
        self.timeout = timeout
        self.wait = wait
        self.dns_servers = ["1.1.1.1", "8.8.8.8", "9.9.9.9", "208.67.222.222"]
        self.logloc = prgnm if logloc is None else logloc
        self.slpd = {'1;5': 1, '6;10': 2, '11;20': 3, '21;50': 4, '51;100': 5, '101;150': 6, '151;200': 7,
                     '201;300': 8, '301;400': 9, '401;600': 10, '601;1000': 11, '1001;1500': 12,
                     '1501;999999999': 15}

    def get_interval(self, count):
        """Return the sleep time based on the poll_count without logging."""
        slpt = 1
        for key in self.slpd:
            start, end = map(int, key.split(';'))
            if start <= count <= end:
                slpt = self.slpd[key]
                break
        return slpt

    def tcp_check(self, ip=None, timeout=None):
        if timeout is None:
            timeout = self.timeout if ip is None else 2.0
        host = choice(self.dns_servers) if ip is None else ip
        ports = [443, 80]

        for port in ports:
            try:
                with socket(AF_INET, SOCK_STREAM) as sock:
                    sock.settimeout(timeout)
                    if sock.connect_ex((host, port)) == 0:
                        return True
            except Exception:
                continue
        return False

    def is_net(self, wait=None, logloc=None):
        wait = self.wait if wait is None else wait
        logloc = self.logloc if logloc is None else logloc
        if self.tcp_check():
            return True
        return self.wait_net(typ='internet', wait=wait, logloc=logloc)

    def wait_net(self, typ=None, wait=None, logloc=None):
        typ = 'internet' if typ is None else typ
        wait = self.wait if wait is None else wait
        logloc = self.logloc if logloc is None else logloc
        fcnm = _getframe().f_code.co_name

        exc_time = time()
        start_time = time()
        count = 1
        logged = False

        while time() - start_time < wait:
            if self.tcp_check():
                if logged:
                    eltm = time() - exc_time
                    tmp = f"{typ} ; connection ; restored"
                    log_notes(tmp)
                    log_notes(f"✅ {tmp}", cons=False, logloc=logloc)
                    log_notes(f"✅ {prgnm} ; {fcnm} ; {eltm:.3f} sec{br}", cons=False, logloc=logloc)
                return True

            if not logged:
                eltm = time() - exc_time
                if eltm >= LOG_THRESHOLD:
                    tmp = f"{typ} ; connection ; exception"
                    log_notes(tmp)
                    log_notes(f"⚠️ {tmp}", cons=False, logloc=logloc)
                    log_notes(f"⚠️ {prgnm} ; {fcnm} ; {strftime('%H:%M:%S')}", cons=False, logloc=logloc)
                    logged = True

            interval = self.get_interval(count)
            count += 1
            sleep(interval)

        return False

    def is_host(self, host, wait=None, logloc=None):
        wait = self.wait if wait is None else wait
        logloc = self.logloc if logloc is None else logloc
        fcnm = _getframe().f_code.co_name

        if "://" in host:
            host = urlparse(host).netloc.replace('www.', '')

        if self.tcp_check():
            try:
                gethostbyname(host)
                start_time = time()
                exc_time = time()
                count = 1
                logged = False
                while time() - start_time < wait:
                    if self.tcp_check(ip=host):
                        if logged:
                            eltm = time() - exc_time
                            tmp = f"{host} ; connection ; restored"
                            log_notes(tmp)
                            log_notes(f"✅ {tmp}", cons=False, logloc=logloc)
                            log_notes(f"✅ {prgnm} ; {fcnm} ; {eltm:.3f} sec{br}", cons=False,
                                      logloc=logloc)
                        return True

                    if not logged:
                        eltm = time() - exc_time
                        if eltm >= LOG_THRESHOLD:
                            tmp = f"{host} ; connection ; exception"
                            log_notes(tmp)
                            log_notes(f"⚠️ {tmp}", cons=False, logloc=logloc)
                            log_notes(f"⚠️ {prgnm} ; {fcnm} ; {strftime('%H:%M:%S')}", cons=False,
                                      logloc=logloc)
                            logged = True

                    interval = self.get_interval(count)
                    count += 1
                    sleep(interval)

                return False
            except gaierror:
                return self.wait_net(typ=host, wait=wait, logloc=logloc)
            except Exception:
                return self.wait_net(typ=host, wait=wait, logloc=logloc)
        else:
            return self.wait_net(typ=host, wait=wait, logloc=logloc)

_net = CheckNet()

def is_net(wait=None, logloc=None):
    return _net.is_net(wait=wait, logloc=logloc)

def is_host(host, wait=None, logloc=None):
    return _net.is_host(host, wait=wait, logloc=logloc)

__all__ = ['is_net', 'is_host']

if __name__ == "__main__":
    from ww_net import demo
    demo()
