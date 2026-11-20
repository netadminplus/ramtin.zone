---
title: "Access Windows RDP with Cloudflare Tunnel (No Port Forwarding!)"
date: 2026-11-20
slug: access-windows-rdp-with-cloudflare-tunnel
categories: ["VPN", "Windows", "Youtube Videos"]
youtube_id: QlN0brpdPVE
description: "Reach your home Windows PC from any browser with Cloudflare Tunnel and Access — no port forwarding, no public IP, no VPN server. The PC makes an outbound connection; Access checks your email first."
---

If you want to reach your Windows PC from outside your home network, the usual answers are all annoying. You open a port on your router and hope nobody scans it. You set up a VPN server and maintain it. Or you install a third-party tool and trust someone else's cloud with your desktop. And if your internet provider puts you behind CGNAT, port forwarding is not even on the table. My own connection is behind CGNAT, so that door was closed before I started.

There is a fourth way. Cloudflare Tunnel lets the Windows PC make an outbound connection to Cloudflare, and Cloudflare Access puts a login gate in front of it. Nothing inbound is ever opened. You open a browser tab, prove who you are, and you are looking at your own Windows desktop.

In this lab, I am going to connect one Windows 11 Pro PC to Cloudflare, give it a name and an address, lock it behind an email allow policy, and test it live from an incognito browser — including the clipboard between my own desktop and the remote one.

## Before You Start

You need a Cloudflare account and at least one domain managed in Cloudflare. You need a Windows 10 or 11 Pro or Enterprise machine. Windows Home cannot host Remote Desktop, and the Windows account must have a password. The RDP security layer must accept TLS, so Negotiate or SSL, not the legacy RDP layer.

My setup values, so you can follow along exactly: domain ramtiin.ir, Windows PC at 192.168.30.204, tunnel name home-rdp-test, target name home-windows-pc, final address rdp.ramtiin.ir, and my email as the only allowed address. Your values will differ. The steps are the same.

One detail before anything else: this runs on Cloudflare's Zero Trust free plan, which covers up to 50 users. Free does not mean no card. Cloudflare still asks for a payment method on file before the free subscription activates. It never charges it.

And a warning that matters: the install command for cloudflared contains a token. Treat it like a password. Never show it on camera and never paste it anywhere public. If it leaks, rotate it from the tunnel settings.

## Connect the PC to Cloudflare

First, enable Remote Desktop on the Windows machine. Open Settings, go to System, then Remote Desktop, turn it on, and confirm. Before that, check the edition: run `winver`. Mine showed Windows 11 Pro. The default RDP port is 3389, and it stays closed to the internet. That is the whole point.

Next, create the tunnel. In the Cloudflare dashboard, open Networking, then Tunnels, and click Create Tunnel. Choose Cloudflared and name it home-rdp-test. The Install and Run page shows Windows and 64-bit, with an install command and a token.

Then install cloudflared on Windows. Download the MSI from that page and install it. Open Command Prompt as administrator and run the install command from the page:

```
cloudflared.exe service install <TOKEN>
```

If the service is already installed, run `cloudflared.exe service uninstall` first, then install again. When it works, the service installs and starts, and the tunnel status in the dashboard turns Healthy. Do not continue until it does. The connection is initiated by the Windows machine, not by Cloudflare, so no public IP address and no port forwarding are needed. Cloudflare's own docs describe it the same way: the daemon creates outbound-only connections.

## Point Cloudflare at the PC

Now the tunnel exists, but Cloudflare needs to know which machine it leads to. Create a route: Networking, then Routes, then Create route, then Tunnel CIDR. Pick the home-rdp-test tunnel, set the network to 192.168.30.204/32, and leave the virtual network on default. The /32 means one address only, not the whole network. When the route is listed, that step is done.

Then create a target: Zero Trust, then Access controls, then Targets, then Add a target. The hostname is home-windows-pc. The IPv4 address is 192.168.30.204 — pick the option that shows virtual network default and the tunnel name. A target is only a name pointing at an IP. The Access application refers to the machine by this name.

Then the DNS record: open the ramtiin.ir domain, go to DNS, then Records, then Add record. Type A, name rdp, IPv4 address 240.0.0.0, proxy status Proxied. The IP here is a placeholder from Cloudflare's docs. 240.0.0.0 sits in the reserved Class E range and has no real route on the internet. The record only needs to be valid and proxied. The proxy sends the traffic to the tunnel, and the route and the target decide the real destination.

## Lock the Door with Access

Create the application: Zero Trust, then Access controls, then Applications, then Create new application, then Self-hosted and private. Set the subdomain to rdp and the domain to ramtiin.ir. Turn on "Allow access through browser-based RDP, SSH, or VNC sessions" and choose RDP. Set the target hostname to home-windows-pc and the port to 3389.

Then create the policy inside it. Name it rdp-allow-owner, set the action to Allow, and use the Emails selector with the allowed email address. You can add more than one email. In the policy Connection settings, set Text controls and File controls to Both directions allowed. That is what enables clipboard and file transfer. Both are disabled by default in a new policy. Keep "Authenticate with Cloudflare One Client" off, and create the application. Policies deny by default. Only the allowed email gets through.

One more step, easy to miss: add the policy to the App Launcher. Go to Access controls, then Access settings, then Manage your App Launcher, then Manage. Add current policies, choose rdp-allow-owner, and save. Without this step, the tile never appears.

## Test It from Outside

Open https://ramtiin.cloudflareaccess.com in an incognito window. That is your team domain, found at Zero Trust, then Settings, then Team domain. Sign in with the allowed email. The one-time PIN arrives by email and expires in 10 minutes. Click the rdp tile, then enter the Windows username and password.

When it works, the local Windows session ends and the browser shows the desktop. I tested the clipboard by copying a random string on my own desktop and pasting it into the remote session. It worked. If you get "That account does not have access", check the Access authentication logs, check that the email is in the policy and the policy is in the App Launcher, and retry in an incognito window. An old browser session is a common cause.

## Honest Limits

File transfer was enabled in the policy, but I did not test it on camera. Only the clipboard was tested live. The docs call file transfer beta, with a 2 GB limit per file and 1000 files per upload. Treat it as untested until you try it yourself.

The direct URL format is in the docs, but I did not test it for this build. Use the App Launcher method shown in the video.

Clipboard is text only, with a 500 KB maximum. Audio is not supported: no microphone, no speakers. The session lasts 24 hours by default. And the obvious one: if the PC goes offline or loses internet, the tunnel drops and you cannot connect until it comes back. The service reconnects by itself.

One more thing I want to be precise about: the team domain name, ramtiin in my case, is shown in the dashboard, but the dashboard does not say whether it came from my domain name or was typed in by hand. I will not claim either.

## Final Thoughts

I like this setup for one reason: it reaches one PC and nothing else. There is no port to scan, no VPN server to maintain, and the login happens twice — once at Cloudflare's gate, once at Windows. That is the right shape for a home PC or a small-office machine you manage yourself.

It is not a replacement for a VPN when you need your whole network. This reaches the PC behind the router, not the router. For the router itself, the companion setup is a tunnel to WinBox. For one Windows machine from any browser, this is the simplest secure path I have found, and it costs nothing.

## Links

Cloudflare Tunnel documentation: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/

Browser-based RDP (Cloudflare blog): https://blog.cloudflare.com/browser-based-rdp/

Cloudflare Zero Trust dashboard: https://one.dash.cloudflare.com/
