---
title: "How to Setup WireGuard VPN on MikroTik + Policy Based Routing Guide"
date: 2026-01-22
slug: how-to-setup-wireguard-vpn-on-mikrotik-policy-based-routing-guide
categories: ["MikroTik", "VPN", "Youtube Videos"]
youtube_id: 7qD3G6utj8A
description: "In this MikroTik tutorial, I address one of the most requested topics for RouterOS v7: setting up a high-performance WireGuard VPN and managing traffic flow. You will learn how to not only establish a secure tunnel but also how to config Policy-Based Routing (PBR) to control exactly which parts of your local network use the VPN."
---

WireGuard is one of the fastest and simplest VPN protocols you can run on a MikroTik router. But getting the tunnel up is only half the job. The real question is what your traffic does after that. Does all of it go through the tunnel, or only part of it?

In this lab, I connect my home MikroTik router to a WireGuard server, then I decide exactly which traffic uses the tunnel. I show two ways to build the tunnel: the one-click WG Import feature, and the manual way, step by step. Then I add policy-based routing, so the router sends all LAN traffic through the VPN, with one exception for a single website.

## What We're Building

- A WireGuard tunnel from my MikroTik router to a WireGuard server
- The same tunnel built twice: once with WG Import, once by hand
- Policy-based routing that sends all LAN traffic through the tunnel
- One address-list exception, so a single website stays off the VPN
- MTU and MSS settings that keep web pages loading cleanly over the tunnel

My WireGuard server runs on my own Ubuntu server. If you use a config file from a VPN provider instead, the process is the same.

## Before You Start

My router runs RouterOS 7.20.6, with the default configuration, connected to the internet from my home office. WireGuard has been part of RouterOS since version 7, so if your router still runs RouterOS 6, you need to upgrade first. The WG Import button needs RouterOS 7.12 or newer. The manual method works on older RouterOS 7 versions too.

You need a WireGuard config file. Mine came from my own server panel. It has two parts: my side of the tunnel (private key, private IP address, DNS) and the server side (public key, preshared key, allowed IPs, persistent keepalive, endpoint address and port).

One small detail from the video: I set persistent keepalive to 10 seconds, moved the last two lines of the file into the right order, and removed an empty line, so MikroTik reads the file cleanly.

## Step 1: Test the Config File on My Computer First

Before I touch the router, I test the config file on my Mac. I create a new client in my WireGuard panel, download the config file, and import it into the WireGuard app. I check my public IP first: it starts with 139, and I am in Germany.

After I activate the tunnel, the sent and received counters start moving. That tells me the tunnel is up. I open the IP check page again, and my public IP is now in New Jersey. I disconnect, and my IP is back in Germany. The config file works. Now I can put it on the router with confidence.

Expected result: the tunnel activates, traffic counters move, and the public IP changes from Germany to New Jersey.

## Step 2: One-Click Setup with WG Import

In WinBox, I drag the config file onto the router, then open the WireGuard menu and click WG Import. I pick the file and confirm. One second later, the interface is there.

MikroTik creates an interface named WG1, generates a random listen port, and fills in the private key. The public key is generated from it. In the Peers tab, the peer is already there too, with the public key, endpoint, endpoint port, allowed addresses, and preshared key from the file. The RX and TX counters move, so the tunnel is established.

I check IP, then Addresses: the private IP from the config file sits on the WG1 interface. Then I open a terminal in WinBox and ping the WireGuard gateway. I get replies. I disable the interface for a second, and the ping requests time out. I enable it again, and the replies come back. That is the cleanest proof the tunnel itself works.

Expected result: WG1 exists with a peer, RX and TX move, and pings to the tunnel gateway answer only while the interface is enabled.

## Step 3: The Manual Way

WG Import is fast, but I want to show what it does under the hood. So I delete the interface, the peer, and the IP address, and build the same tunnel by hand.

First, the interface. In WireGuard, I create a new interface named wg-1. The listen port does not matter here. The one field that must be right is the private key, so I copy it from the config file and paste it in. After I apply, a random port is generated and the public key appears.

Second, the address. In IP, then Addresses, I add the private IP from the config file on the wg-1 interface.

Third, the peer. In the Peers tab, I create a new peer on wg-1. I paste the server public key, the endpoint address, and the endpoint port. Allowed address is 0.0.0.0/0. I paste the preshared key and set persistent keepalive to 10 seconds. After I apply, RX and TX start moving, and a ping to the WireGuard server answers.

