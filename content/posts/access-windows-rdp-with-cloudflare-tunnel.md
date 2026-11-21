---
title: "Access Windows RDP with Cloudflare Tunnel (No Port Forwarding!)"
date: 2026-11-20
slug: access-windows-rdp-with-cloudflare-tunnel
categories: ["VPN", "Windows", "Youtube Videos"]
youtube_id: QlN0brpdPVE
description: "Reach your home Windows PC from any browser with Cloudflare Tunnel and Access — no port forwarding, no public IP, no VPN server. The PC makes an outbound connection; Access checks your email first."
---

If you want to reach your Windows PC from outside your home network, the usual answers are all annoying. You open a port on your router and hope nobody scans it. You set up a VPN server and maintain it. Or you install a third-party tool and trust someone else's cloud with your desktop. And if your provider puts you behind CGNAT, port forwarding is not even on the table.

There is a fourth way. Cloudflare Tunnel lets the Windows PC make an outbound connection to Cloudflare, and Cloudflare Access puts a login gate in front of it. Nothing inbound is ever opened. You open a browser tab, prove who you are, and you are looking at your own Windows desktop.

This guide is a runbook: nine steps, in order, each with the exact click path and the result you should see before moving on. Follow them with your own values and you will end up with the same setup.

## Your Values

Every step below uses example values. Replace them with your own — the steps are identical.

- Domain: `yourdomain.com` — a domain you manage in Cloudflare.
- Windows PC LAN IP: `192.168.1.100` — find yours by running `ipconfig` on the PC and reading the IPv4 Address.
- Tunnel name: `home-rdp` — any name you like.
- Target name: `home-windows-pc` — any name you like.
- Public address: `rdp.yourdomain.com` — the subdomain you will type in the browser.
- Your email: `you@example.com` — the email allowed to sign in. You can add more than one.
- Team domain: `your-team.cloudflareaccess.com` — shown at Zero Trust, then Settings, then Team domain.

## Before You Start

You need a Cloudflare account and at least one domain managed in Cloudflare. You need a Windows 10 or 11 Pro or Enterprise machine. Windows Home cannot host Remote Desktop, and the Windows account must have a password. The RDP security layer must accept TLS, so Negotiate or SSL, not the legacy RDP layer.

This runs on Cloudflare's Zero Trust free plan, which covers up to 50 users. Free does not mean no card. Cloudflare still asks for a payment method on file before the free subscription activates. It never charges it.

One warning that matters: the install command for cloudflared contains a token. Treat it like a password. Never show it on camera and never paste it anywhere public. If it leaks, rotate it from the tunnel settings.

## Connect the PC to Cloudflare

**Step 1 — Prepare Windows.** Check the edition first: run `winver`. It must say Pro or Enterprise. Then turn on Remote Desktop: Settings, then System, then Remote Desktop, turn it on, and confirm. The default RDP port is 3389, and it stays closed to the internet. That is the whole point. Now find the PC's LAN IP: run `ipconfig` and read the IPv4 Address. In this guide that is `192.168.1.100`.

**Step 2 — Create the tunnel.** In the Cloudflare dashboard, open Networking, then Tunnels, and click Create Tunnel. Choose Cloudflared and name it `home-rdp`. Click Save. The Install and Run page shows Windows and 64-bit, with an install command and a token.

**Step 3 — Install cloudflared.** Download the MSI from that page and install it. Open Command Prompt as administrator and run the install command from the page:

```
cloudflared.exe service install <TOKEN>
```

If the service is already installed, run `cloudflared.exe service uninstall` first, then install again. Expected result: the service installs and starts, and the tunnel status in the dashboard turns Healthy. Do not continue until it does. The connection is started by the Windows machine, not by Cloudflare, so no public IP address and no port forwarding are needed. Cloudflare's own docs describe it the same way: the daemon creates outbound-only connections.

## Point Cloudflare at the PC

**Step 4 — Create the route.** The tunnel exists, but Cloudflare needs to know which machine it leads to. Go to Networking, then Routes, then Create route, then Tunnel CIDR. Pick the `home-rdp` tunnel, set the network to `192.168.1.100/32`, and leave the virtual network on default. Click Create route. The /32 means one address only, not the whole network. When the route is listed, that step is done.

**Step 5 — Create the target.** Go to Zero Trust, then Access controls, then Targets, then Add a target. The hostname is `home-windows-pc`. The IPv4 address is `192.168.1.100` — pick the option that shows virtual network default and the tunnel name. Click Add target. A target is only a name pointing at an IP. The Access application refers to the machine by this name.

