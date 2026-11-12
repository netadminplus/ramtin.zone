---
title: "How to Run an OpenConnect VPN (ocserv) Container on MikroTik with Let's Encrypt"
date: 2026-11-12
slug: mikrotik-ocserv-openconnect-vpn-container
categories: ["MikroTik", "VPN"]
image: /assets/images/ocserv-openconnect-vpn-mikrotik-container.webp
description: "Run an OpenConnect VPN server as a container on MikroTik RouterOS 7, with a real Let's Encrypt certificate on port 443 and copy-paste commands for every step — networking, certificates, NAT, and user management."
---

If you want a VPN server on your router that works with any AnyConnect-compatible client, ocserv is the straightforward answer. It speaks the OpenConnect protocol, so Cisco Secure Client, the open-source client, and the mobile apps connect without anything special.

The catch with most ocserv guides is the certificate: a self-signed cert means a warning on every first connection and a CA to install on every device. This setup avoids that — the router gets a real Let's Encrypt certificate, and clients connect cleanly.

I run ocserv as a container on RouterOS 7, using my own image, `ramtiin/mikrotik-ocserv:1.0.0`. Here is what we build:

- A dedicated bridge and veth interface for the container (172.18.0.0/24)
- A Let's Encrypt certificate for your domain, issued by RouterOS itself
- The ocserv container, listening on TCP and UDP 443
- NAT rules and a VPN pool of 10.10.10.0/24, so clients reach the internet through your WAN

Every command block has a copy button. Paste the commands in order and check the expected result after each step. Validated on RouterOS 7.25.1.

## Before You Start

You need these in place before running any command:

- **RouterOS:** 7.12 or later (I validated this on 7.25.1)
- **Container package:** installed, and container mode enabled (`container: yes`)
- **Architecture:** amd64 / x86_64
- **RAM:** 512 MB minimum, and 500 MB free storage
- **Public IPv4:** assigned to your WAN interface (ether1 in this guide)
- **DNS:** an A record pointing your VPN hostname to the router's WAN IP, DNS-only, no proxy
- **Ports:** TCP and UDP 443 open to the internet, and TCP 80 reachable for the ACME challenge

One thing up front: your firewall filter policy must allow inbound TCP/UDP 443 and forwarded traffic to the container subnet. Firewall filter configuration is not covered here.

Check the starting state first:

```routeros
/system resource print
/system package print where name=container
/system device-mode print
```

Expected: RouterOS 7.x, the container package present, and `container: yes`.

## Step 1 — Prepare RouterOS

Set the container storage paths and the clock — certificates and ACME both depend on correct time:

```routeros
/container config set layer-dir=/container-layers tmpdir=/container-tmp
/system ntp client set enabled=yes
/system ntp client servers add address=0.pool.ntp.org
/system ntp client servers add address=1.pool.ntp.org
```

Then confirm the clock is synchronized (wait up to 60 seconds):

```routeros
/system ntp client print
```

Expected: `status: synchronized`.

## Step 2 — Set Up the Container Network

The container gets its own bridge and veth interface — router side 172.18.0.1, container side 172.18.0.2 — plus a route for the VPN pool:

```routeros
/interface bridge add name=br-ocserv comment="ocserv-vpn"
/ip address add address=172.18.0.1/24 interface=br-ocserv comment="ocserv-vpn"
/interface veth add name=veth-ocserv address=172.18.0.2/24 gateway=172.18.0.1 gateway6="" comment="ocserv-vpn"
/interface bridge port add bridge=br-ocserv interface=veth-ocserv comment="ocserv-vpn"
/ip route add dst-address=10.10.10.0/24 gateway=172.18.0.2 comment="ocserv-vpn"
```

Every object carries the `ocserv-vpn` comment, so the whole setup is easy to find — and easy to remove later.

## Step 3 — Issue the Let's Encrypt Certificate

First, create the directories the container mounts:

```routeros
/file add name="ocserv" type=directory
/file add name="ocserv/config" type=directory
/file add name="ocserv/config/certs" type=directory
```

Before the next step, confirm your DNS record resolves to this router's WAN IP and the RouterOS HTTP service on port 80 is reachable from the internet — the ACME challenge needs both. Then issue the certificate, replacing `oc.ramtiin.ir` with your own hostname:

```routeros
/ip service enable www
/certificate add-acme name=oc.ramtiin.ir domain-names=oc.ramtiin.ir
```

