---
title: "MikroTik CMR: Manage All Your Routers from One Dashboard"
date: 2026-10-20
slug: mikrotik-cmr-manage-all-your-routers-from-one-dashboard
categories: ["MikroTik", "Youtube Videos"]
youtube_id: 5Te5-Uo5u1Y
description: "Manage multiple MikroTik routers from one dashboard using MikroTik CMR (Centralized Management for RouterOS). In this hands-on tutorial, I'll show you how to set up a CMR controller, connect MikroTik routers as clients, and manage your RouterOS devices through a centralized interface."
---

You have three, five, or maybe ten MikroTik routers. Each time you want to upgrade them or change a setting, you log in to each one, one by one. That gets old fast.

MikroTik CMR fixes exactly that. It is the centralized management platform for RouterOS, introduced in RouterOS 7.26. You make one of your routers the controller, connect the rest as clients, and manage the whole fleet from one dashboard.

In this lab, I set up a CMR controller on a cloud CHR, connect three more routers to it, two of them behind CGNAT with no public IP, and walk through what the controller can do.

## What CMR Does

From the controller, you get:

- **Monitoring.** Every device, its version, CPU, memory, and disk usage, and which apps use traffic.
- **Updates.** Upgrade 10 or 50 devices with one rule, on a schedule, instead of logging in to each one.
- **Alerts.** If a router CPU gets too high, a device goes offline, or an upgrade fails, the controller tells you in the log, with a script, or with a webhook.
- **Wi-Fi and VLANs.** Push an SSID or a VLAN to many devices from one place.
- **Script tool.** Run a RouterOS command on the whole fleet at once, or on part of it.
- **Topology map.** CMR can draw your network map. I skip that part here, because it did not work in my test.

## How It Works

There are two roles: server and client. The server is a normal MikroTik router with one extra package, the CMR package. The clients run the CMR client, already inside RouterOS. You only need to upgrade them to RouterOS 7.26 or later. Nothing to install.

The server package only runs on ARM, ARM64, and x86. A CCR, an RB4011, or a CHR works fine. An older router like the RB951 with a MIPSBE CPU cannot be a server. For clients, almost every device works except SMIPS and PowerPC.

Clients find the server three ways: MNDP neighbor discovery on a shared LAN, DNS, or the server IP typed in the settings. They talk over TCP port 54321, so that port needs to be open on the server firewall.

Only the client connects to the server. The server never connects back. So a client can sit behind ISP CGNAT in a branch office or another city, with no public IP at all, and it still works. The server needs a public IP if the clients reach it over the WAN. On a LAN, it does not need one.

CMR menus need WinBox 4. WebFig works too. WinBox 3 does not show them.

One honest note about timing: at the time of recording, CMR was an experimental feature in RouterOS 7.26 beta 1. Beta 3 came out the same day, but I stayed on beta 1 for the lab. If you watch this later, CMR may have reached the stable channel by then. Either way, the steps still apply. Beta software has bugs, and this video catches a few of them.

## The Lab

My setup has four devices. A MikroTik CHR on a cloud server, with a public IP, acts as the CMR server. A second CHR acts as a client. In my home office, a hAP ax lite with an ARM CPU and an RB951 with a MIPSBE CPU act as clients, both behind my ISP CGNAT with no public IP.

All four run RouterOS 7.26 beta 1.

## Step 1: Install and Enable the Server

On the CHR that will be the server, go to System, then Packages. Select the CMR package and click Enable, then Apply changes. The router reboots, and the package is installed.

After that, the new CMR menus sit under Controller on the left, and the traditional menus sit under System. You can hide or unhide either group.

The CMR package is not enabled by default. In IP, then Services, the port is not exposed yet. Enable it from the settings, or from the terminal:

```
/cmr set enabled=yes
```

After that, the port is exposed. If you run firewall rules on this router, allow TCP 54321 in, so clients can connect. To disable it again, run `/cmr set enabled=no`.

Expected result: the server is up, the port is open, and the CMR menus are visible in WinBox 4.

## Step 2: Server Settings

Before connecting clients, look at the settings.

**Controller addresses.** This is the IP the server hands to clients that cannot find it themselves. I skipped it: my clients sit across a routed network and enter the server public IP directly.

**Track topology.** Enabled by default. It pulls routes, registration info, and neighbor discovery data from the clients so the server can build the network map.

**App traffic devices.** This picks which devices report application traffic. I set it to all.

**Pairing requirement.** This is the important one. The default is confirm, and the options are none and password. With none, a client is accepted automatically. That is fine for a lab, but for production I suggest confirm or password. With password, the client has to enter a RouterOS username and password of the server. I set it to password.

More settings cover the package directory for upgrade packages and the interval for checking client updates. I left those at their defaults.

Click Apply. The server is ready.

## Step 3: Connect the Clients

Start with the RB951. It has a MIPSBE CPU, so there is no CMR package in its package list. That is fine: the client is built in. Go to System, then CMR Client, and enable it.

Two things to know. If you disable a paired client, all the configuration the server injected is removed. To get it back, re-enable the client and reconnect. Also, the controller address is optional on a LAN, because MNDP discovery finds the server. Across a routed network, enter the server public IP.