**Step 6 — Create the DNS record.** Open your domain, go to DNS, then Records, then Add record. Type A, name `rdp`, IPv4 address `240.0.0.0`, proxy status Proxied. Click Save. The IP here is a placeholder from Cloudflare's docs. `240.0.0.0` sits in the reserved Class E range and has no real route on the internet — no server is there. The record only needs to be valid and proxied. The proxy sends the traffic to the tunnel, and the route and the target decide the real destination. Do not use `224.0.0.0` instead: that is the multicast range.

## Lock the Door with Access

**Step 7 — Create the application and the policy.** Go to Zero Trust, then Access controls, then Applications, then Create new application, then Self-hosted and private. Set the subdomain to `rdp` and the domain to `yourdomain.com`. Turn on "Allow access through browser-based RDP, SSH, or VNC sessions" and choose RDP. Set the target hostname to `home-windows-pc` and the port to 3389.

Then create the policy inside it. Name it `rdp-allow-owner`, set the action to Allow, and use the Emails selector with your email address. In the policy Connection settings, set Text controls and File controls to Both directions allowed. That is what enables clipboard and file transfer. Both are disabled by default in a new policy. Keep "Authenticate with Cloudflare One Client" off, and create the application. Policies deny by default. Only the allowed email gets through.

**Step 8 — Add the policy to the App Launcher.** This step is easy to miss. Go to Access controls, then Access settings, then Manage your App Launcher, then Manage. Add current policies, choose `rdp-allow-owner`, and save. Without this step, the tile never appears.

## Test It from Outside

**Step 9 — Sign in from any browser.** Open `https://your-team.cloudflareaccess.com` in an incognito window. That is your team domain, found at Zero Trust, then Settings, then Team domain. Sign in with the allowed email. The one-time PIN arrives by email and expires in 10 minutes. Click the `rdp` tile, then enter the Windows username and password.

Expected result: the local Windows session ends and the browser shows the desktop. Test the clipboard: copy a string on your own desktop and paste it into the remote session. It should appear. That is the whole setup working, end to end.

## If It Does Not Work

- "That account does not have access": check Zero Trust, then Insights & Logs, then Access authentication logs. If it says Blocked, check that the email is in the policy and that the policy is in the App Launcher. Then retry in an incognito window. An old browser session is a common cause.
- "service is already installed": run `cloudflared.exe service uninstall` first, then install again.
- Tunnel will not turn Healthy: is Windows online? Is the Cloudflared agent service running (check services.msc)? Is the outbound connection on port 7844 blocked?
- RDP will not connect: check the /32 route and the IP, check Remote Desktop is on, and check the security layer accepts TLS.

## Honest Limits

File transfer was enabled in the policy, but I did not test it on camera. Only the clipboard was tested live. The docs call file transfer beta, with a 2 GB limit per file and 1000 files per upload. Treat it as untested until you try it yourself.

The direct URL format is in the docs, but I did not test it for this build. Use the App Launcher method shown in the video.

Clipboard is text only, with a 500 KB maximum. Audio is not supported: no microphone, no speakers. The session lasts 24 hours by default. And the obvious one: if the PC goes offline or loses internet, the tunnel drops and you cannot connect until it comes back. The service reconnects by itself.

One more thing I want to be precise about: the team domain name is shown in the dashboard, but the dashboard does not say whether it came from your domain name or was typed in by hand. I will not claim either.

## Cleanup

To remove everything, work in this order: first the Access application, then detach and delete the policy from the App Launcher, then the target, then the DNS record, then the route, then on Windows run `cloudflared.exe service uninstall`, and finally delete the tunnel. You cannot delete a tunnel while a connector is still active.

## Final Thoughts

I like this setup for one reason: it reaches one PC and nothing else. There is no port to scan, no VPN server to maintain, and the login happens twice — once at Cloudflare's gate, once at Windows. That is the right shape for a home PC or a small-office machine you manage yourself.

It is not a replacement for a VPN when you need your whole network. This reaches the PC behind the router, not the router. For the router itself, the companion setup is a tunnel to WinBox. For one Windows machine from any browser, this is the simplest secure path I have found, and it costs nothing.

## Links

Cloudflare Tunnel documentation: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/

Browser-based RDP (Cloudflare blog): https://blog.cloudflare.com/browser-based-rdp/

Cloudflare Zero Trust dashboard: https://one.dash.cloudflare.com/