Wait up to 60 seconds for the challenge, then check:

```routeros
/certificate print detail where name=oc.ramtiin.ir
```

Expected: `issuer=Let's Encrypt`, `days-valid=89`, flag `K` present, and an `acme-status` line. Then turn the HTTP service back off:

```routeros
/ip service disable www
```

## Step 4 — Export and Place the Certificate Files

The container needs the certificate and private key as files. Export them with a passphrase — pick a strong one and remember it, because the container reads it from a file next:

```routeros
/certificate export-certificate oc.ramtiin.ir export-passphrase=<KEY-PASSPHRASE>
```

Warning: a passphrase typed into a RouterOS command appears in the command history. Use a strong value, and consider changing it after setup.

Check the export produced both files:

```routeros
/file print where name~"cert_export"
```

Expected: `cert_export_oc.ramtiin.ir.crt` (the leaf certificate) and `cert_export_oc.ramtiin.ir.key` (the encrypted private key).

Move both into the mount directory, under the names the container expects:

```routeros
/file set [find name="cert_export_oc.ramtiin.ir.crt"] name="ocserv/config/certs/server.pem"
/file set [find name="cert_export_oc.ramtiin.ir.key"] name="ocserv/config/certs/server-key.pem"
```

Then create the passphrase file with the same passphrase:

```routeros
/file add name=key-pin.txt type=file contents="<KEY-PASSPHRASE>"
/file set [find name="key-pin.txt"] name="ocserv/config/certs/key-pin.txt"
```

Verify all three files are in place:

```routeros
/file print where name~"ocserv/config/certs"
```

Expected: `server.pem`, `server-key.pem`, and `key-pin.txt`.

## Step 5 — Configure the Container

Add the mount for the container's configuration directory:

```routeros
/container mounts add list=ocserv-config src=ocserv/config dst=/etc/ocserv
```

Then the environment variables — replace `<VPN-PASSWORD>` with your VPN users' password:

```routeros
/container envs add list=ocserv-env key=VPN_USER value=vpnuser comment="ocserv-vpn"
/container envs add list=ocserv-env key=VPN_PASS value=<VPN-PASSWORD> comment="ocserv-vpn"
/container envs add list=ocserv-env key=VPN_POOL value=10.10.10.0 comment="ocserv-vpn"
/container envs add list=ocserv-env key=VPN_MASK value=255.255.255.0 comment="ocserv-vpn"
/container envs add list=ocserv-env key=SERVER_CERT value=/etc/ocserv/certs/server.pem comment="ocserv-vpn"
/container envs add list=ocserv-env key=SERVER_KEY value=/etc/ocserv/certs/server-key.pem comment="ocserv-vpn"
/container envs add list=ocserv-env key=KEY_PIN_FILE value=/etc/ocserv/certs/key-pin.txt comment="ocserv-vpn"
```

Now add the container:

```routeros
/container add remote-image=ramtiin/mikrotik-ocserv:1.0.0 interface=veth-ocserv root-dir=/container-layers/ocserv envlists=ocserv-env mountlists=ocserv-config dns=8.8.8.8 hostname=ocserv-vpn privileged=yes logging=yes start-on-boot=yes comment="ocserv-vpn"
```

Adding the container starts the download. The image is 91 MB, so allow 30–90 seconds. Watch the status change from `E` (extracting) to `S` (stopped) — do not start it yet:

```routeros
/container print
```

## Step 6 — Set Up NAT

NAT goes in before the first start — the container needs outbound internet access on its first run to fetch the intermediate certificate:

```routeros
/ip firewall nat add chain=dstnat in-interface=ether1 protocol=tcp dst-port=443 action=dst-nat to-addresses=172.18.0.2 to-ports=443 comment="ocserv-vpn"
/ip firewall nat add chain=dstnat in-interface=ether1 protocol=udp dst-port=443 action=dst-nat to-addresses=172.18.0.2 to-ports=443 comment="ocserv-vpn"
/ip firewall nat add chain=srcnat out-interface=ether1 src-address=172.18.0.0/24 action=masquerade comment="ocserv-vpn"
/ip firewall nat add chain=srcnat out-interface=ether1 src-address=10.10.10.0/24 action=masquerade comment="ocserv-vpn"
```

