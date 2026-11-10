---
title: "WireGuard on OpenWrt: Route Everything Through a VPN Tunnel 🔐"
date: 2026-02-23
slug: wireguard-on-openwrt-route-everything-through-a-vpn-tunnel
categories: ["OpenWrt", "VPN", "Youtube Videos"]
youtube_id: MG6PI4KQpoA
description: "In this OpenWrt tutorial, I show you how to set up a high-performance WireGuard VPN and configure your router to route all outbound internet traffic through a secure tunnel."
---

A VPN app on one laptop protects one laptop. A VPN tunnel on your router protects every device in the house at once: the phones, the TV, the laptop, all of it, with no app to install on any of them.

That is what this lab does. I set up WireGuard on OpenWrt, on a Xiaomi Mi 4A Gigabit Edition, and routed all outbound traffic from the LAN through the tunnel. There are two ways to do it: the manual way, where you fill in every field yourself, and the fast import way, where you paste in a config file and OpenWrt fills the fields for you.

## What We Are Building

- **A hardened OpenWrt router**: root password set, Wi-Fi on, LAN address changed so it cannot clash with another network.
- **A WireGuard tunnel** to a VPN server, built by hand first so you see what each field does.
- **The same tunnel built again by import**, in seconds, from a config file.
- **A working check** at each step: the public IP moves from Singapore to Frankfurt, Germany.
- **Three performance tweaks at the end**: MTU, software flow offloading, and the kill switch idea.

## Before You Start

You need a WireGuard config file. I run my own WireGuard server on a personal server, and I used its client config. You can use any config your provider gives you. NordVPN, ExpressVPN, and Windscribe all hand out WireGuard configs, and any of them works the same way here.

You also need a router running OpenWrt. Mine is the budget Xiaomi Mi 4A Gigabit Edition, running OpenWrt 24.10, which was the latest stable version when I recorded this. The steps are the same on any router running OpenWrt. The interface and the logic never change.

## Step 1: Harden the Fresh Install

I installed OpenWrt fresh, so the config is default. I connected the router to my laptop with a LAN cable, because the Wi-Fi interfaces in OpenWrt are disabled by default and need to be turned on.

Open the LuCI web console at 192.168.1.1. Log in as root. There is no password by default.

First, set a root password. Go to System, then Administration, set a strong password, and save.

Next, turn on Wi-Fi. Go to Network, then Wireless. My router has two Wi-Fi interfaces. I turned on only the first one, the 2.4 GHz interface, for this demo. I changed the SSID to OpenWrt-2G, picked an encryption method, and set a strong Wi-Fi password. Save and apply.

Then change the LAN address. The default 192.168.1.1 clashes with a lot of home networks, so I changed it to 192.168.123.1. Go to Network, then Interfaces, click Edit on the LAN interface, and change the address. If you do not use IPv6 on your network, you can delete the WAN6 interface the same way I did. Save and apply, wait a few seconds, and your laptop gets a new address from the router.

I checked it on my Mac with:

```
ifconfig | grep 192
```

The new address was there. Then I opened the console again at the new address, 192.168.123.1, and logged in with the root password.

Expected result: root has a password, Wi-Fi is on, and the router answers at its new LAN address.

## Step 2: Test the WireGuard Config on Your PC First

Before touching the router, test the config where it is easy to see. I opened iplocation.com, and my public IP was in Singapore. Then I opened the WireGuard app on my laptop, imported the config, and activated it. The sent and received counters started moving, which means the tunnel was up. I opened iplocation.com again, and my new public IP was in Frankfurt, Germany.

The config works. Now I know that any problem on the router is a router problem, not a bad config.

A WireGuard config file has two parts. The first part is the Interface section, our side of the tunnel: the private key and the tunnel IP address. The second part is the Peer section, the server side: the public key, the allowed IPs, and the endpoint. We need both parts for the router setup.

## Step 3: Install the WireGuard Package

Go to System, then Software. Click Update lists first, so the package list is fresh. Then search for wireguard. Install `luci-proto-wireguard`. LuCI is the OpenWrt web console, and this package adds the WireGuard protocol to it. Two more related packages came along with it as dependencies.

Then reboot the router once: System, then Reboot, then Perform reboot. Log back in with the root password.

