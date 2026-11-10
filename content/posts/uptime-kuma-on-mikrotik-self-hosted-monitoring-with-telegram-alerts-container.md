---
title: "Uptime Kuma on MikroTik: Self-Hosted Monitoring with Telegram Alerts (Container Setup) 🔥"
date: 2025-11-09
slug: uptime-kuma-on-mikrotik-self-hosted-monitoring-with-telegram-alerts-container
categories: ["MikroTik", "Youtube Videos"]
youtube_id: EbeIQxGbxzY
description: "In this step-by-step tutorial, you'll learn how to run Uptime Kuma container on MikroTik Router! We will use the MikroTik Container package to host Uptime Kuma—a powerful, free, and self-hosted monitoring tool—directly on your MikroTik RouterOS device."
---

If you run services for yourself or for other people, you need to know the moment one of them goes down. Not an hour later, when someone calls you. Right away, on your phone.

Uptime Kuma does that. It is a free, open-source, self-hosted monitoring tool, and it runs as a container right on a MikroTik router. In this lab I run it on a MikroTik CHR on a cloud server, wire it to Telegram, and test it by faking an outage with a firewall rule.

## What We Are Building

- **Uptime Kuma in a RouterOS container**, on its own bridge network, with internet access.
- **Public access to the dashboard** through a destination NAT rule, then secured with a Cloudflare domain and HTTPS.
- **Telegram alerts** through a bot, so a downtime message lands in a Telegram group.
- **A ping monitor** on 8.8.8.8, checked every 20 seconds, and a fake outage to prove the alert works.

## Before You Start

The container package only runs on three CPU architectures: ARM, ARM64, and x86. My CHR is x86, so it works. Check yours in System, then Resources, before you start.

You also need the container package installed and turned on. Check System, then Packages, for the container package. Then run this in the terminal to confirm it is active:

```
/system/device-mode/print
```

The output should show that the container feature is already activated. If it is not, enable it first. My CHR already had it on, and there is no difference between a CHR and a physical router for this setup, so you can follow along on either one.

One more warning from the MikroTik manual, worth reading before you run a container: once the container feature is on, containers can be added and started remotely, and a router is only as secure as what you run inside a container. Only run images you trust.

## Step 1: Build the Container Network

Create a new bridge for the containers. I named mine bridge-1. Give it a private address:

```
/ip/address
add address=172.17.0.1/24 interface=bridge-1
```

Then create a VETH interface for the Uptime Kuma container, with its own address and the bridge address as its gateway:

```
/interface/veth
add name=veth-uptime address=172.17.0.10/24 gateway=172.17.0.1
```

Add the VETH to the bridge:

```
/interface/bridge/port
add bridge=bridge-1 interface=veth-uptime
```

Last, give the containers internet access with a masquerade rule. The source is the container network, and the out-interface is ether1, my WAN interface:

```
/ip/firewall/nat
add chain=srcnat action=masquerade src-address=172.17.0.0/24 out-interface=ether1
```

Expected result: the bridge, the VETH, and the NAT rule are all in place, and the container network can reach the internet.

## Step 2: Point RouterOS at Docker Hub

Go to Containers, then Config. Set the registry URL to Docker Hub:

```
https://registry-1.docker.io
```

It is free to use. Also set a temporary directory for the image layers. That is all the container config needs.

## Step 3: Create the Environment and the Mount

Uptime Kuma keeps its data in `/app/data` inside the container, and it listens on port 3001. The image name, from the Uptime Kuma docs, is `louislam/uptime-kuma`.

First, the environment list. Create one called uptime-kuma-env, with the key `TZ` and the value `Asia/Tehran`. Use your own time zone.

Then the mount. Create one called uptime-kuma-data. The source is a directory with the same name, which RouterOS creates on its own after the container runs. The destination is `/app/data` inside the container.

Expected result: the env list and the mount are both saved and ready to attach.

## Step 4: Create and Start the Container

Create the container with the image, the VETH interface, the mount, and the env list. Turn on logging and start-on-boot, then apply. RouterOS pulls the image layers from Docker Hub. The import takes a few seconds, and the container shows as stopped.

Start it. The first time, it failed. The container log showed a permission error for the data directory inside the container. It did not look like a serious error, so I did not debug it further. I copied the container, removed the old one, and started the copy. This time it came up, and the log said it was up and listening on port 3001.