The first two rules forward VPN traffic to the container; the last two masquerade the container subnet and the VPN pool out through your WAN.

## Step 7 — Start the Container and Check the Logs

Confirm the image finished downloading (status `S`), then start:

```routeros
/container print
/container start [find comment="ocserv-vpn"]
```

Wait 15 seconds, then read the logs:

```routeros
/log print proplist=message where message~"ocserv"
```

On a fresh install, expect lines like these:

```
[ocserv] created user: vpnuser
[ocserv] cert has 1 cert — fetching intermediate
[ocserv] intermediate appended — chain is now complete
[ocserv] configuration written
[ocserv] starting...
listening (TCP) on 0.0.0.0:443...
listening (UDP) on 0.0.0.0:443...
sec-mod initialized
```

Two notes. If the log says `cert chain has 2 certs — OK` instead, that is also fine — the exported certificate already contained the full chain. And I want to be precise about `start-on-boot=yes`: it is set, but I have not tested it through a full reboot yet. Reboot and check `/container print` to confirm.

## Step 8 — Connect and Test

Check the certificate chain from the outside first, from a terminal on your computer:

```bash
openssl s_client -connect oc.ramtiin.ir:443 -showcerts </dev/null 2>&1 | grep -c "BEGIN CERTIFICATE"
```

Expected: `2` — the leaf and the intermediate.

```bash
openssl s_client -connect oc.ramtiin.ir:443 </dev/null 2>&1 | grep -E "subject=|issuer="
```

Expected: the issuer contains `Let's Encrypt`.

Then connect with Cisco Secure Client or any AnyConnect-compatible client:

- **Server:** oc.ramtiin.ir (your hostname)
- **Username:** vpnuser
- **Password:** the `<VPN-PASSWORD>` you set

While connected, verify the tunnel carries your traffic — your public IP should be the router's WAN IP:

```bash
curl -4 https://api.ipify.org
```

Check DNS resolution too:

```bash
nslookup google.com
```

Expected: it resolves via 8.8.8.8.

One honest note: I confirmed the TCP-based TLS tunnel working. DTLS over UDP 443 was not explicitly verified — the logs show the UDP listener active, and AnyConnect upgrades automatically when UDP 443 is reachable, but I did not test that path.

## Managing VPN Users

The first user comes from `VPN_USER` and `VPN_PASS`, and the container stores the credentials in `ocserv/config/ocpasswd` on the router. Later starts keep the file, so users survive restarts.

The limitation: you cannot add or change users interactively at runtime. The `ocpasswd` tool lives only inside the container, and RouterOS gives you no docker-exec-style way to run it. So user changes go through Docker on your computer.

One honest note: this flow is the documented procedure from my runbook — I have not run it against a live deployment yet.

Stop the container first, so nothing writes to the credential file while you edit it:

```routeros
/container stop [find comment="ocserv-vpn"]
```

