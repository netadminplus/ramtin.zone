---
title: "MikroTik Back To Home: VPN Server WITHOUT Public IP (Easiest WireGuard VPN Setup Ever) 🔥"
date: 2025-11-13
slug: mikrotik-back-to-home-vpn-server-without-public-ip-easiest-wireguard-vpn-setup
categories: ["MikroTik", "VPN", "Youtube Videos"]
youtube_id: CRLUQgU1_Xs
description: "In this essential MikroTik tutorial, you'll learn how to set up your own Remote Access VPN Server that works perfectly without a Public IP Address—the definitive answer to the massive CG-NAT problem! MikroTik's Back To Home (BTH) feature is a game-changer."
---

You want a VPN server at home, so you can reach your network from anywhere. But your ISP never gave you a public IP address. You are behind CGNAT, where one public IP is shared by many users, and nobody on the internet can connect to your router.

That is the exact problem MikroTik Back To Home solves. It turns your router into a WireGuard VPN server you can reach from anywhere, even with no public IP. And the first setup needs no commands at all.

## What We're Doing

- Look at how Back To Home works, direct and through a relay
- Enable it from the Back To Home mobile app, with no CLI
- Prove it works: reach a shared folder on my home Windows PC from my phone
- Create a guest user with limited access, and test it with a QR code
- Test the same guest setup in the plain WireGuard app
- Check the public IP change and the limits of the feature

## Before You Start

My lab router is a hAP ax lite, ARM CPU, running RouterOS 7.20.2, with the default configuration. Back To Home needs RouterOS 7.12 or newer, and an ARM, ARM64, or TILE CPU. You also need the Back To Home app on your phone, from Google Play or the App Store.

My router sits in the UAE, behind CGNAT. The phone I test from is on a Wi-Fi network in Germany. That distance is the whole point of the test.

One honest note about my lab setup: the router still has its default services open, and I did not harden it before recording. My router sits behind NAT with no public IP, so I accepted that for this test. Do not copy that part into your own setup without thinking about it.

## How It Works

Back To Home is a WireGuard tunnel between your phone and your router. If your router has a public IP, the phone connects to it directly, like a normal WireGuard tunnel. If it does not, the connection goes through a MikroTik relay server.

The relay only helps the two sides find each other. MikroTik's own docs put it this way: even when a direct connection is not possible and the relay must be used, the tunnel still runs from your phone directly to your home router, uninterrupted and securely encrypted. The relay cannot read your traffic. The tunnel is end-to-end encrypted in both cases.

Two limits come with that design. Through the relay, speed can be lower than a direct connection, so test your throughput. And Back To Home is built for simple access to your home network, not for anonymity.

## Step 1: Turn On DDNS

In WinBox, I open IP, then Cloud. First, I enable Dynamic DNS and apply. The router gets a dedicated DNS name. But the page also warns me: the router is behind a NAT, and a remote connection might not work. The address shown is not my public IP. My provider shares that public IP with many users, so nobody can reach my router through it. That warning is the CGNAT problem, written on the screen.

Expected result: a DDNS name is assigned, plus a clear warning that the router is behind NAT.

## Step 2: Enable Back To Home VPN

On the same Cloud page, I enable Back To Home VPN. There is almost nothing to fill in. Behind the scenes, RouterOS does the work.

I open IP, then Firewall, and two new filter rules sit at the top, both related to Back To Home. There is a new source NAT rule for it as well. A new WireGuard interface appears, with a dynamic peer. In IP, then Addresses, a dynamic private IP address sits on that WireGuard interface.

Expected result: the VPN is enabled, and the router has a WireGuard interface, a dynamic peer, firewall rules, and a NAT rule for it.

## Step 3: Connect from the Phone

There are three ways to connect. If your router has a public IP, you can open the app, create a new tunnel, and type in the public IP, the WinBox port, and your router username and password. If you changed the WinBox port from the default, you add it after a colon, for example `:8292`.

