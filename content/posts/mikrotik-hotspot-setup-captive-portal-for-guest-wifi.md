---
title: "MikroTik Hotspot Setup: Captive Portal for Guest Wi-Fi"
date: 2026-11-27
slug: mikrotik-hotspot-setup-captive-portal-for-guest-wifi
categories: ["MikroTik", "Youtube Videos"]
youtube_id: qiIFvBpTU_E
description: "Set up a MikroTik Hotspot from scratch with the Setup wizard: open Wi-Fi, a login page, and internet only after login. Tested from a phone, with the WinBox steps and the checks that prove it works."
---

Wi-Fi in a hotel or a cafe works a certain way: the network is open, anyone can join it, and then a login page asks for a username and password. Nobody gets internet before logging in, and the owner always knows who is connected. That is a captive portal, and on a MikroTik router it is a built-in feature called Hotspot.

This guide builds one from scratch. The router starts with no configuration at all. By the end it hands out guest Wi-Fi with a login page, and a phone test proves the gate works: no internet before login, full internet after. Every step follows the video, in WinBox, with the Hotspot Setup wizard doing the heavy work.

## Your Values

Every step below uses example values from the video. Replace them with your own — the steps are identical.

- Router: a MikroTik with a built-in Wi-Fi interface (in the video, a hAP ax lite). Any RouterOS 7 router with Wi-Fi works the same way.
- WAN: ether1, connected to the home router, getting its address by DHCP.
- Hotspot interface: wifi1.
- Hotspot network: the /24 network the wizard suggests for wifi1.
- DNS: Google 8.8.8.8 as primary, Cloudflare 1.1.1.1 as secondary.
- Login page DNS name: ramtin.xyz.
- First Hotspot user: ramtin, with a simple demo password.

## Before You Start

You need a MikroTik router running RouterOS 7 with a Wi-Fi interface, WinBox on your PC, and an upstream network that hands out addresses by DHCP — in the video that is the home router. You also need a phone to test with, because the test is the whole point: the portal has to appear on a real device.

Two facts from the MikroTik manual matter before you start. HotSpot works with IPv4 only. And device-mode can block it, so check that hotspot is enabled under /system/device-mode first. One HotSpot server runs on one interface, so pick the interface your guests will use and keep it separate from your own network.

## Give the Router Internet

**Step 1 — Connect and set the admin password.** In WinBox, open Neighbors and connect to the router by its MAC address. A clean router logs in as admin with no password. Set a strong admin password first, then log back in with it. In the video I use a simple password for the demo — do not do that on a real network. Open the terminal and confirm the configuration is empty before going further.

**Step 2 — Add a DHCP client on ether1.** Open IP, then DHCP Client, and add a client on ether1, with Use Peer DNS on and Add Default Route set to yes. The upstream router hands the MikroTik an address. Check IP, then Routes: a default route through the upstream gateway should be there. Test it from the terminal: ping a public IP address, then ping a domain name to confirm DNS works too. Nothing else in this guide works until the router itself has internet.

## Run the Hotspot Setup Wizard

**Step 3 — Open IP, then Hotspot, and click Hotspot Setup.** Building a Hotspot by hand means configuring the interface, the address, the DHCP server, and the Hotspot itself one by one. The wizard does all of it in one pass, so this guide uses the wizard.

The wizard asks, in order: the Hotspot interface (wifi1 here — it has no SSID yet, and that is fine, the SSID comes later); the local address of the Hotspot network (the wizard suggests a /24 address on wifi1); masquerade network (yes — this adds the NAT rule that lets logged-in users reach the internet); the address pool for guest IPs (accept the suggested pool, it stays editable under IP, then Pool); the certificate (none, to keep it simple); the SMTP server (none here); the DNS servers (Google 8.8.8.8 first, Cloudflare 1.1.1.1 second); and a DNS name for the login page (ramtin.xyz in the video).

**Step 4 — Create the first Hotspot user.** The last wizard screen creates a user. The default name is admin; in the video I create a user called ramtin with a simple demo password. Click Next and the Hotspot exists.

## What the Wizard Created

Open IP, then Hotspot. The Servers tab shows hotspot1 on wifi1. The Server Profiles tab shows hsprof1 with the DNS name ramtin.xyz. The Users tab shows the user just created. Add a second user the same way if you need one.

The User Profiles tab holds the default profile, and the Active and Hosts tabs are empty for now — they fill up once a device connects, which is the next test. There are many more Hotspot settings behind these tabs. This guide skips them on purpose: the basic setup first, the advanced parts another time.

## Set the SSID

**Step 5 — Give the Wi-Fi a name.** Open Wi-Fi. The wifi1 interface is enabled but has no SSID, so guests cannot find it yet. Open the interface, go to the Configuration tab, and set the SSID, the country, the band (2 GHz AX here), and the channel width (20 MHz). The exact wireless settings depend on your router model — set what fits your hardware and click OK. The Hotspot network is now live.

## Test It from a Phone

**Step 6 — Connect and log in.** On the phone, search for Wi-Fi networks. The new SSID appears after a few seconds. Connect to it: there is no Wi-Fi password, and the phone gets an address from the Hotspot pool. A moment later the phone offers the login page — the default MikroTik Hotspot page.

Before logging in, test the gate: from the phone, ping the Cloudflare DNS address 1.1.1.1. There is no internet yet, which is exactly what a captive portal should do. Then log in with the Hotspot user and the password. Run the test again and the internet works.

**Step 7 — Check the result in WinBox.** Back in IP, then Hotspot, the Active tab shows the logged-in user with its IP address and uptime. The Hosts tab shows the phone's MAC address and IP, plus its RX and TX rates. Either entry can be removed from here — the user then has to log in again.

## Behind the Scenes: Pool and NAT

The wizard leaves two things worth knowing about. Under IP, then Pool, the Hotspot address pool sits ready to edit — change the range here if the default does not fit your network. Under IP, then Firewall, on the NAT tab, the masquerade rule the wizard created is what gives logged-in users internet access. It translates the Hotspot network's addresses to the router's own address on the way out. Do not delete it while the Hotspot runs.

## Honest Limits

This is the basic setup, and it shows. The login page is the MikroTik default — customizing it is a separate job, and I covered it in an earlier video, linked below. There are no time limits, no traffic limits, and no vouchers; every user is a plain local account on the router. The Wi-Fi network is open by design, so anyone in range can join it — the login page is the only gate, which is why strong Hotspot passwords matter. HotSpot is IPv4-only, and the manual notes that device-mode can block it. For a bigger setup — many users, time-limited access, or central management — the next step is a RADIUS server such as User Manager.

## Cleanup

To take the Hotspot down, remove the server under IP, then Hotspot, delete the users, and turn off the Wi-Fi interface or give it back its old SSID. To return the router to a clean state, reset the configuration from System, then Reset Configuration. The DHCP client on ether1 goes with the reset.

## Final Thoughts

A Hotspot is one of those RouterOS features that looks complex from the outside and turns out to be a wizard with nine questions. The value is not the wizard, though — it is the test. Connecting a real phone, watching the login page appear, and confirming that there is no internet before login and full internet after is what turns a configuration into a working guest network. From here the interesting work starts: a login page of your own, time limits, and RADIUS.

## Links

MikroTik HotSpot documentation: https://manual.mikrotik.com/docs/7.25/authentication-authorization-accounting/hotspot-captive-portal/

Custom login page video and guide: https://ramtin.zone/posts/how-to-customize-a-mikrotik-hotspot-login-page-with-ai-custom-login-template/