Download the credential file (SSH on port 2212; replace the address with your router's WAN IP):

```bash
scp -P 2212 admin@<ROUTER-WAN-IP>:/ocserv/config/ocpasswd /tmp/ocpasswd
```

Add a user, or change an existing user's password — existing entries are preserved:

```bash
printf '<NEW-PASSWORD>\n<NEW-PASSWORD>\n' | \
  docker run --rm -i -v /tmp:/tmp ramtiin/mikrotik-ocserv:1.0.0 \
  ocpasswd -c /tmp/ocpasswd <USERNAME>
```

Delete a user:

```bash
docker run --rm -i -v /tmp:/tmp ramtiin/mikrotik-ocserv:1.0.0 \
  ocpasswd -c /tmp/ocpasswd -d <USERNAME>
```

Upload the file back, remove the local copy, and restart:

```bash
scp -P 2212 /tmp/ocpasswd admin@<ROUTER-WAN-IP>:/ocserv/config/ocpasswd
rm /tmp/ocpasswd
```

```routeros
/container start [find comment="ocserv-vpn"]
```

To start over with a single user, delete the credential file and restart — the container creates a fresh one from `VPN_USER` and `VPN_PASS`. Update the variables first if the username or password should change:

```routeros
/container stop [find comment="ocserv-vpn"]
/file remove [find name="ocserv/config/ocpasswd"]
/container envs set [find key=VPN_USER] value=<NEW-USERNAME>
/container envs set [find key=VPN_PASS] value=<NEW-PASSWORD>
/container start [find comment="ocserv-vpn"]
```

## Troubleshooting

**The intermediate certificate fetch fails on first start.** The container had no outbound internet access when it first started. Confirm the Step 6 NAT rules are in place, then restart:

```routeros
/container stop [find comment="ocserv-vpn"]
/container start [find comment="ocserv-vpn"]
```

If the fetch still fails, append the intermediate manually:

```bash
scp -P 2212 admin@<ROUTER-WAN-IP>:/ocserv/config/certs/server.pem /tmp/server.pem
LEAF=$(openssl x509 -in /tmp/server.pem -noout -text | grep "CA Issuers" | sed 's/.*URI://' | tr -d ' \r\n')
curl -s "$LEAF" | openssl x509 -inform DER >> /tmp/server.pem
scp -P 2212 /tmp/server.pem admin@<ROUTER-WAN-IP>:/ocserv/config/certs/server.pem
rm /tmp/server.pem
```

```routeros
/container start [find comment="ocserv-vpn"]
```

**AnyConnect keeps asking for the password.** Two causes. First, a wrong credential-file format:

```bash
scp -P 2212 admin@<ROUTER-WAN-IP>:/ocserv/config/ocpasswd ./check
grep -o ":" ./check | wc -l
```

Expected: `2` (three fields: `username:*:hash`). If the result is `1`, delete the file and restart — the image recreates it correctly. Second, an IP ban from repeated failed attempts: restart the container, or wait 20 minutes (ban resets after 1200 seconds).

**The container starts but ocserv does not listen.** Read the logs:

```routeros
/log print proplist=message where message~"ocserv"
```

`cannot open file` or `certificate not found` means the certificate files are missing from the mount — go back to Step 4. `could not fetch intermediate cert` means no internet access — see the first item above.

**The VPN connects, then drops immediately.** Remove any `no-route` entries from `ocserv.conf` — only `route = default` should be present.

## Certificate Renewal

RouterOS renews the certificate automatically, around day 71. After a renewal, the container needs the new files — automatic pushing has not been tested, so treat this as manual:

```routeros
/certificate export-certificate oc.ramtiin.ir export-passphrase=<KEY-PASSPHRASE>
/file set [find name="cert_export_oc.ramtiin.ir.crt"] name="ocserv/config/certs/server.pem"
/file set [find name="cert_export_oc.ramtiin.ir.key"] name="ocserv/config/certs/server-key.pem"
```

`key-pin.txt` only changes if the passphrase changes. Then restart:

```routeros
/container stop [find comment="ocserv-vpn"]
/container start [find comment="ocserv-vpn"]
```

## Cleanup

Every object carries the `ocserv-vpn` comment, so one block removes the whole setup:

```routeros
/container stop [find comment="ocserv-vpn"]
:delay 5s
/container remove [find comment="ocserv-vpn"]
/container mounts remove [find list=ocserv-config]
/container envs remove [find list=ocserv-env]
/interface bridge port remove [find comment="ocserv-vpn"]
/ip address remove [find comment="ocserv-vpn"]
/interface veth remove [find comment="ocserv-vpn"]
/interface bridge remove [find comment="ocserv-vpn"]
/ip route remove [find comment="ocserv-vpn"]
/ip firewall nat remove [find comment="ocserv-vpn"]
/certificate remove [find name=oc.ramtiin.ir]
/file remove [find name="ocserv/config/certs/server.pem"]
/file remove [find name="ocserv/config/certs/server-key.pem"]
/file remove [find name="ocserv/config/certs/key-pin.txt"]
/file remove [find name="ocserv/config/ocpasswd"]
/file remove [find name="ocserv/config/ocserv.conf"]
/ip service disable www
```

## Final Thoughts

This is the VPN setup I wanted on my own router: a real certificate, a standard protocol every client already speaks, and no separate server to maintain.

The honest limits are the ones I flagged: `start-on-boot` untested through a reboot, DTLS not verified directly, and the Docker user-management flow documented but not yet run live. None of those change the core setup — but I would rather state them than let you discover them.

If you hit something outside the troubleshooting section, drop it in the comments — someone else has probably hit the same wall.

## References

- [MikroTik Container documentation](https://manual.mikrotik.com/docs/containers/)
- [ocserv manual — ocserv(8)](https://ocserv.openconnect-vpn.net/ocserv.8.html)