Without a public IP, you can share a QR code, or you can join the home Wi-Fi once for the first setup. I use the Wi-Fi way. I connect my phone to the home Wi-Fi, open the app, and create a new tunnel. I enter the router's local IP address, my username and password, and save the password. The app shows the router model, hAP ax lite, and a few options, including file access and using the router's DNS. I leave the router DNS off, name the tunnel, and create it.

Then I switch the phone back to the Germany Wi-Fi and press Connect. The first connection drops for a short moment, then it connects and stays stable. On the router, in the WireGuard peers tab, my phone shows up as a Back To Home VPN peer, and the RX and TX counters move.

Expected result: the tunnel connects from the Germany network, and the peer counters on the router move.

## Step 4: Prove the LAN Access Works

Counters are not proof. Access is proof.

I ping the WireGuard interface address from my phone, and I get replies. I ping my Windows PC on the LAN, and I get replies too. Then I open the shared folder on that Windows PC from my phone. It opens. I create a new file in it from the phone and name it `ramtin.txt`. It appears in the folder on Windows. I open it on Windows, type `test`, and save it. A few seconds later, I open the same file on the phone, and the text is there.

Expected result: ping answers from the LAN, the shared folder opens, and a file edited on Windows shows its new text on the phone.

## Step 5: A Guest User with Limited Access

The main tunnel has full access. A guest should not. Back in IP, then Cloud, I open the Back To Home users tab. This user list exists in RouterOS 7.14 and later. My own login already created one user there automatically.

I create a new user and name it Jose, after my cat. The important setting is allow-lan. If I leave it off, the guest can only use the internet through my router, for example to bypass geo restrictions, and cannot reach my internal network. I also set an expiry of 3 days, and the other fields fill in by themselves. There is a second tab for file access. If I set it to full and apply, the app asks for a file access path, and I enter the root path.

Now I test the new user. I disconnect my old tunnel and delete it, then use the Join Shared option in the app and scan the QR code for the new user. The app reads it, I import it, and I connect. Because this user has full file access, I can now browse the router's file system from the phone.

Then I test the same QR code in the plain WireGuard app. I create a new tunnel, scan the code, name it `ramtin`, and turn it on. The send and receive counters move. I open the shared folder again, create a file named `test99` from the phone, and it appears in the Windows folder. Then I disconnect the WireGuard tunnel and ping the LAN again. Request timed out. I reconnect, and the ping answers again.

Expected result: the guest tunnel connects from a QR code in both apps, file access works, and disconnecting stops the access at once.

## Step 6: Check the Public IP

By default, the Back To Home tunnel changes the client's public IP. I open the IP check page on the phone while connected, and my public IP is now in the UAE, where the router sits. Before the tunnel, the same phone showed a Germany address. That is the geo bypass working, on top of the LAN access.

Expected result: the phone's public IP changes from Germany to the UAE while the tunnel is up.

## Final Thoughts

Back To Home does what it promises. It removes the two things that normally block a home VPN server: the need for a public IP, and the need to configure WireGuard by hand. The app setup takes minutes, and the guest controls are simple enough to use for real: allow-lan off for internet-only guests, an expiry date, and a QR code to hand over.

Keep the limits in mind. If the connection goes through the relay, expect lower speed, and test it before you depend on it. It is a remote access tool for your home or office, not an anonymity tool. And the first connection may drop once before it settles, as mine did. That short drop is normal, not a failure.

For a home network behind CGNAT, this is the easiest VPN server setup I have used on a MikroTik.

## Quick Reference

Settings from this lab:

- Router: hAP ax lite, ARM, RouterOS 7.20.2
- Back To Home needs RouterOS 7.12 or newer, ARM, ARM64, or TILE
- Back To Home users tab needs RouterOS 7.14 or newer
- Menu: IP, then Cloud
- Guest user in this lab: Jose, allow-lan off, expiry 3 days
- WinBox port example: 8292
- Guest file access path used: root

## Official Documentation

- [MikroTik Back To Home Documentation](https://manual.mikrotik.com/docs/network-management/cloud/back-to-home/)
- [MikroTik WireGuard Documentation](https://help.mikrotik.com/docs/spaces/ROS/pages/69664792/WireGuard)
