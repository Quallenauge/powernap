# $Id: PKGBUILD 193962 2013-09-08 19:31:47Z eric $
# Maintainer: Eric Bélanger <eric@archlinux.org>

pkgbase=powernap
pkgname=('powernap_common'
         'powernap_server'
)

pkgver=2.18
pkgrel=1
arch=('i686' 'x86_64')
url="https://launchpad.net/powernap"
license=('GPL')
#makedepends=('cmake')
#options=('!makeflags')
#install=audacity.install
source=(
#https://launchpad.net/powernap/trunk/${pkgver}/+download/powernap_${pkgver}.orig.tar.gz
'powernap.conf'
)

prepare() {
  cp -r "${srcdir}/../powernap" "${srcdir}/powernap-${pkgver}"
}

package_powernap_common() {
    pkgdesc="Daemon which puts server into standby when it is idle. Common packages..."
    depends=()

install -Dm644 "$srcdir/powernap-$pkgver/actions/pm/00flag" "$pkgdir/etc/pm/power.d/00flag"
install -Dm644 "$srcdir/powernap-$pkgver/actions/pm/01cpu_online" "$pkgdir/etc/pm/power.d/01cpu_online"
install -Dm644 "$srcdir/powernap-$pkgver/actions/pm/cpu_frequency" "$pkgdir/etc/pm/power.d/cpu_frequency"
install -Dm644 "$srcdir/powernap-$pkgver/actions/pm/eth_speed" "$pkgdir/etc/pm/power.d/eth_speed"
install -Dm644 "$srcdir/powernap-$pkgver/actions/pm/kms_powermode" "$pkgdir/etc/pm/power.d/kms_powermode"
install -Dm644 "$srcdir/powernap-$pkgver/actions/pm/usb" "$pkgdir/etc/pm/power.d/usb"
install -Dm644 "$srcdir/powernap-$pkgver/actions/pm/usb_autosuspend" "$pkgdir/etc/pm/power.d/usb_autosuspend"
install -Dm644 "$srcdir/powernap-$pkgver/actions/pm/video" "$pkgdir/etc/pm/power.d/video"

install -Dm644 "$srcdir/powernap-$pkgver/actions/powernap/kernel_module" "$pkgdir/etc/powernap/actions/kernel_module"
install -Dm644 "$srcdir/powernap-$pkgver/actions/powernap/service" "$pkgdir/etc/powernap/actions/service"

install -Dm644 "$srcdir/powernap-$pkgver/powernap/monitors/__init__.py" "$pkgdir/usr/lib/python3.4/site-packages/powernap/__init__.py"
install -Dm644 "$srcdir/powernap-$pkgver/powernap/monitors/ConsoleMonitor.py" "$pkgdir/usr/lib/python3.4/site-packages/powernap/monitors/ConsoleMonitor.py"
install -Dm644 "$srcdir/powernap-$pkgver/powernap/monitors/DiskMonitor.py" "$pkgdir/usr/lib/python3.4/site-packages/powernap/monitors/DiskMonitor.py"
install -Dm644 "$srcdir/powernap-$pkgver/powernap/monitors/IOMonitor.py" "$pkgdir/usr/lib/python3.4/site-packages/powernap/monitors/IOMonitor.py"
install -Dm644 "$srcdir/powernap-$pkgver/powernap/monitors/InputMonitor.py" "$pkgdir/usr/lib/python3.4/site-packages/powernap/monitors/InputMonitor.py"
install -Dm644 "$srcdir/powernap-$pkgver/powernap/monitors/LoadMonitor.py" "$pkgdir/usr/lib/python3.4/site-packages/powernap/monitors/LoadMonitor.py"
install -Dm644 "$srcdir/powernap-$pkgver/powernap/monitors/Monitor.py" "$pkgdir/usr/lib/python3.4/site-packages/powernap/monitors/Monitor.py"
install -Dm644 "$srcdir/powernap-$pkgver/powernap/monitors/ProcessMonitor.py" "$pkgdir/usr/lib/python3.4/site-packages/powernap/monitors/ProcessMonitor.py"
install -Dm644 "$srcdir/powernap-$pkgver/powernap/monitors/TCPMonitor.py" "$pkgdir/usr/lib/python3.4/site-packages/powernap/monitors/TCPMonitor.py"
install -Dm644 "$srcdir/powernap-$pkgver/powernap/monitors/UDPMonitor.py" "$pkgdir/usr/lib/python3.4/site-packages/powernap/monitors/UDPMonitor.py"
install -Dm644 "$srcdir/powernap-$pkgver/powernap/monitors/WoLMonitor.py" "$pkgdir/usr/lib/python3.4/site-packages/powernap/monitors/WoLMonitor.py"
install -Dm644 "$srcdir/powernap-$pkgver/powernap/monitors/__init__.py" "$pkgdir/usr/lib/python3.4/site-packages/powernap/monitors/__init__.py"
install -Dm644 "$srcdir/powernap-$pkgver/powernap/powernap.py" "$pkgdir/usr/lib/python3.4/site-packages/powernap/powernap.py"
install -Dm644 "$srcdir/powernap-$pkgver/powernap/__init__.py" "$pkgdir/usr/lib/python3.4/site-packages/powernap/__init__.py"
}