The pairing requirement on the client is password or none, and the default is password: one side has to enter the other side's RouterOS credentials. The client status shows searching first, then waiting for pairing, then paired and connected. If it stays on searching, something is wrong with connectivity, or the port is closed on the server side.

I paired the RB951 from the client side, entering the server admin username and password. One small bug showed up here: the password field displayed the password in plain text instead of asterisks. I expect MikroTik to fix that in a later version.

The hAP ax lite paired the other way: I enabled its client, entered the server public IP, and accepted it from the server side. For that, I created a user called `test` on the client first, then ran Pair on the server with that username and password. Both home routers share the same public IP behind CGNAT, and that caused no problem.

The second CHR was the stubborn one. Pairing from the server side failed again and again, even though the ping between the two routers worked fine. I removed the device and paired it again, then disabled the client and enabled it again. Same result. Then I paired it from the client side with the server credentials, and it connected at once. I do not know what was wrong with the server-side attempt. Beta software, again.

After that, all four devices were paired and connected. I renamed them from the server so I could tell them apart, and renaming from the server changes the identity on the device itself.

Expected result: four devices in the list, all paired and connected, with board, version, IP, and uptime visible.

## Step 4: Labels and the Device List

The device window has two tabs. Devices shows the board, IP, labels, current RouterOS version, available version, pairing status, and uptime. Resources shows CPU, memory, and disk usage for each device.

One odd detail: the available version column offered me a downgrade instead of an upgrade on the beta devices, because it follows the stable channel. That is expected when the device runs a testing build.

Labels are how you group devices. I created a label called `home` and gave it to the two home-office routers. If you manage routers for several clients on one CMR server, labels let you group by client or by site.

## Step 5: Reboot, Upgrade, and Run Commands

The tools sit on the right of the device window.

**Reboot.** Select all, a label, or single devices. Note that all includes the CMR server itself, so pick carefully.

**Upgrade.** Pick the devices, the version (available, or manual with a channel like stable or long-term), and a schedule. The strategy is parallel, all at once, or sequential, one after the other. There is a fail policy for what happens when one device fails, and you can add packages to the upgrade. Upgrade rules work the same way: a default rule upgrades all devices to the stable channel, and you can create your own and watch the jobs and logs.

**Script tool.** Pick the devices, type RouterOS commands, and they run on each one. I kept it simple and rebooted the two home routers:

```
/system reboot
```

Both rebooted from the controller: one command, many routers.

## Step 6: Dashboard and Alerts

The dashboard shows a live summary: how many devices are online, a resources table, and a bandwidth graph. The blue line is download and the green line is upload. One bug here: changing the device selection did not change the graph. I could not get it to show a different router, so I skipped it.

The dashboard also shows active alerts and available updates. The traffic section shows application traffic from the reporting devices. One gap: there is no way to pick a single router in that view.

Alerts come from templates. There are eight of them, all disabled by default. Open one, make a copy, and customize it. I copied the memory template and set it to fire when memory goes above 60 percent on the home label, with high severity.

The actions are flexible: write a log message with the CMR topic at warning level, run a script, or call an HTTP URL. That last one hooks alerts into another system, so a notification lands on Telegram or WhatsApp.

I enabled the rule, and it fired at once: one of the two home devices was above 60 percent memory. The dashboard showed the alert, and the log had the entry.

The ports window is a plain report: per-interface rate, PVID, TX and RX, and PoE state where the port supports it.

## Step 7: Wi-Fi, VLANs, and What Did Not Work

The Wi-Fi and VLAN sections push configuration to the clients. One thing to understand first: CMR does not remove configuration already on the routers. It adds its own next to it. To change something that already exists, inject the commands through the script tool.

In the Wi-Fi window, the interfaces on my home routers are listed: the hAP ax lite on AX, and the older RB951, with MAC address, mode, channel, and SSID. I created a rule for the home label: a new SSID called `CMR SSID`, access point mode, WPA PSK security with TKIP encryption, and a passphrase. Then a radio rule with the country set to United Kingdom, plus chains and antenna gain.

It did not apply, and there was no log entry explaining why. Most likely I skipped a required field, or it is another beta bug.

The topology map is the other thing I skipped. I tested it before recording, and it did not work.

## Final Thoughts

CMR is the feature a lot of MikroTik users have waited for, and it is finally here. One controller, one dashboard, and the boring fleet work, upgrades, reboots, alerts, and the same command on ten routers, happens from one place.

It is still young. In one lab session I hit a plain-text password field, a pairing that only worked from one side, a bandwidth graph that would not switch devices, a Wi-Fi rule that never applied, and a topology map that did not draw. None of that makes it useless.

If you manage more than a couple of routers, set up a lab controller and try it. Start with monitoring and upgrades, add one alert, and keep the production fleet on confirm or password pairing.

## Official Documentation

- [CMR — MikroTik Manual](https://manual.mikrotik.com/docs/management-tools/cmr/)
- [Management Tools — MikroTik Manual](https://manual.mikrotik.com/docs/management-tools/)