That is a normal container story. The first start fails, the fix is boring, and the second start works. I am writing it down because pretending labs always work on the first try helps nobody.

Expected result: the container status is running, and the log says it listens on port 3001.

## Step 5: Open the Dashboard

The container runs on 172.17.0.10:3001, but nothing can reach it from outside yet. Add a destination NAT rule: chain dstnat, in-interface ether1, protocol TCP, destination port 80, action dst-nat to 172.17.0.10 port 3001.

This only works because I had already moved the router's own HTTP service off port 80, to port 808. If your router's web service still sits on port 80, the rule will fight with it.

Open the router's public IP in a browser. The first try showed the MikroTik login page instead of Uptime Kuma. That was a stale connection. I killed all the connections in IP, then Firewall, then the Connections tab, and opened the page again in a new private tab. This time Uptime Kuma loaded, and I could pick a language and set a username and password for the first login.

Expected result: the Uptime Kuma first-run page loads, and you can create the admin account.

## Step 6: Put It Behind HTTPS

The connection over the raw public IP is not secure. So I made an A record in Cloudflare for the CHR's public IP, with the proxy turned on. After the DNS record was created, I opened the domain in a fresh browser, and the connection was secure.

Log in, and the dashboard is there. Monitors sit on the left, details on the right. You can also make status pages, so people without a login can see the monitors that matter for your business. In Settings you can change the time zone, the look, light, dark, or auto, and the heartbeat bar position. I keep the bar at the bottom.

## Step 7: Connect Telegram

Uptime Kuma supports a long list of notification services. Discord, LINE, Matrix, and many more are all there. I tested it with Telegram because it is simple to connect.

First, make a bot. Open BotFather in Telegram, ask it to create a new bot, give the bot a name, and copy the token it gives you. Then create a Telegram group, add the bot to it, and find the group's chat ID in the browser. Paste the token and the chat ID into Uptime Kuma, name the notification, and press Test.

A test message arrived in the group right away. I set this notification as the default and saved it.

Expected result: the test notification shows up in your Telegram group.

## Step 8: Create a Monitor and Fake an Outage

Uptime Kuma can monitor HTTP, TCP, Ping, DNS, and more. For this test I used Ping. I named the monitor Google DNS, set the hostname to 8.8.8.8, and set the interval to 20 seconds, which is the fastest it allows. I attached the Telegram notification we just made.

Every 20 seconds it pings the address. Green means up, and the dashboard shows the ping time and the uptime. The monitor showed 100% uptime. I cloned it to make a second monitor for 4.2.2.4, named Level 3 DNS, and both showed as up.

Now the real test. Google DNS is always up, so I faked the outage. In IP, then Firewall, then the Filter tab, I added a rule: chain forward, destination address 8.8.8.8, action drop.

At the next check, the monitor went down, and a few seconds later the Telegram group got a message: Google DNS is down. Then I disabled the rule. At the next check the monitor came back, and Telegram got a second message: Google DNS is up.

Expected result: one Telegram message for the outage, one for the recovery, and a gap in the monitor's history where the firewall blocked the pings.

## One Limitation I Found While Testing

The first container start failed on a permission error, and the only fix I tried was to recreate the container. That worked, but I never found the root cause. If it happens to you, recreating the container is the fast fix. If it keeps happening, check the mount and the data directory before you look anywhere else.

Also, this whole setup puts a monitoring dashboard on the public internet. The Cloudflare proxy gives you HTTPS, but it does not give you a login wall in front of the dashboard. Uptime Kuma's own login is the only gate. Keep the password strong, and think twice before you publish the dashboard address anywhere.

## Final Thoughts

This is a strong use for the container package. A router that already sits at the edge of your network, already on all the time, now watches your services and tells you the second one of them drops. The Telegram part took a few minutes, and the fake outage proved the whole chain works, from the ping to the phone.

It is not a replacement for a full monitoring stack. It watches from one place, your router, and if the router itself goes down, it cannot tell you about it. But for watching your websites, your DNS, and your internal devices, and for getting the alert on your phone fast, it is simple, free, and it works.

### Official Documentation

- [Uptime Kuma on GitHub](https://github.com/louislam/uptime-kuma)
- [MikroTik Container Documentation](https://manual.mikrotik.com/docs/containers)