package_powernap_server() {
    pkgdesc="Daemon which puts server into standby when it is idle. Server packages..."
    depends=()
    backup=('etc/powernap/config'
            'etc/powernap/action')
install -Dm644 "$srcdir/powernap-$pkgver/etc/systemd/system/powernapd.service" "$pkgdir/etc/systemd/system/powernapd.service"
install -Dm644 "$srcdir/powernap.conf" "$pkgdir/etc/init/powernap.conf"
install -Dm755 "$srcdir/powernap-$pkgver/action" "$pkgdir/etc/powernap/action"
install -Dm644 "$srcdir/powernap-$pkgver/config" "$pkgdir/etc/powernap/config"
install -Dm744 "$srcdir/powernap-$pkgver/bin/powernap_calculator" "$pkgdir/usr/bin/powernap_calculator"
install -Dm755 "$srcdir/powernap-$pkgver/sbin/powernap" "$pkgdir/usr/sbin/powernap"
install -Dm755 "$srcdir/powernap-$pkgver/sbin/powernap-action" "$pkgdir/usr/sbin/powernap-action"
install -Dm755 "$srcdir/powernap-$pkgver/sbin/powernap-now" "$pkgdir/usr/sbin/powernap-now"
install -Dm755 "$srcdir/powernap-$pkgver/sbin/powernapd" "$pkgdir/usr/sbin/powernapd"
install -Dm755 "$srcdir/powernap-$pkgver/sbin/powerwake-now" "$pkgdir/usr/sbin/powerwake-now"
install -Dm644 "$srcdir/powernap-$pkgver/man/powernap_calculator.1" "$pkgdir/usr/share/man/man1/powernap_calculator.1"
install -Dm644 "$srcdir/powernap-$pkgver/man/powernap-action.8" "$pkgdir/usr/share/man/man8/powernap-action.8"
install -Dm644 "$srcdir/powernap-$pkgver/man/powernap-now.8" "$pkgdir/usr/share/man/man8/powernap-now.8"
install -Dm644 "$srcdir/powernap-$pkgver/man/powernap.8" "$pkgdir/usr/share/man/man8/powernap.8"
install -Dm644 "$srcdir/powernap-$pkgver/man/powernapd.8" "$pkgdir/usr/share/man/man8/powernapd.8"
install -Dm644 "$srcdir/powernap-$pkgver/man/powerwake-now.8" "$pkgdir/usr/share/man/man8/powerwake-now.8"
install -Dm644 "$srcdir/powernap-$pkgver/config" "$pkgdir/usr/share/powernap/config"
}