Expected result: the same tunnel as before, built from three pieces I entered myself, with traffic flowing.

## Step 4: Policy-Based Routing for All LAN Traffic

The tunnel is up, but no LAN user is using it yet. Their traffic still leaves through the normal internet connection. That is where policy-based routing comes in.

First, I disable one default firewall rule: the fasttrack rule in the forward chain. Fasttrack conflicts with the mangle rule I am about to create. The filter rules stay in place, so the router is still protected.

Then I create a mangle rule:

- Chain: prerouting
- Source address: my LAN network
- Destination address: anything except my LAN network
- Action: mark routing, with the new routing mark `VPN`

The mark needs a routing table. In Routing, then Tables, I create a table named `VPN` and check the FIB box. Back in the mangle rule, I set the new routing mark to `VPN`.

Next, the route. In IP, then Routes, I add a default route: destination 0.0.0.0/0, gateway set to the WireGuard interface, routing table `VPN`.

One more piece: NAT. The default masquerade rule uses the WAN interface list, and ether1 is in that list. I add the WireGuard interface to the WAN list too, in Interfaces, then Interface List. Now a LAN client can reach the internet through the tunnel. I ping Cloudflare DNS from a client, and I get replies.

Expected result: LAN clients reach the internet, and their traffic leaves through the WireGuard tunnel.

## Step 5: MTU and MSS, So Pages Load Cleanly

A tunnel adds overhead, so I make two small changes for safety. On the WireGuard interface, I set MTU to 1360 to prevent fragmentation.

Then I add a second mangle rule, this one in the forward chain: protocol TCP, out-interface set to the WireGuard interface, TCP flags set to SYN, action change MSS with clamp to PMTU. This one is optional, but it keeps web browsing smooth over the tunnel. After I add it, I watch the rule and packets start matching it.

To test, I ping Cloudflare DNS with a 1332-byte packet. It works. Then I open the IP check page, and I get a US address.

Expected result: the 1332-byte ping answers, the MSS rule matches packets, and web pages open with a US public IP.

## Step 6: One Website Stays Off the Tunnel

Sending everything through the tunnel is not always what you want. Some sites, like a bank or a streaming service, may need your real location. So I show how to make one exception.

In IP, then Firewall, then Address Lists, I create a list named `NOVPN` and add iplocation.net to it. The router resolves the site through DNS and fills in its IP addresses by itself. That only works if the router has a working DNS server set, and mine does.

Then I open the first mangle rule again and exclude the `NOVPN` list from the destination. Now the rule reads: traffic from my LAN, going anywhere except my LAN and except the addresses in `NOVPN`, gets marked for the VPN table.

I test it. I open iplocation.net, and my Germany IP shows up. I open the IP check page again, and my US address shows up. Same router, same minute, two different exits, decided by the destination.

Expected result: iplocation.net shows the Germany IP, everything else shows the US IP.

## Final Thoughts

MikroTik makes this easy. WG Import builds the whole tunnel from one file in about a second, and the manual method is only three pieces: interface, address, peer. Policy-based routing is one mangle rule, one routing table, and one route.

The part worth learning is the logic, not the clicks. Mark the traffic you want in the tunnel, give that mark its own routing table, and put a default route in that table. Once you have that pattern, you can build any version of it: all traffic through the VPN, one country through the VPN, or one website kept outside it. That is the whole idea, and it is the same idea behind the exception list at the end.

## Quick Reference

Settings from this lab, in one place:

- RouterOS version: 7.20.6
- WireGuard needs RouterOS 7; WG Import needs 7.12 or newer
- Interface name: wg-1 (WG Import creates WG1)
- Persistent keepalive: 10 seconds
- Peer allowed address: 0.0.0.0/0
- WireGuard MTU: 1360
- Ping test size: 1332 bytes
- Routing table and mark: VPN
- Mangle rule 1: chain prerouting, action mark routing
- Mangle rule 2: chain forward, TCP, SYN flag, action change MSS, clamp to PMTU
- Address list for exceptions: NOVPN

## Official Documentation

- [MikroTik WireGuard Documentation](https://help.mikrotik.com/docs/spaces/ROS/pages/69664792/WireGuard)