Expected result: the WireGuard VPN protocol is available when you add a new interface.

## Step 4: Build the Tunnel by Hand

Go to Network, then Interfaces, and click Add new interface. Pick WireGuard VPN as the protocol and name the interface WG1. Click Create interface.

On the settings page, click Generate new key pair. That makes a private and a public key. But we need the private key from the config file, not a fresh one, so copy the private key from the config and paste it over the generated one. Then copy the tunnel IP address from the config file into the IP address field.

Leave the other fields at their defaults. Two things to check: the interface must not be disabled, and Bring up on boot must be checked, so the tunnel comes back up every time the router reboots.

In the Advanced Settings tab, set the DNS servers for the interface. I used the Cloudflare and Google public DNS servers.

In the Firewall Settings tab, assign the interface to the WAN zone. The WireGuard interface acts as a WAN interface, so that is where it belongs.

Then the peer. Click Add peer. Make sure it is not disabled. Copy the peer's public key from the config file and paste it in. Copy the Allowed IPs from the config file too. My config has no pre-shared key, so I left that field empty. If your provider gave you a pre-shared key, paste it here.

For the endpoint, copy the server's IP address into the endpoint host field, without the port, and put the port number in the endpoint port field.

Last, and this is the step people miss: check Route Allowed IPs. If you do not check it, your LAN traffic will not go through the WireGuard tunnel.

Click Save, then Save and apply. After a few seconds, the TX and RX counters start moving. That is the handshake, and the tunnel is up.

To prove it, I turned off the WireGuard client on my laptop, so the laptop's traffic had to go through the router, and opened iplocation.com again. The public IP was Frankfurt, Germany. Every device on the LAN now goes out through the tunnel.

Expected result: TX and RX are counting, and your public IP is the server's location.

## Step 5: Build the Same Tunnel by Import

The manual way teaches you what is under the hood. But if you want it done in seconds, there is a faster way.

Delete the WG1 interface first, so we start clean. Then add a new interface again, protocol WireGuard VPN, and name it WG2. This time, click Load configuration. Paste your WireGuard config into the field, or drag and drop the config file, and click Import settings.

Every field fills itself: the IP address, the private key, both DNS servers, and the peer settings. Two things still need your hand. In the Firewall Settings tab, select the WAN zone yourself. And on the peer, check Route Allowed IPs yourself. The import does not set those two.

Save, save again, and save and apply. After a few seconds the RX and TX counters are moving. Open iplocation.com in a private tab, and the public IP is Frankfurt, Germany again.

Expected result: the same tunnel, the same Frankfurt IP, built in seconds instead of minutes.

## Three Tweaks Worth Knowing

**MTU.** The default tunnel MTU is 1420. If your ISP uses PPPoE, drop it to 1412. The symptom of a wrong MTU is easy to spot: websites load halfway, or sessions hang, because packets fragment. You change it in the Advanced Settings tab of the interface.

**Software flow offloading.** Go to the firewall settings, find the Routing/NAT Offloading section, and turn on software flow offloading. It lowers the CPU cost of routing established flows, which frees up processing power for WireGuard's encryption and lifts your throughput. One warning: if you use SQM or QoS to manage latency, leave offloading off. The two do not work well together.

**The kill switch.** This one I did not set up in this video, only the idea. If your LAN zone is only allowed to forward traffic to the WireGuard zone, then nothing leaks out on the plain internet if the tunnel ever drops. That is what a kill switch is. If you want a full video on building one on OpenWrt, tell me in the comments.

The Mi 4A is a budget, entry-level router, and it is not a powerhouse. That is exactly why WireGuard fits it. Heavier protocols like OpenVPN can struggle on modest hardware. WireGuard is light, so a small router can run an encrypted tunnel without maxing out its CPU. If you are buying a new router for OpenWrt, I recommend one with an ARM CPU.

## Final Thoughts

The import method is the one you will use day to day. But build it by hand once first. When the tunnel breaks at some point, and it will, the hand-built version is what lets you look at the fields and know which one is wrong.

The whole point of this setup is simple. One tunnel on the router, and every device behind it is covered. No app per device, no per-device config, and the check is one page: iplocation.com, before and after.

### Official Documentation

- [WireGuard — Fast, Modern, Secure VPN Tunnel](https://www.wireguard.com/)
